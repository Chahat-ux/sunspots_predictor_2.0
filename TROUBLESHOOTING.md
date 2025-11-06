# Troubleshooting Guide

## Page Not Loading? Follow These Steps:

### Step 1: Check if Server is Running
1. Look for a terminal/command window that says "Running on http://127.0.0.1:5000"
2. If you don't see it, double-click `run.bat` to start the server

### Step 2: Verify Server is Running
Open a new PowerShell/Command Prompt and run:
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000 -UseBasicParsing
```
If you see "200 OK", the server is running correctly.

### Step 3: Try Different URLs
Try these URLs in your browser:
- http://localhost:5000
- http://127.0.0.1:5000
- http://0.0.0.0:5000

### Step 4: Check Browser Console
1. Open your browser (Chrome/Firefox/Edge)
2. Press F12 to open Developer Tools
3. Go to the "Console" tab
4. Look for any red error messages
5. Go to the "Network" tab and refresh the page
6. Check if any files failed to load (shown in red)

### Step 5: Clear Browser Cache
1. Press Ctrl+Shift+Delete
2. Select "Cached images and files"
3. Click "Clear data"
4. Refresh the page (Ctrl+F5)

### Step 6: Check Firewall/Antivirus
- Your firewall or antivirus might be blocking port 5000
- Try temporarily disabling them to test

### Step 7: Try a Different Port
If port 5000 is blocked, edit `app.py` line 377:
```python
app.run(host='127.0.0.1', port=5001, debug=True)  # Changed to 5001
```
Then access http://localhost:5001

### Step 8: Check Python Process
Make sure only one Python process is running:
```powershell
Get-Process python
```
If multiple are running, stop them:
```powershell
Stop-Process -Name python -Force
```

### Step 9: Reinstall Dependencies
If nothing works, reinstall dependencies:
```powershell
cd "C:\sun spot 2.0"
.venv\Scripts\pip install --upgrade -r requirements.txt
```

### Step 10: Check for Errors
Look at the terminal window where the server is running. Any error messages will appear there.

## Common Issues:

**Issue: "Connection refused"**
- Solution: Server is not running. Start it with `run.bat`

**Issue: "This site can't be reached"**
- Solution: Check if you're using the correct URL (http://localhost:5000, not https://)

**Issue: Page loads but is blank**
- Solution: Check browser console (F12) for JavaScript errors
- Solution: Try a different browser

**Issue: Fonts not loading**
- Solution: The page will still work, fonts will just use fallback fonts
- Solution: Check your internet connection (fonts load from Google)

**Issue: Graph not showing**
- Solution: Check browser console for errors
- Solution: Make sure matplotlib is installed: `.venv\Scripts\pip install matplotlib`

## Still Not Working?

1. Stop the server (Ctrl+C in the terminal)
2. Delete the `.venv` folder
3. Recreate virtual environment:
   ```powershell
   py -3.11 -m venv .venv
   .venv\Scripts\pip install -r requirements.txt
   ```
4. Start server again: `run.bat`

## Quick Test

Run this to test if everything works:
```powershell
cd "C:\sun spot 2.0"
.venv\Scripts\python test_app.py
```

If all tests pass, the app should work!

