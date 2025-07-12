#!/usr/bin/env python3
"""
Crypto Tracker - Real-time cryptocurrency price tracker with graphical analysis
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
# import yfinance as yf  # Optional - not needed for basic functionality

console = Console()

class CryptoTracker:
    def __init__(self):
        self.api_base = "https://api.coingecko.com/api/v3"
        self.prices = {}
        self.historical_data = {}
        self.supported_coins = [
            'bitcoin', 'ethereum', 'cardano', 'polkadot', 'chainlink',
            'litecoin', 'bitcoin-cash', 'stellar', 'dogecoin', 'polygon'
        ]
        
    def get_current_prices(self, coins: List[str] = None) -> Dict:
        """Fetch current prices for specified cryptocurrencies"""
        if coins is None:
            coins = self.supported_coins
            
        try:
            coins_str = ','.join(coins)
            url = f"{self.api_base}/simple/price"
            params = {
                'ids': coins_str,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.prices = data
            return data
            
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error fetching prices: {e}[/red]")
            return {}
    
    def get_historical_data(self, coin: str, days: int = 30) -> pd.DataFrame:
        """Fetch historical price data for a cryptocurrency"""
        try:
            url = f"{self.api_base}/coins/{coin}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily' if days > 1 else 'hourly'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Convert to DataFrame
            prices = data['prices']
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Add volume and market cap if available
            if 'total_volumes' in data:
                volumes = data['total_volumes']
                vol_df = pd.DataFrame(volumes, columns=['timestamp', 'volume'])
                vol_df['timestamp'] = pd.to_datetime(vol_df['timestamp'], unit='ms')
                vol_df.set_index('timestamp', inplace=True)
                df = df.join(vol_df)
            
            self.historical_data[coin] = df
            return df
            
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error fetching historical data for {coin}: {e}[/red]")
            return pd.DataFrame()
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators for price analysis"""
        if df.empty:
            return df
            
        # Simple Moving Averages
        df['SMA_7'] = df['price'].rolling(window=7).mean()
        df['SMA_14'] = df['price'].rolling(window=14).mean()
        df['SMA_30'] = df['price'].rolling(window=30).mean()
        
        # Exponential Moving Average
        df['EMA_12'] = df['price'].ewm(span=12).mean()
        df['EMA_26'] = df['price'].ewm(span=26).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        
        # RSI
        delta = df['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_Middle'] = df['price'].rolling(window=20).mean()
        bb_std = df['price'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        return df
    
    def create_price_chart(self, coin: str, days: int = 30) -> go.Figure:
        """Create an interactive price chart with technical indicators"""
        df = self.get_historical_data(coin, days)
        if df.empty:
            return go.Figure()
            
        df = self.calculate_technical_indicators(df)
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(f'{coin.upper()} Price Chart', 'Volume', 'RSI'),
            vertical_spacing=0.1,
            row_heights=[0.6, 0.2, 0.2]
        )
        
        # Price chart with Bollinger Bands
        fig.add_trace(
            go.Scatter(x=df.index, y=df['price'], name='Price', line=dict(color='blue')),
            row=1, col=1
        )
        
        if 'BB_Upper' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper', line=dict(color='red', dash='dash')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower', line=dict(color='red', dash='dash')),
                row=1, col=1
            )
        
        # Moving averages
        if 'SMA_7' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['SMA_7'], name='SMA 7', line=dict(color='orange')),
                row=1, col=1
            )
        
        if 'SMA_30' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['SMA_30'], name='SMA 30', line=dict(color='green')),
                row=1, col=1
            )
        
        # Volume
        if 'volume' in df.columns:
            fig.add_trace(
                go.Bar(x=df.index, y=df['volume'], name='Volume', marker_color='lightblue'),
                row=2, col=1
            )
        
        # RSI
        if 'RSI' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple')),
                row=3, col=1
            )
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
        
        fig.update_layout(
            title=f'{coin.upper()} Technical Analysis',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            height=800,
            showlegend=True
        )
        
        return fig
    
    def create_portfolio_chart(self, coins: List[str] = None) -> go.Figure:
        """Create a portfolio overview chart"""
        if coins is None:
            coins = self.supported_coins[:5]  # Top 5 coins
            
        prices = self.get_current_prices(coins)
        if not prices:
            return go.Figure()
        
        # Extract data for pie chart
        labels = []
        values = []
        colors = []
        
        for coin, data in prices.items():
            if 'usd_market_cap' in data:
                labels.append(coin.replace('-', ' ').title())
                values.append(data['usd_market_cap'])
                
        # Create pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        fig.update_layout(
            title="Cryptocurrency Market Cap Distribution",
            annotations=[dict(text='Market Cap', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        return fig
    
    def display_live_prices(self):
        """Display live prices in a formatted table"""
        def create_table():
            table = Table(title="🚀 Live Cryptocurrency Prices", show_header=True, header_style="bold magenta")
            table.add_column("Coin", style="cyan", width=12)
            table.add_column("Price (USD)", style="green", width=15)
            table.add_column("24h Change", style="yellow", width=12)
            table.add_column("Market Cap", style="blue", width=15)
            table.add_column("Volume", style="red", width=15)
            
            prices = self.get_current_prices()
            for coin, data in prices.items():
                price = f"${data.get('usd', 0):,.2f}"
                change_24h = data.get('usd_24h_change', 0)
                change_color = "green" if change_24h >= 0 else "red"
                change_str = f"[{change_color}]{change_24h:+.2f}%[/{change_color}]"
                
                market_cap = data.get('usd_market_cap', 0)
                market_cap_str = f"${market_cap:,.0f}" if market_cap else "N/A"
                
                volume = data.get('usd_24h_vol', 0)
                volume_str = f"${volume:,.0f}" if volume else "N/A"
                
                table.add_row(
                    coin.replace('-', ' ').title(),
                    price,
                    change_str,
                    market_cap_str,
                    volume_str
                )
            
            return table
        
        return create_table()
    
    def save_chart(self, fig: go.Figure, filename: str):
        """Save chart as HTML file"""
        fig.write_html(f"{filename}.html")
        console.print(f"[green]Chart saved as {filename}.html[/green]")
    
    def run_live_tracker(self, update_interval: int = 30):
        """Run the live price tracker"""
        console.print("[bold blue]Starting Crypto Tracker...[/bold blue]")
        console.print(f"[yellow]Updating every {update_interval} seconds[/yellow]")
        console.print("[dim]Press Ctrl+C to stop[/dim]")
        
        try:
            while True:
                with Live(self.display_live_prices(), refresh_per_second=1) as live:
                    time.sleep(update_interval)
        except KeyboardInterrupt:
            console.print("\n[red]Stopping tracker...[/red]")

def main():
    tracker = CryptoTracker()
    
    console.print("[bold green]🚀 Crypto Tracker Initialized![/bold green]")
    console.print("\n[yellow]Available commands:[/yellow]")
    console.print("1. [cyan]live[/cyan] - Start live price tracking")
    console.print("2. [cyan]chart <coin>[/cyan] - Generate technical analysis chart")
    console.print("3. [cyan]portfolio[/cyan] - Show portfolio overview")
    console.print("4. [cyan]prices[/cyan] - Show current prices once")
    console.print("5. [cyan]quit[/cyan] - Exit the application")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "live":
                tracker.run_live_tracker()
            elif command.startswith("chart"):
                parts = command.split()
                coin = parts[1] if len(parts) > 1 else "bitcoin"
                console.print(f"[blue]Generating chart for {coin}...[/blue]")
                fig = tracker.create_price_chart(coin)
                if fig.data:
                    tracker.save_chart(fig, f"{coin}_chart")
                else:
                    console.print(f"[red]Could not generate chart for {coin}[/red]")
            elif command == "portfolio":
                console.print("[blue]Generating portfolio overview...[/blue]")
                fig = tracker.create_portfolio_chart()
                if fig.data:
                    tracker.save_chart(fig, "portfolio_overview")
                else:
                    console.print("[red]Could not generate portfolio chart[/red]")
            elif command == "prices":
                table = tracker.display_live_prices()
                console.print(table)
            elif command == "quit":
                console.print("[green]Goodbye![/green]")
                break
            else:
                console.print("[red]Unknown command. Try 'live', 'chart <coin>', 'portfolio', 'prices', or 'quit'[/red]")
                
        except KeyboardInterrupt:
            console.print("\n[green]Goodbye![/green]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()
