import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Sunspot Predictor", layout="wide")

st.title("🌞 Sunspot Number Prediction (1970–2039)")
st.write("This app predicts future sunspot activity using a Random Forest model based on historical data.")

# ======================
# Historical Data
# ======================
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

df = pd.DataFrame(data)
df['Cycle_Position'] = (df['Year'] - 1970) % 11
df['Years_Since_1970'] = df['Year'] - 1970
df['Cycle_Number'] = ((df['Year'] - 1970) // 11).astype(int)

def create_features(df):
    df_features = df.copy()
    for lag in [1, 2, 3, 4, 5]:
        df_features[f'Lag_{lag}'] = df_features['Sunspot_Number'].shift(lag)
    df_features['MA_3'] = df_features['Sunspot_Number'].rolling(3).mean()
    df_features['MA_5'] = df_features['Sunspot_Number'].rolling(5).mean()
    df_features['MA_11'] = df_features['Sunspot_Number'].rolling(11).mean()
    df_features['Sin_Cycle'] = np.sin(2 * np.pi * df_features['Cycle_Position'] / 11)
    df_features['Cos_Cycle'] = np.cos(2 * np.pi * df_features['Cycle_Position'] / 11)
    df_features['Trend'] = df_features['Years_Since_1970']
    return df_features

df_features = create_features(df).dropna()

X = df_features[['Cycle_Position', 'Years_Since_1970', 'Cycle_Number', 
                'Lag_1', 'Lag_2', 'Lag_3', 'Lag_4', 'Lag_5',
                'MA_3', 'MA_5', 'MA_11', 'Sin_Cycle', 'Cos_Cycle', 'Trend']]
y = df_features['Sunspot_Number']

rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
rf_model.fit(X, y)

def predict_future_years(model, last_data, start_year, end_year):
    predictions = []
    current_data = last_data.copy()
    for year in range(start_year, end_year + 1):
        cycle_pos = (year - 1970) % 11
        years_since = year - 1970
        cycle_num = (year - 1970) // 11
        lag_values = current_data['Sunspot_Number'].tail(5).values[::-1]
        ma_3 = current_data['Sunspot_Number'].tail(3).mean()
        ma_5 = current_data['Sunspot_Number'].tail(5).mean()
        ma_11 = current_data['Sunspot_Number'].tail(11).mean()
        sin_cycle = np.sin(2 * np.pi * cycle_pos / 11)
        cos_cycle = np.cos(2 * np.pi * cycle_pos / 11)
        features = np.array([[cycle_pos, years_since, cycle_num,
                              *lag_values[:5], ma_3, ma_5, ma_11,
                              sin_cycle, cos_cycle, years_since]])
        pred = model.predict(features)[0]
        predictions.append({'Year': year, 'Sunspot_Number': max(0, pred)})
        new_row = pd.DataFrame({'Year': [year], 'Sunspot_Number': [pred]})
        current_data = pd.concat([current_data, new_row], ignore_index=True)
    return pd.DataFrame(predictions)

future_predictions = predict_future_years(rf_model, df_features, 2025, 2039)

st.subheader("📈 Predicted Sunspot Numbers (2025–2039)")
st.dataframe(future_predictions)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['Year'], df['Sunspot_Number'], 'o-', label="Historical", color='#2E86AB')
ax.plot(future_predictions['Year'], future_predictions['Sunspot_Number'], 's--', label="Predicted", color='#A23B72')
ax.set_xlabel("Year")
ax.set_ylabel("Sunspot Number")
ax.set_title("Sunspot Number Prediction (1970–2039)")
ax.legend()
st.pyplot(fig)
