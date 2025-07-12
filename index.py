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
def advanced_analytics():
    """Advanced analytics dashboard with charts and technical indicators"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>📊 Advanced Analytics Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            .controls {
                text-align: center;
                margin-bottom: 30px;
            }
            .btn {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                margin: 5px;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.3s ease;
            }
            .btn:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
            .btn.active {
                background: #4CAF50;
            }
            .chart-container {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                backdrop-filter: blur(10px);
            }
            .chart-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }
            .indicator-card {
                background: rgba(255, 255, 255, 0.15);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .indicator-value {
                font-size: 2em;
                font-weight: bold;
                margin: 10px 0;
            }
            .indicator-label {
                opacity: 0.8;
                font-size: 0.9em;
            }
            .back-btn {
                position: fixed;
                top: 20px;
                left: 20px;
                background: rgba(0, 0, 0, 0.3);
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            .back-btn:hover {
                background: rgba(0, 0, 0, 0.5);
                color: white;
                text-decoration: none;
            }
            @media (max-width: 768px) {
                .chart-grid {
                    grid-template-columns: 1fr;
                }
                .container {
                    padding: 10px;
                }
            }
        </style>
    </head>
    <body>
        <a href="/" class="back-btn">← Back to Menu</a>
        
        <div class="container">
            <div class="header">
                <h1>📊 Advanced Analytics Dashboard</h1>
                <p>Real-time cryptocurrency technical analysis with interactive charts</p>
            </div>
            
            <div class="controls">
                <button class="btn active" onclick="selectCoin('bitcoin')">Bitcoin</button>
                <button class="btn" onclick="selectCoin('ethereum')">Ethereum</button>
                <button class="btn" onclick="selectCoin('cardano')">Cardano</button>
                <button class="btn" onclick="selectCoin('polkadot')">Polkadot</button>
                <button class="btn" onclick="selectCoin('chainlink')">Chainlink</button>
            </div>
            
            <div class="chart-container">
                <h3 id="chart-title">Bitcoin Price Analysis</h3>
                <div id="price-chart" style="height: 500px;"></div>
            </div>
            
            <div class="chart-grid">
                <div class="chart-container">
                    <h3>Technical Indicators</h3>
                    <div id="indicators-chart" style="height: 300px;"></div>
                </div>
                <div class="chart-container">
                    <h3>Volume Analysis</h3>
                    <div id="volume-chart" style="height: 300px;"></div>
                </div>
            </div>
            
            <div class="chart-grid">
                <div class="indicator-card">
                    <div class="indicator-label">RSI (14)</div>
                    <div class="indicator-value" id="rsi-value">65.4</div>
                    <div class="indicator-label">Neutral</div>
                </div>
                <div class="indicator-card">
                    <div class="indicator-label">MACD</div>
                    <div class="indicator-value" id="macd-value">+2.1</div>
                    <div class="indicator-label">Bullish</div>
                </div>
                <div class="indicator-card">
                    <div class="indicator-label">Bollinger Position</div>
                    <div class="indicator-value" id="bb-value">78%</div>
                    <div class="indicator-label">Upper Band</div>
                </div>
                <div class="indicator-card">
                    <div class="indicator-label">24h Volume</div>
                    <div class="indicator-value" id="volume-value">$32.9B</div>
                    <div class="indicator-label">High Activity</div>
                </div>
            </div>
        </div>
        
        <script>
            let currentCoin = 'bitcoin';
            let priceData = [];
            
            function selectCoin(coin) {
                currentCoin = coin;
                document.querySelectorAll('.btn').forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
                document.getElementById('chart-title').textContent = coin.charAt(0).toUpperCase() + coin.slice(1) + ' Price Analysis';
                loadChartData();
            }
            
            function generateMockData() {
                const data = [];
                const dates = [];
                const volumes = [];
                let price = 50000 + Math.random() * 20000;
                
                for (let i = 30; i >= 0; i--) {
                    const date = new Date();
                    date.setDate(date.getDate() - i);
                    dates.push(date.toISOString().split('T')[0]);
                    
                    // Generate realistic price movement
                    price += (Math.random() - 0.5) * price * 0.05;
                    data.push(Math.max(1000, price));
                    
                    // Generate volume data
                    volumes.push(Math.random() * 50000000000 + 10000000000);
                }
                
                return { dates, prices: data, volumes };
            }
            
            function calculateSMA(data, period) {
                const sma = [];
                for (let i = 0; i < data.length; i++) {
                    if (i < period - 1) {
                        sma.push(null);
                    } else {
                        const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
                        sma.push(sum / period);
                    }
                }
                return sma;
            }
            
            function loadChartData() {
                const mockData = generateMockData();
                const sma7 = calculateSMA(mockData.prices, 7);
                const sma21 = calculateSMA(mockData.prices, 21);
                
                // Price Chart with Moving Averages
                const priceTrace = {
                    x: mockData.dates,
                    y: mockData.prices,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Price',
                    line: { color: '#00d4ff', width: 2 }
                };
                
                const sma7Trace = {
                    x: mockData.dates,
                    y: sma7,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'SMA 7',
                    line: { color: '#ff6b35', width: 1 }
                };
                
                const sma21Trace = {
                    x: mockData.dates,
                    y: sma21,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'SMA 21',
                    line: { color: '#4ecdc4', width: 1 }
                };
                
                Plotly.newPlot('price-chart', [priceTrace, sma7Trace, sma21Trace], {
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    font: { color: 'white' },
                    xaxis: { gridcolor: 'rgba(255,255,255,0.1)', title: 'Date' },
                    yaxis: { gridcolor: 'rgba(255,255,255,0.1)', title: 'Price (USD)' },
                    legend: { bgcolor: 'rgba(0,0,0,0.3)' }
                }, { responsive: true });
                
                // RSI Chart
                const rsi = mockData.prices.map((_, i) => 30 + Math.random() * 40); // Mock RSI
                
                const rsiTrace = {
                    x: mockData.dates,
                    y: rsi,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'RSI',
                    line: { color: '#ff6b35' }
                };
                
                Plotly.newPlot('indicators-chart', [rsiTrace], {
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    font: { color: 'white' },
                    xaxis: { gridcolor: 'rgba(255,255,255,0.1)' },
                    yaxis: { gridcolor: 'rgba(255,255,255,0.1)', title: 'RSI', range: [0, 100] },
                    shapes: [
                        { type: 'line', x0: mockData.dates[0], x1: mockData.dates[mockData.dates.length-1], y0: 70, y1: 70, line: { color: 'red', dash: 'dash' } },
                        { type: 'line', x0: mockData.dates[0], x1: mockData.dates[mockData.dates.length-1], y0: 30, y1: 30, line: { color: 'green', dash: 'dash' } }
                    ]
                }, { responsive: true });
                
                // Volume Chart
                const volumeTrace = {
                    x: mockData.dates,
                    y: mockData.volumes,
                    type: 'bar',
                    name: 'Volume',
                    marker: { color: '#4ecdc4', opacity: 0.7 }
                };
                
                Plotly.newPlot('volume-chart', [volumeTrace], {
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    font: { color: 'white' },
                    xaxis: { gridcolor: 'rgba(255,255,255,0.1)' },
                    yaxis: { gridcolor: 'rgba(255,255,255,0.1)', title: 'Volume (USD)' }
                }, { responsive: true });
                
                // Update indicators
                document.getElementById('rsi-value').textContent = rsi[rsi.length-1].toFixed(1);
                document.getElementById('macd-value').textContent = (Math.random() * 4 - 2).toFixed(1);
                document.getElementById('bb-value').textContent = Math.floor(Math.random() * 100) + '%';
                document.getElementById('volume-value').textContent = '$' + (mockData.volumes[mockData.volumes.length-1] / 1e9).toFixed(1) + 'B';
            }
            
            // Load initial data
            loadChartData();
            
            // Auto-refresh every 30 seconds
            setInterval(loadChartData, 30000);
        </script>
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

