#!/usr/bin/env python
# Simple startup script with error handling
import sys
import os

# Set encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

try:
    print("=" * 60)
    print("Starting Sunspot Prediction Web Application")
    print("=" * 60)
    print("\nLoading application...")
    
    from app import app
    
    print("\n[SUCCESS] Application loaded successfully!")
    print("\n" + "=" * 60)
    print("Server starting on http://localhost:5000")
    print("Open your browser and navigate to: http://localhost:5000")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\nServer stopped by user.")
    sys.exit(0)
except Exception as e:
    print(f"\n[ERROR] Failed to start server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

