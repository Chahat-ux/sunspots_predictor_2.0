"""
Netlify serverless function wrapper for Flask app
This file needs to be in netlify/functions/ directory
"""
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Import the main app
from app import app

# Netlify serverless function handler
def handler(event, context):
    """
    Netlify serverless function handler
    Converts Netlify event to WSGI request
    """
    from serverless_wsgi import handle_request
    return handle_request(app, event, context)

# For local testing
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
