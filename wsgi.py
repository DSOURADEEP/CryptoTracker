#!/usr/bin/env python3
"""
WSGI Entry point for production deployment
"""

import os
import sys
from web_dashboard import app, dashboard

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Start background price updates
dashboard.start_price_updates()

if __name__ == "__main__":
    # For production, use Gunicorn instead of Flask's built-in server
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
