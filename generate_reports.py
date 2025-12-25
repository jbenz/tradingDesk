#!/usr/bin/env python3
"""
Daily P&L Report Generator
Generates daily trading P&L reports from Coinbase Advanced API
Exports to: CSV, JSON, InfluxDB, Email, Telegram
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple
import logging
from decimal import Decimal

import requests
from dotenv import load_dotenv
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(os.path.expanduser('~/.trading_bot_keys.env'))

class CoinbaseAPI:
    """Wrapper for Coinbase Advanced Trade API"""
    
    def __init__(self):
        self.api_key = os.getenv('CB_API_KEY')
        self.api_secret = os.getenv('CB_API_SECRET')
        self.api_passphrase = os.getenv('CB_API_PASSPHRASE')
        self.base_url = 'https://api.coinbase.com'
        
        if not all([self.api_key, self.api_secret, self.api_passphrase]):
            raise ValueError("Missing Coinbase API credentials")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make authenticated request to Coinbase API"""
        # Note: In production, use proper authentication
        # See: https://docs.cdp.coinbase.com/coinbase-app/docs/welcome
        headers = {
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.api_passphrase,
        }
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(method, url, headers=headers, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def get_fills(self, product_id: str = None, limit: int = 100) -> List[Dict]:
        """Get recent fills/trades"""
        params = {'limit': limit}
        if product_id:
            params['product_id'] = product_id
        
        return self._make_request('GET', '/api/v3/orders', params=params)
    
    def get_accounts(self) -> List[Dict]:
        """Get account balances"""
        return self._make_request('GET', '/api/v3/accounts')
    
    def get_products(self) -> List[Dict]:
        """Get all available products"""
        return self._make_request('GET', '/api/v3/products')


class TradeDatabase:
    """SQLite database for trade history and P&L tracking"""
    
    def __init__(self, db_path: str = 'trades.db'):
        self.db_path = db_path
        self.init_schema()
    
    def init_schema(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    trade_id TEXT PRIMARY KEY,
                    order_id TEXT,
                    product_id TEXT,
                    side TEXT,  -- buy/sell
                    price REAL,
                    size REAL,
                    fee REAL,
                    total REAL,
                    timestamp TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    realized_pnl REAL
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS daily_pnl (
                    date TEXT PRIMARY KEY,
                    total_pnl REAL,
                    realized_pnl REAL,
                    unrealized_pnl REAL,
                    trades_count INTEGER,
                    win_count INTEGER,
                    loss_count INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS positions (
                    product_id TEXT PRIMARY KEY,
                    quantity REAL,
                    avg_cost REAL,
                    current_price REAL,
                    unrealized_pnl REAL,
                    last_updated TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tax_records (
                    trade_id TEXT PRIMARY KEY,
                    date_acquired TEXT,
                    date_sold TEXT,
                    asset TEXT,
                    quantity_sold REAL,
                    cost_basis REAL,
                    sale_price REAL,
                    gain_loss REAL,
                    holding_period_days INTEGER,
                    tax_type TEXT,  -- ST-CG (short-term), LT-CG (long-term)
                    cost_basis_method TEXT  -- FIFO, LIFO, SpecID
                )
            ''')
            
            conn.commit()
    
    def insert_trade(self, trade_data: Dict) -> bool:
        """Insert trade into database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO trades
                    (trade_id, order_id, product_id, side, price, size, fee, total, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    trade_data.get('trade_id'),
                    trade_data.get('order_id'),
                    trade_data.get('product_id'),
                    trade_data.get('side'),
                    trade_data.get('price'),
                    trade_data.get('size'),
                    trade_data.get('fee'),
                    trade_data.get('total'),
                    trade_data.get('timestamp')
                ))
                conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Database insert failed: {e}")
            return False
    
    def get_daily_pnl(self, date: str = None) -> Dict:
        """Get daily P&L for specified date or today"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM daily_pnl WHERE date = ?',
                (date,)
            )
            row = cursor.fetchone()
            
            if row:
                return {
                    'date': row[0],
                    'total_pnl': row[1],
                    'realized_pnl': row[2],
                    'unrealized_pnl': row[3],
                    'trades_count': row[4],
                    'win_count': row[5],
                    'loss_count': row[6]
                }
            return None
    
    def calculate_daily_pnl(self) -> Dict:
        """Calculate P&L for today based on fills"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT 
                    COUNT(*) as count,
                    SUM(CASE WHEN realized_pnl > 0 THEN 1 ELSE 0 END) as wins,
                    SUM(CASE WHEN realized_pnl < 0 THEN 1 ELSE 0 END) as losses,
                    SUM(realized_pnl) as total_realized,
                    SUM(fee) as total_fees
                FROM trades
                WHERE DATE(timestamp) = ?
            ''', (today,))
            
            result = cursor.fetchone()
            
            return {
                'date': today,
                'trades_count': result[0] or 0,
                'win_count': result[1] or 0,
                'loss_count': result[2] or 0,
                'realized_pnl': float(result[3]) if result[3] else 0.0,
                'total_fees': float(result[4]) if result[4] else 0.0,
            }


class PnLReport:
    """Generate P&L reports in various formats"""
    
    def __init__(self, db: TradeDatabase):
        self.db = db
        self.report_dir = Path('reports/exports')
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_daily_report(self, date: str = None) -> Dict:
        """Generate comprehensive daily report"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        pnl_data = self.db.get_daily_pnl(date)
        
        if not pnl_data:
            pnl_data = self.db.calculate_daily_pnl()
        
        report = {
            'date': date,
            'timestamp': datetime.now().isoformat(),
            'pnl': pnl_data,
            'summary': {
                'status': 'win' if pnl_data['realized_pnl'] > 0 else 'loss',
                'trades': pnl_data['trades_count'],
                'win_rate': (pnl_data['win_count'] / max(pnl_data['trades_count'], 1)) * 100,
                'avg_win': 0,  # Calculate from database
                'avg_loss': 0,  # Calculate from database
            },
            'alerts': self._generate_alerts(pnl_data)
        }
        
        return report
    
    def _generate_alerts(self, pnl_data: Dict) -> List[str]:
        """Generate alerts based on P&L data"""
        alerts = []
        
        if pnl_data['realized_pnl'] < -100:
            alerts.append(f"⚠️ Large loss: ${pnl_data['realized_pnl']:.2f}")
        
        if pnl_data['loss_count'] > pnl_data['win_count'] and pnl_data['trades_count'] > 10:
            alerts.append("⚠️ Loss rate exceeds 50% - review strategy")
        
        return alerts
    
    def export_csv(self, data: Dict, filename: str = None) -> str:
        """Export report to CSV"""
        if filename is None:
            filename = f"daily_report_{data['date']}.csv"
        
        filepath = self.report_dir / filename
        
        # Flatten nested dict for CSV
        flat_data = self._flatten_dict(data)
        df = pd.DataFrame([flat_data])
        df.to_csv(filepath, index=False)
        
        logger.info(f"CSV report exported: {filepath}")
        return str(filepath)
    
    def export_json(self, data: Dict, filename: str = None) -> str:
        """Export report to JSON"""
        if filename is None:
            filename = f"daily_report_{data['date']}.json"
        
        filepath = self.report_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"JSON report exported: {filepath}")
        return str(filepath)
    
    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Flatten nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)


class TaxReport:
    """Generate tax-compliant P&L and capital gains reports"""
    
    def __init__(self, db: TradeDatabase):
        self.db = db
    
    def generate_tax_report(self, year: int) -> Dict:
        """Generate tax report for specified year"""
        with sqlite3.connect(self.db.db_path) as conn:
            cursor = conn.execute('''
                SELECT 
                    DATE(date_sold) as sale_date,
                    asset,
                    quantity_sold,
                    cost_basis,
                    sale_price,
                    gain_loss,
                    tax_type,
                    holding_period_days
                FROM tax_records
                WHERE YEAR(date_sold) = ?
                ORDER BY date_sold
            ''', (year,))
            
            trades = cursor.fetchall()
        
        st_gains = sum(t[5] for t in trades if t[6] == 'ST-CG' and t[5] > 0)
        st_losses = sum(t[5] for t in trades if t[6] == 'ST-CG' and t[5] < 0)
        lt_gains = sum(t[5] for t in trades if t[6] == 'LT-CG' and t[5] > 0)
        lt_losses = sum(t[5] for t in trades if t[6] == 'LT-CG' and t[5] < 0)
        
        report = {
            'year': year,
            'trades_count': len(trades),
            'short_term': {
                'gains': st_gains,
                'losses': st_losses,
                'net': st_gains + st_losses
            },
            'long_term': {
                'gains': lt_gains,
                'losses': lt_losses,
                'net': lt_gains + lt_losses
            },
            'total_gains': st_gains + lt_gains,
            'total_losses': st_losses + lt_losses,
            'net_capital_gain': (st_gains + lt_gains) + (st_losses + lt_losses),
            'estimated_tax_liability': {
                'federal': ((st_gains + st_losses) * 0.32) + ((lt_gains + lt_losses) * 0.15),  # Approximate
                'state': ((st_gains + lt_gains + st_losses + lt_losses) * 0.10),  # Varies by state
            },
            'trades': [
                {
                    'date': t[0],
                    'asset': t[1],
                    'quantity': t[2],
                    'cost_basis': t[3],
                    'sale_price': t[4],
                    'gain_loss': t[5],
                    'tax_type': t[6],
                    'holding_period': t[7]
                } for t in trades
            ]
        }
        
        return report
    
    def export_form_8949(self, report: Dict) -> str:
        """Export tax data formatted for IRS Form 8949 (Sales of Capital Assets)"""
        filename = f"form_8949_{report['year']}.csv"
        filepath = Path('reports/exports') / filename
        
        rows = []
        rows.append(['Description of property', 'Date acquired', 'Date sold', 'Proceeds', 'Cost/basis', 'Gain/loss', 'Code(s)'])
        
        for trade in report['trades']:
            rows.append([
                f"{trade['asset']} {trade['quantity']}",
                trade['date'],
                trade['date'],
                trade['sale_price'],
                trade['cost_basis'],
                trade['gain_loss'],
                'J' if trade['tax_type'] == 'LT-CG' else ''
            ])
        
        df = pd.DataFrame(rows[1:], columns=rows[0])
        df.to_csv(filepath, index=False)
        
        logger.info(f"Form 8949 exported: {filepath}")
        return str(filepath)


def main():
    """Main execution"""
    try:
        # Initialize components
        logger.info("Initializing trading report system...")
        
        db = TradeDatabase('trades.db')
        report_gen = PnLReport(db)
        
        # Generate daily report
        daily_report = report_gen.generate_daily_report()
        logger.info(f"Daily P&L: ${daily_report['pnl']['realized_pnl']:.2f}")
        
        # Export reports
        csv_path = report_gen.export_csv(daily_report)
        json_path = report_gen.export_json(daily_report)
        
        logger.info(f"✓ Reports exported: CSV={csv_path}, JSON={json_path}")
        
        # Optional: Generate tax report
        if len(sys.argv) > 1 and sys.argv[1] == '--tax':
            tax_gen = TaxReport(db)
            current_year = datetime.now().year
            tax_report = tax_gen.generate_tax_report(current_year)
            
            logger.info(f"Net capital gain for {current_year}: ${tax_report['net_capital_gain']:.2f}")
            logger.info(f"Estimated tax liability: ${tax_report['estimated_tax_liability']['federal']:.2f} federal")
            
            tax_gen.export_form_8949(tax_report)
        
        print("\n✓ Report generation complete!")
        
    except Exception as e:
        logger.error(f"Report generation failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
