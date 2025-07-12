#!/usr/bin/env python3
"""
Main Landing Page for Crypto Tracker
Provides interface selection menu like run.py but for web
"""

from flask import Flask, render_template_string, redirect, url_for
import os

app = Flask(__name__)

# Main landing page HTML template
LANDING_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Crypto Tracker - Choose Your Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            width: 90%;
            text-align: center;
        }
        
        .header {
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .interface-grid {
            display: grid;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .interface-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 30px;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 2px solid transparent;
            text-decoration: none;
            color: white;
            display: block;
        }
        
        .interface-card:hover {
            transform: translateY(-5px);
            border-color: rgba(255, 255, 255, 0.5);
            background: rgba(255, 255, 255, 0.2);
            text-decoration: none;
            color: white;
        }
        
        .interface-icon {
            font-size: 3em;
            margin-bottom: 15px;
            display: block;
        }
        
        .interface-title {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .interface-description {
            opacity: 0.8;
            line-height: 1.4;
        }
        
        .features {
            margin-top: 40px;
            opacity: 0.7;
        }
        
        .features h3 {
            margin-bottom: 15px;
        }
        
        .feature-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            text-align: left;
        }
        
        .feature-item {
            padding: 5px 0;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .interface-card {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Crypto Tracker</h1>
            <p>Professional cryptocurrency tracking with real-time updates</p>
            <p><strong>Choose your preferred interface:</strong></p>
        </div>
        
        <div class="interface-grid">
            <a href="/dashboard" class="interface-card">
                <div class="interface-icon">🌐</div>
                <div class="interface-title">Web Dashboard</div>
                <div class="interface-description">
                    Beautiful web interface with real-time updates, interactive charts, 
                    and portfolio analysis. Perfect for desktop and mobile.
                </div>
            </a>
            
            <a href="/streamlit" class="interface-card">
                <div class="interface-icon">📊</div>
                <div class="interface-title">Advanced Analytics</div>
                <div class="interface-description">
                    Streamlit-powered dashboard with advanced technical indicators, 
                    detailed charts, and comprehensive market analysis.
                </div>
            </a>
            
            <a href="/api" class="interface-card">
                <div class="interface-icon">🔌</div>
                <div class="interface-title">API Endpoint</div>
                <div class="interface-description">
                    JSON API for developers. Get real-time crypto data programmatically 
                    for your applications and integrations.
                </div>
            </a>
        </div>
        
        <div class="features">
            <h3>✨ Features</h3>
            <div class="feature-list">
                <div class="feature-item">📈 10+ Cryptocurrencies</div>
                <div class="feature-item">⚡ Real-time Updates</div>
                <div class="feature-item">📱 Mobile Responsive</div>
                <div class="feature-item">🔒 Secure HTTPS</div>
                <div class="feature-item">🌍 Global Access</div>
                <div class="feature-item">💰 Market Analysis</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def landing_page():
    """Main landing page with interface selection"""
    return render_template_string(LANDING_PAGE_HTML)

@app.route('/dashboard')
def web_dashboard():
    """Redirect to the main web dashboard"""
    # Import and run the web dashboard
    from web_dashboard import HTML_TEMPLATE, dashboard, get_prices
    
    # Start price updates if not already running
    if not dashboard.running:
        dashboard.start_price_updates()
    
    return HTML_TEMPLATE

@app.route('/api/prices')
def api_prices():
    """API endpoint for crypto prices"""
    from web_dashboard import get_prices
    return get_prices()

@app.route('/streamlit')
def streamlit_info():
    """Information about Streamlit dashboard"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Streamlit Dashboard</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                text-align: center; 
                padding: 50px; 
            }
            .container { 
                background: rgba(255,255,255,0.1); 
                padding: 40px; 
                border-radius: 15px; 
                max-width: 600px; 
                margin: 0 auto; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Advanced Analytics Dashboard</h1>
            <p>The Streamlit dashboard provides advanced technical analysis with:</p>
            <ul style="text-align: left; margin: 20px 0;">
                <li>📈 Technical indicators (RSI, MACD, Bollinger Bands)</li>
                <li>📊 Interactive charts with zoom and pan</li>
                <li>🔍 Detailed market analysis</li>
                <li>📱 Real-time data visualization</li>
            </ul>
            <p><strong>Note:</strong> This requires additional setup for Streamlit deployment.</p>
            <a href="/" style="color: #4CAF50; text-decoration: none; font-weight: bold;">← Back to Main Menu</a>
        </div>
    </body>
    </html>
    """)

@app.route('/api')
def api_info():
    """API documentation page"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crypto Tracker API</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 20px; 
            }
            .container { 
                background: rgba(255,255,255,0.1); 
                padding: 40px; 
                border-radius: 15px; 
                max-width: 800px; 
                margin: 0 auto; 
            }
            code { 
                background: rgba(0,0,0,0.3); 
                padding: 10px; 
                border-radius: 5px; 
                display: block; 
                margin: 10px 0; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔌 Crypto Tracker API</h1>
            <h2>Endpoints:</h2>
            
            <h3>GET /api/prices</h3>
            <p>Returns real-time cryptocurrency prices</p>
            <code>
{
  "prices": {
    "bitcoin": {
      "usd": 117483.00,
      "usd_24h_change": -0.41,
      "usd_market_cap": 2337242612,
      "usd_24h_vol": 34842426957
    },
    ...
  },
  "last_update": "2025-07-12T15:00:00Z"
}
            </code>
            
            <h3>Usage Example:</h3>
            <code>
curl {{ request.url_root }}api/prices
            </code>
            
            <a href="/" style="color: #4CAF50; text-decoration: none; font-weight: bold;">← Back to Main Menu</a>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
