import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Historical sunspot data
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

# Create DataFrame
df = pd.DataFrame(data)

# Feature engineering for solar cycle pattern (11-year cycle)
df['Cycle_Position'] = (df['Year'] - 1970) % 11
df['Years_Since_1970'] = df['Year'] - 1970
df['Cycle_Number'] = ((df['Year'] - 1970) // 11).astype(int)

# Create features for prediction
def create_features(df):
    """Create features for time series prediction"""
    df_features = df.copy()
    
    # Lag features (previous years)
    for lag in [1, 2, 3, 4, 5]:
        df_features[f'Lag_{lag}'] = df_features['Sunspot_Number'].shift(lag)
    
    # Moving averages
    df_features['MA_3'] = df_features['Sunspot_Number'].rolling(window=3, min_periods=1).mean()
    df_features['MA_5'] = df_features['Sunspot_Number'].rolling(window=5, min_periods=1).mean()
    df_features['MA_11'] = df_features['Sunspot_Number'].rolling(window=11, min_periods=1).mean()
    
    # Cycle-based features
    df_features['Sin_Cycle'] = np.sin(2 * np.pi * df_features['Cycle_Position'] / 11)
    df_features['Cos_Cycle'] = np.cos(2 * np.pi * df_features['Cycle_Position'] / 11)
    
    # Trend
    df_features['Trend'] = df_features['Years_Since_1970']
    
    return df_features

df_features = create_features(df)

# Prepare data for training (remove NaN rows from lag features)
train_data = df_features.dropna()
X = train_data[['Cycle_Position', 'Years_Since_1970', 'Cycle_Number', 
                'Lag_1', 'Lag_2', 'Lag_3', 'Lag_4', 'Lag_5',
                'MA_3', 'MA_5', 'MA_11',
                'Sin_Cycle', 'Cos_Cycle', 'Trend']]
y = train_data['Sunspot_Number']

# Split data (use last 10 years for validation)
split_idx = len(train_data) - 10
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

# Train Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
rf_model.fit(X_train, y_train)

# Evaluate model
train_score = rf_model.score(X_train, y_train)
test_score = rf_model.score(X_test, y_test)
print(f"Model Training Score (R²): {train_score:.4f}")
print(f"Model Test Score (R²): {test_score:.4f}")

# Function to predict future years
def predict_future_years(model, last_data, start_year, end_year):
    """Predict sunspot numbers for future years"""
    predictions = []
    current_data = last_data.copy()
    
    for year in range(start_year, end_year + 1):
        # Create features for this year
        cycle_pos = (year - 1970) % 11
        years_since = year - 1970
        cycle_num = (year - 1970) // 11
        
        # Use recent predictions/last known values for lags
        lag_values = current_data['Sunspot_Number'].tail(5).values[::-1]
        
        # Calculate moving averages
        ma_3 = current_data['Sunspot_Number'].tail(3).mean()
        ma_5 = current_data['Sunspot_Number'].tail(5).mean()
        ma_11 = current_data['Sunspot_Number'].tail(11).mean() if len(current_data) >= 11 else current_data['Sunspot_Number'].mean()
        
        # Cycle features
        sin_cycle = np.sin(2 * np.pi * cycle_pos / 11)
        cos_cycle = np.cos(2 * np.pi * cycle_pos / 11)
        
        # Create feature vector
        features = np.array([[
            cycle_pos, years_since, cycle_num,
            lag_values[0] if len(lag_values) > 0 else current_data['Sunspot_Number'].iloc[-1],
            lag_values[1] if len(lag_values) > 1 else current_data['Sunspot_Number'].iloc[-1],
            lag_values[2] if len(lag_values) > 2 else current_data['Sunspot_Number'].iloc[-1],
            lag_values[3] if len(lag_values) > 3 else current_data['Sunspot_Number'].iloc[-1],
            lag_values[4] if len(lag_values) > 4 else current_data['Sunspot_Number'].iloc[-1],
            ma_3, ma_5, ma_11,
            sin_cycle, cos_cycle, years_since
        ]])
        
        # Predict
        pred = model.predict(features)[0]
        predictions.append({'Year': year, 'Sunspot_Number': max(0, pred)})  # Ensure non-negative
        
        # Update current_data for next iteration
        new_row = pd.DataFrame({'Year': [year], 'Sunspot_Number': [pred]})
        current_data = pd.concat([current_data, new_row], ignore_index=True)
    
    return pd.DataFrame(predictions)

# Predict next 15 years (2025-2039)
future_predictions = predict_future_years(rf_model, df_features, 2025, 2039)

print("\n" + "="*60)
print("PREDICTIONS FOR FUTURE YEARS (2025-2039)")
print("="*60)
print(future_predictions.to_string(index=False))

# Combine historical and predicted data for visualization
all_data = pd.concat([df[['Year', 'Sunspot_Number']], future_predictions], ignore_index=True)
all_data['Type'] = ['Historical'] * len(df) + ['Predicted'] * len(future_predictions)

# Create visualization
plt.figure(figsize=(16, 8))

# Plot historical data
historical = all_data[all_data['Type'] == 'Historical']
predicted = all_data[all_data['Type'] == 'Predicted']

plt.plot(historical['Year'], historical['Sunspot_Number'], 
         'o-', color='#2E86AB', linewidth=2, markersize=6, 
         label='Historical Data', alpha=0.8)

# Plot predictions
plt.plot(predicted['Year'], predicted['Sunspot_Number'], 
         's--', color='#A23B72', linewidth=2, markersize=5, 
         label='Predicted Data', alpha=0.8)

# Add vertical lines for 11-year cycle markers
cycle_start_year = 1970
for i in range(0, 8):  # Mark cycles from 1970 to ~2050
    cycle_year = cycle_start_year + i * 11
    if cycle_year <= 2039:
        plt.axvline(x=cycle_year, color='gray', linestyle=':', 
                   alpha=0.5, linewidth=1)
        if cycle_year >= 1970:
            plt.text(cycle_year, plt.ylim()[1] * 0.95, 
                    f'Cycle {i}', rotation=90, 
                    verticalalignment='top', fontsize=8, alpha=0.7)

# Highlight the 11-year cycle pattern
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)

# Formatting
plt.xlabel('Year', fontsize=12, fontweight='bold')
plt.ylabel('Sunspot Number', fontsize=12, fontweight='bold')
plt.title('Sunspot Number Prediction Model (1970-2039)\n11-Year Solar Cycle Pattern', 
          fontsize=14, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(loc='upper left', fontsize=10, framealpha=0.9)

# Add text annotation about solar cycle
plt.text(0.02, 0.98, 
         'Vertical dotted lines mark 11-year solar cycle boundaries',
         transform=plt.gca().transAxes,
         fontsize=9, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('sunspot_prediction.png', dpi=300, bbox_inches='tight')
print("\n" + "="*60)
print("Graph saved as 'sunspot_prediction.png'")
print("="*60)

# Display the plot
plt.show()

# Print cycle analysis
print("\n" + "="*60)
print("SOLAR CYCLE ANALYSIS")
print("="*60)
print(f"Average cycle length: ~11 years")
print(f"Peak years observed: 1979-1980, 1989-1990, 2000-2001, 2013-2014, 2023-2024")
print(f"Minimum years observed: 1976, 1986, 1996, 2008-2009, 2019")
print(f"\nNext predicted peak: ~{future_predictions.loc[future_predictions['Sunspot_Number'].idxmax(), 'Year']}")
print(f"Next predicted minimum: ~{future_predictions.loc[future_predictions['Sunspot_Number'].idxmin(), 'Year']}")

