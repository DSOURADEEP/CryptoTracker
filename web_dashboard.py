#!/usr/bin/env python3
"""
Flask Web Dashboard for Crypto Tracker
Simple web interface that works without complex dependencies
"""

import json
import os
from datetime import datetime
import threading
import time
from crypto_tracker import CryptoTracker

# Try to import Flask, if not available, use simple HTTP server
try:
    from flask import Flask, render_template, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import urllib.parse

class CryptoWebDashboard:
    def __init__(self):
        self.tracker = CryptoTracker()
        self.current_prices = {}
        self.last_update = None
        self.update_thread = None
        self.running = False
        
    def update_prices(self):
        """Background thread to update prices"""
        while self.running:
            try:
                self.current_prices = self.tracker.get_current_prices()
                self.last_update = datetime.now()
                time.sleep(60)  # Update every minute
            except Exception as e:
                print(f"Error updating prices: {e}")
                time.sleep(60)
                
    def start_price_updates(self):
        """Start background price updates"""
        self.running = True
        self.update_thread = threading.Thread(target=self.update_prices)
        self.update_thread.daemon = True
        self.update_thread.start()
        
    def stop_price_updates(self):
        """Stop background price updates"""
        self.running = False
        if self.update_thread:
            self.update_thread.join()

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Crypto Tracker Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            backdrop-filter: blur(5px);
        }
        .stat-card h3 {
            margin: 0 0 10px 0;
            font-size: 1.1em;
            opacity: 0.9;
        }
        .stat-card .value {
            font-size: 1.8em;
            font-weight: bold;
            color: #4CAF50;
        }
        .crypto-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .crypto-card {
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(5px);
            transition: transform 0.3s ease;
        }
        .crypto-card:hover {
            transform: translateY(-5px);
        }
        .crypto-name {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            text-transform: capitalize;
        }
        .crypto-price {
            font-size: 1.5em;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 8px;
        }
        .crypto-change {
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .crypto-change.positive {
            color: #4CAF50;
        }
        .crypto-change.negative {
            color: #F44336;
        }
        .crypto-details {
            font-size: 0.9em;
            opacity: 0.8;
        }
        .update-time {
            text-align: center;
            opacity: 0.7;
            margin-top: 20px;
        }
        .refresh-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            margin: 10px;
            transition: background 0.3s ease;
        }
        .refresh-btn:hover {
            background: #45a049;
        }
        .loading {
            text-align: center;
            font-size: 1.2em;
            opacity: 0.7;
            margin: 40px 0;
        }
        .error {
            text-align: center;
            color: #F44336;
            font-size: 1.1em;
            margin: 20px 0;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .loading {
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Crypto Tracker Dashboard</h1>
        
        <div style="text-align: center; margin-bottom: 30px;">
            <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
            <button class="refresh-btn" onclick="toggleAutoRefresh()">⏱️ Auto Refresh</button>
        </div>
        
        <div id="loading" class="loading">Loading cryptocurrency data...</div>
        <div id="error" class="error" style="display: none;"></div>
        
        <div id="stats" class="stats-grid" style="display: none;">
            <div class="stat-card">
                <h3>Total Market Cap</h3>
                <div class="value" id="total-market-cap">$0</div>
            </div>
            <div class="stat-card">
                <h3>Average 24h Change</h3>
                <div class="value" id="avg-change">0%</div>
            </div>
            <div class="stat-card">
                <h3>Tracked Coins</h3>
                <div class="value" id="coin-count">0</div>
            </div>
        </div>
        
        <div id="crypto-container" class="crypto-grid" style="display: none;"></div>
        
        <div class="update-time">
            <p>Last updated: <span id="last-update">Never</span></p>
        </div>
    </div>

    <script>
        let autoRefresh = false;
        let refreshInterval;
        
        function formatNumber(num) {
            if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
            if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
            if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';
            return num.toFixed(2);
        }
        
        function formatCurrency(num) {
            return '$' + num.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        }
        
        function refreshData() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error').style.display = 'none';
            
            fetch('/api/prices')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    updateDisplay(data);
                    document.getElementById('loading').style.display = 'none';
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('error').style.display = 'block';
                    document.getElementById('error').textContent = 'Error loading data: ' + error.message;
                });
        }
        
        function updateDisplay(data) {
            // Update stats
            let totalMarketCap = 0;
            let totalChange = 0;
            let changeCount = 0;
            
            // Update crypto cards
            const container = document.getElementById('crypto-container');
            container.innerHTML = '';
            
            for (const [coin, info] of Object.entries(data.prices)) {
                const card = document.createElement('div');
                card.className = 'crypto-card';
                
                const price = info.usd || 0;
                const change = info.usd_24h_change || 0;
                const marketCap = info.usd_market_cap || 0;
                const volume = info.usd_24h_vol || 0;
                
                totalMarketCap += marketCap;
                totalChange += change;
                changeCount++;
                
                const changeClass = change >= 0 ? 'positive' : 'negative';
                const changeSymbol = change >= 0 ? '+' : '';
                
                card.innerHTML = `
                    <div class="crypto-name">${coin.replace('-', ' ')}</div>
                    <div class="crypto-price">${formatCurrency(price)}</div>
                    <div class="crypto-change ${changeClass}">${changeSymbol}${change.toFixed(2)}%</div>
                    <div class="crypto-details">
                        Market Cap: $${formatNumber(marketCap)}<br>
                        Volume: $${formatNumber(volume)}
                    </div>
                `;
                
                container.appendChild(card);
            }
            
            // Update summary stats
            document.getElementById('total-market-cap').textContent = '$' + formatNumber(totalMarketCap);
            document.getElementById('avg-change').textContent = (totalChange / changeCount).toFixed(2) + '%';
            document.getElementById('coin-count').textContent = Object.keys(data.prices).length;
            
            // Update timestamp
            document.getElementById('last-update').textContent = new Date().toLocaleString();
            
            // Show content
            document.getElementById('stats').style.display = 'grid';
            document.getElementById('crypto-container').style.display = 'grid';
        }
        
        function toggleAutoRefresh() {
            autoRefresh = !autoRefresh;
            const btn = event.target;
            
            if (autoRefresh) {
                btn.textContent = '⏹️ Stop Auto';
                refreshInterval = setInterval(refreshData, 60000); // Refresh every minute
            } else {
                btn.textContent = '⏱️ Auto Refresh';
                clearInterval(refreshInterval);
            }
        }
        
        // Initial load
        refreshData();
    </script>
</body>
</html>
"""

if FLASK_AVAILABLE:
    # Flask-based web server
    app = Flask(__name__)
    dashboard = CryptoWebDashboard()
    
    @app.route('/')
    def index():
        return HTML_TEMPLATE
    
    @app.route('/api/prices')
    def get_prices():
        try:
            if not dashboard.current_prices:
                # Get fresh data if not available
                dashboard.current_prices = dashboard.tracker.get_current_prices()
                dashboard.last_update = datetime.now()
            
            return jsonify({
                'prices': dashboard.current_prices,
                'last_update': dashboard.last_update.isoformat() if dashboard.last_update else None
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def run_flask_dashboard():
        dashboard.start_price_updates()
        print("🌐 Starting Flask Web Dashboard...")
        print("📱 Open http://localhost:5000 in your browser")
        print("Press Ctrl+C to stop")
        try:
            port = int(os.environ.get('PORT', 5000))
            app.run(host='0.0.0.0', port=port, debug=False)
        except KeyboardInterrupt:
            print("\n👋 Stopping web dashboard...")
        finally:
            dashboard.stop_price_updates()

else:
    # Simple HTTP server fallback
    class CryptoHTTPHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(HTML_TEMPLATE.encode())
            elif self.path == '/api/prices':
                try:
                    tracker = CryptoTracker()
                    prices = tracker.get_current_prices()
                    
                    response_data = {
                        'prices': prices,
                        'last_update': datetime.now().isoformat()
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response_data).encode())
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': str(e)}).encode())
            else:
                self.send_response(404)
                self.end_headers()
        
        def log_message(self, format, *args):
            pass  # Suppress log messages
    
    def run_simple_dashboard():
        print("🌐 Starting Simple Web Dashboard...")
        print("📱 Open http://localhost:8000 in your browser")
        print("Press Ctrl+C to stop")
        
        server = HTTPServer(('', 8000), CryptoHTTPHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Stopping web dashboard...")
            server.shutdown()

def main():
    print("🚀 Crypto Tracker Web Dashboard")
    print("=" * 50)
    
    if FLASK_AVAILABLE:
        print("✅ Flask available - Using advanced dashboard")
        run_flask_dashboard()
    else:
        print("⚠️  Flask not available - Using simple dashboard")
        print("💡 Install Flask for better features: pip install flask")
        run_simple_dashboard()

if __name__ == "__main__":
    main()
