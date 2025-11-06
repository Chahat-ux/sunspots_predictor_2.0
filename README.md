# Sunspot Prediction Model

This project predicts sunspot numbers based on historical data using machine learning techniques, accounting for the 11-year solar cycle pattern.

## Features

- **Time Series Analysis**: Analyzes historical sunspot data from 1970-2024
- **Pattern Recognition**: Identifies the 11-year solar cycle pattern
- **Interactive Year Input**: Users can enter any year (1970-2100) to get predictions
- **Dynamic Predictions**: Predicts sunspot numbers for any future year
- **Customizable Visualization**: Graph automatically adjusts to show data from 1970 to the user's input year
- **11-Year Cycle Scale**: X-axis displays 11-year solar cycle intervals with vertical markers

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Web Application (Recommended)

Start the Flask web server:
```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

**Web App Features:**
1. Enter any year (1970-2100) in the input form
2. Click "Predict Sunspots" to get the predicted sunspot number
3. View the graph showing data from 1970 to your input year
4. See historical data and predictions in tables

### Command Line Script

Run the standalone prediction model:
```bash
python sunspot_prediction.py
```

The script will:
1. Load and analyze historical sunspot data
2. Train a Random Forest regression model
3. Generate predictions for future years (2025-2039)
4. Create a visualization graph saved as `sunspot_prediction.png`
5. Display predictions and cycle analysis in the console

## Model Details

- **Algorithm**: Random Forest Regressor
- **Features**: 
  - Lag features (previous 1-5 years)
  - Moving averages (3, 5, and 11-year windows)
  - Solar cycle position (11-year cycle)
  - Trigonometric features (sin/cos) for cycle pattern
  - Trend features

## Output

- Console output with predictions and model performance metrics
- PNG graph file: `sunspot_prediction.png`
- Graph shows:
  - Historical data (1970-2024) in blue
  - Predicted data (2025-2039) in purple
  - 11-year cycle markers as vertical dotted lines

## Solar Cycle Information

Sunspots follow an approximately 11-year cycle:
- **Peak years**: Maximum sunspot activity
- **Minimum years**: Minimum sunspot activity
- The model accounts for this cyclical pattern in its predictions

