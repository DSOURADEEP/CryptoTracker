#!/usr/bin/env python3
"""
WSGI Entry point for production deployment
"""

import os
import sys
from index import app

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    # For production, use Gunicorn instead of Flask's built-in server
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
