# Deployment Guide

## Local Development

The application runs locally on `http://localhost:5000` by default.

## Deploying to Production

### Option 1: Deploy to Heroku

1. **Install Heroku CLI:**
   ```bash
   winget install --id Heroku.HerokuCLI
   ```

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku App:**
   ```bash
   heroku create sunspot-predictor
   ```

4. **Set Buildpacks:**
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-git-lfs.git
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

### Option 2: Deploy to PythonAnywhere

1. Sign up at https://www.pythonanywhere.com
2. Upload files via Files tab
3. Configure web app:
   - Source code: `/home/yourusername/sunspots_predictor_2.0`
   - WSGI file: Point to `app.py`
   - Static files: Map `/static` to `static/` folder

### Option 3: Deploy to Railway

1. Sign up at https://railway.app
2. Connect GitHub repository
3. Railway will auto-detect Flask app
4. Add environment variables if needed

### Option 4: Deploy to Render

1. Sign up at https://render.com
2. Connect GitHub repository
3. Select "Web Service"
4. Build command: `pip install -r requirements.txt`
5. Start command: `python app.py`

## Environment Variables

Create a `.env` file (not committed to git) for production:

```env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
```

## Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use production WSGI server (gunicorn, waitress)
- [ ] Set up proper logging
- [ ] Configure CORS if needed
- [ ] Set up SSL/HTTPS
- [ ] Configure domain name
- [ ] Set up monitoring/analytics

## Using Gunicorn (Production Server)

Install gunicorn:
```bash
pip install gunicorn
```

Create `Procfile`:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4
```

Run:
```bash
gunicorn app:app --bind 0.0.0.0:5000
```

## Using Waitress (Windows-friendly)

Install waitress:
```bash
pip install waitress
```

Update `app.py`:
```python
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
```

