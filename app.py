import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# --- Streamlit setup ---
st.set_page_config(page_title="Sunspot Predictor", layout="wide")

st.title("☀️ Sunspot Predictor — 11-Year Solar Cycle")
st.markdown(
    "<div style='text-align:justify;'>"
    "This app predicts **future sunspot activity** using a Random Forest model trained on historical data (1970–2024). "
    "It visualizes the solar cycle pattern and forecasts up to the year 2039."
    "</div>",
    unsafe_allow_html=True
)

# --- Load data ---
def load_data():
    data = {
        'Year': [1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979,
                 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989,
                 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
                 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
                 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,
                 2020, 2021, 2022, 2023, 2024],
        'Sunspot_Number': [104.5, 66.6, 68.9, 38.0, 34.5, 15.5, 12.6, 27.5, 92.5, 155.4,
                           154.6, 140.4, 115.9, 66.6, 45.9, 17.9, 13.4, 29.4, 100.2, 157.6,
                           142.2, 145.8, 94.5, 54.7, 29.9, 17.5, 8.6, 21.6, 64.2, 93.4,
                           119.6, 110.9, 104.1, 63.6, 40.4, 29.8, 15.2, 7.6, 2.9, 3.1,
                           16.5, 55.7, 57.6, 64.7, 79.3, 69.8, 39.8, 28.6, 12.9, 6.2,
                           24.7, 48.8, 78.1, 121.0, 136.0]
    }
    return pd.DataFrame(data)

# --- Feature engineering ---
def create_features(df):
    df['Cycle_Position'] = (df['Year'] - 1970) % 11
    df['Years_Since_1970'] = df['Year'] - 1970
    df['Cycle_Number'] = ((df['Year'] - 1970) // 11).astype(int)
    for lag in [1,2,3,4,5]:
        df[f'Lag_{lag}'] = df['Sunspot_Number'].shift(lag)
    df['MA_3'] = df['Sunspot_Number'].rolling(3, min_periods=1).mean()
    df['MA_5'] = df['Sunspot_Number'].rolling(5, min_periods=1).mean()
    df['MA_11'] = df['Sunspot_Number'].rolling(11, min_periods=1).mean()
    df['Sin_Cycle'] = np.sin(2*np.pi*df['Cycle_Position']/11)
    df['Cos_Cycle'] = np.cos(2*np.pi*df['Cycle_Position']/11)
    df['Trend'] = df['Years_Since_1970']
    return df.dropna()

# --- Model training ---
def train_model(df):
    X = df[['Cycle_Position','Years_Since_1970','Cycle_Number',
            'Lag_1','Lag_2','Lag_3','Lag_4','Lag_5',
            'MA_3','MA_5','MA_11','Sin_Cycle','Cos_Cycle','Trend']]
    y = df['Sunspot_Number']
    model = RandomForestRegressor(n_estimators=200, random_state=42, max_depth=10)
    model.fit(X, y)
    return model

# --- Prediction ---
def predict_future(model, df, start_year=2025, end_year=2039):
    preds = []
    current = df.copy()
    for year in range(start_year, end_year+1):
        cycle_pos = (year-1970)%11
        years_since = year-1970
        cycle_num = (year-1970)//11
        lag_vals = current['Sunspot_Number'].tail(5).values[::-1]
        ma3 = current['Sunspot_Number'].tail(3).mean()
        ma5 = current['Sunspot_Number'].tail(5).mean()
        ma11 = current['Sunspot_Number'].tail(11).mean()
        sin_cycle = np.sin(2*np.pi*cycle_pos/11)
        cos_cycle = np.cos(2*np.pi*cycle_pos/11)
        X = np.array([[cycle_pos, years_since, cycle_num,
                       *lag_vals, ma3, ma5, ma11, sin_cycle, cos_cycle, years_since]])
        pred = model.predict(X)[0]
        preds.append({'Year':year, 'Sunspot_Number':max(0,pred)})
        current = pd.concat([current, pd.DataFrame({'Year':[year], 'Sunspot_Number':[pred]})])
    return pd.DataFrame(preds)

# --- Plotting ---
def plot_sunspots(df_hist, df_pred):
    plt.style.use('dark_background')
    plt.figure(figsize=(12,6))
    plt.plot(df_hist['Year'], df_hist['Sunspot_Number'], 'o-', label="Historical", color='#4A90E2', lw=2)
    plt.plot(df_pred['Year'], df_pred['Sunspot_Number'], 's--', label="Predicted", color='#FF6B9D', lw=2)
    plt.fill_between(df_pred['Year'], df_pred['Sunspot_Number'], color='#FF6B9D', alpha=0.2)

    # Mark solar maxima and minima
    max_years = df_hist.loc[df_hist['Sunspot_Number'] > 100, 'Year']
    min_years = df_hist.loc[df_hist['Sunspot_Number'] < 15, 'Year']
    for y in max_years:
        plt.axvline(x=y, color='gold', linestyle='--', alpha=0.3)
    for y in min_years:
        plt.axvline(x=y, color='skyblue', linestyle='--', alpha=0.3)

    plt.xlabel("Year", color='white')
    plt.ylabel("Sunspot Number", color='white')
    plt.title("Sunspot Number Prediction (1970–2039)", color='white', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend()
    st.pyplot(plt)

# --- Main workflow ---
df = load_data()
df_feat = create_features(df)
model = train_model(df_feat)
future = predict_future(model, df_feat)

year = st.slider("Select a year to predict:", 2025, 2039, 2030)
pred_future = predict_future(model, df_feat, 2025, year)
predicted_value = pred_future[pred_future['Year']==year]['Sunspot_Number'].values[-1]

st.subheader(f"🔮 Predicted Sunspot Number in {year}: **{predicted_value:.2f}**")
plot_sunspots(df, pred_future)

st.caption("Yellow dashed lines indicate solar maxima; blue dashed lines indicate solar minima (based on historical data).")

   
