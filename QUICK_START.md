# Quick Start Guide

## 🚀 How to Run the Application

### Method 1: Double-click the batch file (Easiest)
1. Double-click `run.bat` in the project folder
2. Wait for the server to start (you'll see "Running on http://0.0.0.0:5000")
3. Open your web browser and go to: **http://localhost:5000**

### Method 2: Command Line
1. Open PowerShell or Command Prompt in this folder
2. Run: `.venv\Scripts\python app.py`
3. Open your browser to: **http://localhost:5000**

### Method 3: Using the start script
1. Double-click `start_server.bat`
2. A new window will open with the server
3. Go to: **http://localhost:5000**

## 🌌 Features

- **Enter any year** (1970-2100) to predict sunspot numbers
- **Interactive graph** showing data from 1970 to your input year
- **Solar Maximum & Minimum markers** clearly labeled on the graph
- **11-year solar cycle scale** on the x-axis
- **Beautiful space theme** with animated stars

## 📊 Understanding the Graph

- **Gold Stars (★)**: Solar Maximum - Years with highest sunspot activity
- **Cyan Triangles (▼)**: Solar Minimum - Years with lowest sunspot activity
- **Blue line**: Historical data (1970-2024)
- **Pink dashed line**: Predicted data (2025+)
- **Vertical dotted lines**: 11-year solar cycle boundaries

## 🛑 To Stop the Server

Press `Ctrl+C` in the terminal window where the server is running.

## ⚠️ Troubleshooting

**Port 5000 already in use?**
- Close any other applications using port 5000
- Or modify `app.py` line 252 to use a different port (e.g., `port=5001`)

**Server won't start?**
- Make sure Python 3.11 is installed
- Make sure all dependencies are installed: `.venv\Scripts\pip install -r requirements.txt`

**Page not loading?**
- Make sure the server is running (check the terminal window)
- Try refreshing the page
- Check that you're using `http://localhost:5000` (not https)

