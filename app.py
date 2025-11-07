from flask import Flask, render_template, request, redirect, url_for
import io
import base64
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid display issues
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)


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
    df = pd.DataFrame(data)
    return df


def create_features(df):
    df_features = df.copy()
    df_features['Cycle_Position'] = (df_features['Year'] - 1970) % 11
    df_features['Years_Since_1970'] = df_features['Year'] - 1970
    df_features['Cycle_Number'] = ((df_features['Year'] - 1970) // 11).astype(int)

    for lag in [1, 2, 3, 4, 5]:
        df_features[f'Lag_{lag}'] = df_features['Sunspot_Number'].shift(lag)

    df_features['MA_3'] = df_features['Sunspot_Number'].rolling(window=3, min_periods=1).mean()
    df_features['MA_5'] = df_features['Sunspot_Number'].rolling(window=5, min_periods=1).mean()
    df_features['MA_11'] = df_features['Sunspot_Number'].rolling(window=11, min_periods=1).mean()

    df_features['Sin_Cycle'] = np.sin(2 * np.pi * df_features['Cycle_Position'] / 11)
    df_features['Cos_Cycle'] = np.cos(2 * np.pi * df_features['Cycle_Position'] / 11)

    df_features['Trend'] = df_features['Years_Since_1970']
    return df_features


def train_model(df_features):
    train_data = df_features.dropna()
    X = train_data[['Cycle_Position', 'Years_Since_1970', 'Cycle_Number',
                    'Lag_1', 'Lag_2', 'Lag_3', 'Lag_4', 'Lag_5',
                    'MA_3', 'MA_5', 'MA_11', 'Sin_Cycle', 'Cos_Cycle', 'Trend']]
    y = train_data['Sunspot_Number']

    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X, y)
    return model


def predict_future_years(model, df_features, start_year, end_year):
    base_df = df_features[['Year', 'Sunspot_Number']].copy()
    current_data = base_df.copy()
    preds = []
    for year in range(start_year, end_year + 1):
        cycle_pos = (year - 1970) % 11
        years_since = year - 1970
        cycle_num = (year - 1970) // 11

        lag_vals = current_data['Sunspot_Number'].tail(5).values[::-1]
        ma_3 = current_data['Sunspot_Number'].tail(3).mean()
        ma_5 = current_data['Sunspot_Number'].tail(5).mean()
        ma_11 = current_data['Sunspot_Number'].tail(11).mean() if len(current_data) >= 11 else current_data['Sunspot_Number'].mean()
        sin_cycle = np.sin(2 * np.pi * cycle_pos / 11)
        cos_cycle = np.cos(2 * np.pi * cycle_pos / 11)

        features = np.array([[
            cycle_pos, years_since, cycle_num,
            lag_vals[0] if len(lag_vals) > 0 else current_data['Sunspot_Number'].iloc[-1],
            lag_vals[1] if len(lag_vals) > 1 else current_data['Sunspot_Number'].iloc[-1],
            lag_vals[2] if len(lag_vals) > 2 else current_data['Sunspot_Number'].iloc[-1],
            lag_vals[3] if len(lag_vals) > 3 else current_data['Sunspot_Number'].iloc[-1],
            lag_vals[4] if len(lag_vals) > 4 else current_data['Sunspot_Number'].iloc[-1],
            ma_3, ma_5, ma_11, sin_cycle, cos_cycle, years_since
        ]])

        pred = float(model.predict(features)[0])
        preds.append({'Year': year, 'Sunspot_Number': max(0.0, pred)})
        current_data = pd.concat([current_data, pd.DataFrame({'Year': [year], 'Sunspot_Number': [pred]})], ignore_index=True)

    return pd.DataFrame(preds)


def predict_single_year(model, df_features, target_year):
    """Predict sunspot number for a single year"""
    base_df = df_features[['Year', 'Sunspot_Number']].copy()
    current_data = base_df.copy()
    
    # If target year is in historical data, return it
    if target_year <= 2024:
        hist_data = current_data[current_data['Year'] == target_year]
        if not hist_data.empty:
            return float(hist_data['Sunspot_Number'].iloc[0])
    
    # Otherwise predict up to target year
    start_year = int(current_data['Year'].max()) + 1
    if start_year <= target_year:
        for year in range(start_year, target_year + 1):
            cycle_pos = (year - 1970) % 11
            years_since = year - 1970
            cycle_num = (year - 1970) // 11

            lag_vals = current_data['Sunspot_Number'].tail(5).values[::-1]
            ma_3 = current_data['Sunspot_Number'].tail(3).mean()
            ma_5 = current_data['Sunspot_Number'].tail(5).mean()
            ma_11 = current_data['Sunspot_Number'].tail(11).mean() if len(current_data) >= 11 else current_data['Sunspot_Number'].mean()
            sin_cycle = np.sin(2 * np.pi * cycle_pos / 11)
            cos_cycle = np.cos(2 * np.pi * cycle_pos / 11)

            features = np.array([[
                cycle_pos, years_since, cycle_num,
                lag_vals[0] if len(lag_vals) > 0 else current_data['Sunspot_Number'].iloc[-1],
                lag_vals[1] if len(lag_vals) > 1 else current_data['Sunspot_Number'].iloc[-1],
                lag_vals[2] if len(lag_vals) > 2 else current_data['Sunspot_Number'].iloc[-1],
                lag_vals[3] if len(lag_vals) > 3 else current_data['Sunspot_Number'].iloc[-1],
                lag_vals[4] if len(lag_vals) > 4 else current_data['Sunspot_Number'].iloc[-1],
                ma_3, ma_5, ma_11, sin_cycle, cos_cycle, years_since
            ]])

            pred = float(model.predict(features)[0])
            current_data = pd.concat([current_data, pd.DataFrame({'Year': [year], 'Sunspot_Number': [max(0.0, pred)]})], ignore_index=True)
        
        return float(current_data[current_data['Year'] == target_year]['Sunspot_Number'].iloc[0])
    return None


def find_solar_max_min(combined_df, end_year):
    """Find solar maximum and minimum years in the data"""
    filtered_df = combined_df[combined_df['Year'] <= end_year].copy()
    if filtered_df.empty or len(filtered_df) < 3:
        return [], []
    
    maxima = []
    minima = []
    
    # Find local maxima and minima
    years = filtered_df['Year'].values
    values = filtered_df['Sunspot_Number'].values
    
    # Look for peaks and valleys with a window approach
    window = 3  # Look at 3 years on each side
    
    for i in range(window, len(years) - window):
        # Check for local maximum - value should be higher than neighbors
        is_max = True
        for j in range(i - window, i + window + 1):
            if j != i and values[j] >= values[i]:
                is_max = False
                break
        
        if is_max and values[i] > 40:  # Only mark significant peaks
            maxima.append((int(years[i]), float(values[i])))
        
        # Check for local minimum - value should be lower than neighbors
        is_min = True
        for j in range(i - window, i + window + 1):
            if j != i and values[j] <= values[i]:
                is_min = False
                break
        
        if is_min and values[i] < 25:  # Only mark significant valleys
            minima.append((int(years[i]), float(values[i])))
    
    # Also check boundaries
    if len(years) > 2:
        # Check first point
        if values[0] > values[1] and values[0] > 40:
            maxima.append((int(years[0]), float(values[0])))
        if values[0] < values[1] and values[0] < 25:
            minima.append((int(years[0]), float(values[0])))
        
        # Check last point
        if values[-1] > values[-2] and values[-1] > 40:
            maxima.append((int(years[-1]), float(values[-1])))
        if values[-1] < values[-2] and values[-1] < 25:
            minima.append((int(years[-1]), float(values[-1])))
    
    # Remove duplicates and sort
    maxima = list(set(maxima))
    minima = list(set(minima))
    maxima.sort(key=lambda x: x[1], reverse=True)
    minima.sort(key=lambda x: x[1])
    
    # Return top 6 maxima and bottom 6 minima to avoid clutter
    return maxima[:6], minima[:6]


def render_plot_png(historical_df, predicted_df, end_year):
    """Render plot from 1970 to end_year with 11-year cycle markers"""
    # Set dark theme for matplotlib
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='#0a0e27')
    ax.set_facecolor('#0a0e27')

    # Filter data up to end_year
    hist_filtered = historical_df[historical_df['Year'] <= end_year].copy()
    pred_filtered = predicted_df[predicted_df['Year'] <= end_year].copy()
    
    # Combine for finding max/min
    combined_df = pd.concat([hist_filtered, pred_filtered], ignore_index=True).sort_values('Year')

    # Plot historical data
    if not hist_filtered.empty:
        ax.plot(hist_filtered['Year'], hist_filtered['Sunspot_Number'], 
                'o-', color='#4A90E2', linewidth=2.5, markersize=6, 
                label='Historical Data', alpha=0.9, markerfacecolor='#6BB6FF')
    
    # Plot predicted data
    if not pred_filtered.empty:
        ax.plot(pred_filtered['Year'], pred_filtered['Sunspot_Number'], 
                's--', color='#FF6B9D', linewidth=2.5, markersize=5, 
                label='Predicted Data', alpha=0.9, markerfacecolor='#FF8FB3')

    # Find and mark solar maxima and minima
    maxima, minima = find_solar_max_min(combined_df, end_year)
    
    # Mark solar maxima
    for year, value in maxima:
        ax.scatter(year, value, s=400, color='#FFD700', marker='*', 
                  edgecolors='#FFA500', linewidths=2.5, zorder=5, alpha=0.95)
        # Get y limits after plotting for proper positioning
        y_min, y_max = ax.get_ylim()
        y_range = y_max - y_min
        ax.annotate('Solar Maximum', xy=(year, value), 
                   xytext=(year, value + y_range * 0.12),
                   fontsize=11, fontweight='bold', color='#FFD700',
                   ha='center', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.6', facecolor='#0a0e27', 
                           edgecolor='#FFD700', linewidth=2, alpha=0.9),
                   arrowprops=dict(arrowstyle='->', color='#FFD700', lw=2))
    
    # Mark solar minima
    for year, value in minima:
        ax.scatter(year, value, s=400, color='#00CED1', marker='v', 
                  edgecolors='#20B2AA', linewidths=2.5, zorder=5, alpha=0.95)
        # Get y limits after plotting for proper positioning
        y_min, y_max = ax.get_ylim()
        y_range = y_max - y_min
        ax.annotate('Solar Minimum', xy=(year, value), 
                   xytext=(year, value - y_range * 0.12),
                   fontsize=11, fontweight='bold', color='#00CED1',
                   ha='center', va='top',
                   bbox=dict(boxstyle='round,pad=0.6', facecolor='#0a0e27', 
                           edgecolor='#00CED1', linewidth=2, alpha=0.9),
                   arrowprops=dict(arrowstyle='->', color='#00CED1', lw=2))

    # Add 11-year cycle markers (vertical lines every 11 years starting from 1970)
    cycle_start_year = 1970
    i = 0
    while True:
        cycle_year = cycle_start_year + i * 11
        if cycle_year > end_year:
            break
        ax.axvline(x=cycle_year, color='#4A5568', linestyle=':', alpha=0.5, linewidth=1.5)
        i += 1

    # Set x-axis ticks to show 11-year intervals
    x_ticks = []
    tick_year = 1970
    while tick_year <= end_year:
        x_ticks.append(tick_year)
        tick_year += 11
    
    # Add end_year if not already in ticks
    if end_year not in x_ticks:
        x_ticks.append(end_year)
    
    ax.set_xticks(sorted(x_ticks))
    ax.set_xlim(1970, end_year)

    # Style axes for dark theme
    ax.tick_params(colors='#E2E8F0')
    ax.spines['bottom'].set_color('#4A5568')
    ax.spines['top'].set_color('#4A5568')
    ax.spines['right'].set_color('#4A5568')
    ax.spines['left'].set_color('#4A5568')

    ax.set_xlabel('Year (11-Year Solar Cycle Scale)', fontsize=12, fontweight='bold', color='#E2E8F0')
    ax.set_ylabel('Sunspot Number', fontsize=12, fontweight='bold', color='#E2E8F0')
    ax.set_title(f'Sunspot Number Prediction (1970–{end_year}) — 11-Year Solar Cycle', 
                fontsize=14, fontweight='bold', pad=15, color='#E2E8F0')
    ax.grid(True, linestyle='--', alpha=0.2, color='#4A5568')
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9, 
             facecolor='#1a1f3a', edgecolor='#4A5568', labelcolor='#E2E8F0')

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png', dpi=160, facecolor='#0a0e27')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('ascii')


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        df = load_data()
        df_features = create_features(df)
        model = train_model(df_features)
        
        # Default values
        user_year = None
        predicted_value = None
        end_year = 2039
        
        if request.method == 'POST':
            try:
                user_year = int(request.form.get('year', ''))
                if user_year < 1970:
                    user_year = 1970
                elif user_year > 2100:
                    user_year = 2100
                
                # Predict for the user's year
                predicted_value = predict_single_year(model, df_features, user_year)
                if predicted_value is not None:
                    end_year = user_year
                    
                    # Generate predictions up to user's year
                    if user_year > 2024:
                        future = predict_future_years(model, df_features, 2025, user_year)
                    else:
                        future = pd.DataFrame(columns=['Year', 'Sunspot_Number'])
                else:
                    # If prediction failed, use defaults
                    future = predict_future_years(model, df_features, 2025, 2039)
            except (ValueError, TypeError) as e:
                # Invalid input, use defaults
                print(f"Error processing year input: {e}")
                future = predict_future_years(model, df_features, 2025, 2039)
        else:
            # Default: show predictions up to 2039
            future = predict_future_years(model, df_features, 2025, 2039)
        
        # Ensure future is a DataFrame
        if future.empty:
            future = pd.DataFrame(columns=['Year', 'Sunspot_Number'])
        
        # Generate the plot
        try:
            img_b64 = render_plot_png(df[['Year', 'Sunspot_Number']], future, end_year)
        except Exception as e:
            print(f"Error generating plot: {e}")
            # Return a simple error message or default plot
            img_b64 = ""
        
        return render_template('index.html',
                               historical=df.to_dict(orient='records'),
                               future=future.to_dict(orient='records'),
                               plot_data=img_b64,
                               user_year=user_year,
                               predicted_value=predicted_value,
                               end_year=end_year)
    except Exception as e:
        print(f"Error in index route: {e}")
        import traceback
        traceback.print_exc()
        return f"<h1>Error</h1><p>An error occurred: {str(e)}</p>", 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Sunspot Prediction Web Application")
    print("="*60)
    print("\nServer starting on http://127.0.0.1:5000")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
