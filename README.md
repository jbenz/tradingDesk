```
 ┌────────┐
 │ B-Unit │
 └────────┘

  tradingDesk, an open source crypto trading desk solution with reporting and analytics
  and a 7 day jump start plan to get you going in under 2 hours a day.

```
# tradingDesk - a Crypto Trading Bot Ecosystem for Debian

**Open-source, self-hosted trading infrastructure for Coinbase Advanced API**
Includes an install script, getting started guide, 7 day learning plan to get you up and running using the tools included in this package, reporting functionality, P&L management strategies and suggestions, security considerations and best practices, and an all around good open source time. 

> [!NOTE]
> Please take note that I am not a financial advisor, none of this constitutes financial advice, you are always encouraged to do your own research, use testing platforms and testing api's whenever possible, and to make sure you never reveal your api keys, wallet keys or seed phrases, and cex/dex login information or two factor codes. It is advisable to use hardware security keys and hardware wallets whenever real assets are being utilized in executing trades. It is also highly advisable to limit API key usage with limited lifespans (as short as possible without causing nuisances to your workflow), exercising key rotations at monthly or quarterly intervals and during marketing closing hours or in coordination with scheduled maintenance of the exchanges and trading platforms you plan to integrate with. It is also highly advisable to use IP whitelisting to restrict access to APIs on your various accounts and for you to execute and run this suite of solutions behind a hardened firewall, enabling geoip restrictions to maximize protection to your systems, and consider using a static ip via a VPS server, a self-hosted or personal vpn server that is not shared with other users, and allows you to have fine granular control over the use of trading platforms involving your personal capital and crypto. 

# Cheers, and trade on 🚀 🎡 ₿       [@jbenz](https://github.com/jbenz/tradingDesk)

***

## 📦 What's Included

This complete package includes everything you need to run professional-grade trading bots on your own hardware:

### Bots
- **[nav_link:Freqtrade]** - DCA, Grid, Moving Average strategies (Spot/Futures)
- **[nav_link:Passivbot]** - Perpetual futures grid trading with leverage
- **[nav_link:Barbotine]** - Cross-exchange arbitrage (0 directional risk)

### Infrastructure
- **Grafana** - Real-time trading dashboards
- **InfluxDB** - Time-series metrics database
- **PostgreSQL** - Trade history & analytics
- **Redis** - Fast caching & message queue
- **Docker** - All services containerized

### Reporting & Analytics
- **Daily P&L Reports** - CSV, JSON, automated email
- **Tax Compliance** - IRS Form 8949, capital gains tracking
- **Trade Analysis** - Win rate, Sharpe ratio, drawdown metrics
- **Alert System** - Email/Telegram notifications

### Learning Materials
- **7-Day Setup Guide** - Day-by-day learning path
- **Risk Management** - Position sizing, stop-loss, drawdown limits
- **API Integration** - Coinbase Advanced Trade API examples
- **Troubleshooting** - Common issues & solutions

---

## 🚀 Quick Start

### 1. Installation (5 minutes)
```bash
bash install.sh
```

This automated script:
- Installs Python 3.11/3.12, Git, Docker
- Clones all bot repositories
- Sets up virtual environments
- Creates configuration templates
- Initializes databases

### 2. Configuration (10 minutes)
```bash
# Add your Coinbase API keys
nano ~/.trading_bot_keys.env

# Fill in:
# CB_API_KEY=your_key_id
# CB_API_SECRET=your_secret
# CB_API_PASSPHRASE=your_passphrase
```

### 3. Start Services (2 minutes)
```bash
# Start all Docker containers
docker-compose up -d

# Access dashboards:
# Grafana: http://localhost:3000 (admin/admin)
# Freqtrade: http://localhost:8080
```

### 4. First Trade (30 minutes)
```bash
# Configure Freqtrade with DCA strategy
cd ~/trading-bots/freqtrade
freqtrade new-config --config user_data/config.json

# Test with dry run (no real money)
freqtrade trade --config user_data/config.json

# After verification, enable live trading
# (Follow LEARNING_PATH.md Day 7)
```

---

## 📋 File Structure

```
trading-bot-ecosystem/
├── install.sh                    # Automated setup script
├── docker-compose.yml            # All services (Grafana, InfluxDB, etc)
├── DEPLOYMENT_GUIDE.md           # Complete deployment guide
├── LEARNING_PATH.md              # 7-day learning path
├── README.md                     # This file
│
├── scripts/                      # Utility scripts
│   ├── test_api_connection.py   # Verify Coinbase API
│   ├── check_balance.py         # Show account balances
│   ├── check_alerts.py          # Check for trading alerts
│   └── emergency_stop.sh        # Stop all bots immediately
│
├── reports/                      # P&L & tax reporting
│   ├── generate_reports.py      # Daily P&L report generator
│   ├── generate_tax_report.py   # Tax compliance reports
│   ├── weekly_summary.py        # Weekly performance summary
│   └── Dockerfile               # Container for reports API
│
├── freqtrade/                   # DCA, Grid, MA strategies
│   ├── user_data/
│   │   ├── config.json          # Main configuration
│   │   ├── strategies/          # Strategy files (modify here)
│   │   └── backtest_results/    # Backtest history
│   └── logs/
│
├── passivbot/                   # Perpetual futures
│   ├── configs/
│   │   ├── default.json         # Default config
│   │   ├── coinbase_grid.json   # Grid trading config
│   │   └── coinbase_dca.json    # DCA config
│   ├── backtest_results/
│   └── logs/
│
├── barbotine/                   # Arbitrage bot
│   ├── exchange_config.py       # Exchange API configs
│   ├── main.py                  # Entry point
│   └── logs/
│
├── grafana/                     # Dashboard configs
│   └── provisioning/
│       ├── dashboards/          # Pre-built dashboards
│       └── datasources/         # Data source configs
│
├── nginx/                       # Reverse proxy
│   ├── nginx.conf              # Web server config
│   └── ssl/                    # HTTPS certificates
│
└── config/
    ├── api_keys.example.json   # Example config (customize this)
    └── .env.example            # Environment variables template
```

---

## 🎯 Common Commands

### Bot Management
```bash
# Start all bots
~/trading-bots/start_all.sh

# Stop all bots
docker-compose down

# View logs
docker-compose logs -f freqtrade

# See running processes
tmux list-sessions
```

### Monitoring & Reports
```bash
# Generate daily P&L report
python3 reports/generate_reports.py

# Generate tax report for 2025
python3 reports/generate_reports.py --tax --year 2025

# Check account balance
python3 scripts/check_balance.py

# Monitor daily loss limit
python3 scripts/check_alerts.py
```

### Configuration
```bash
# Freqtrade interactive setup
cd ~/trading-bots/freqtrade && ./setup.sh -c

# Passivbot config edit
nano ~/trading-bots/passivbot/configs/coinbase_grid.json

# Barbotine exchange setup
nano ~/trading-bots/barbotine/exchange_config.py
```

### Backtesting
```bash
# Backtest Freqtrade strategy (last 6 months)
freqtrade backtest --config user_data/config.json \
  --timerange 20240701-20241220

# Backtest Passivbot strategy
python3 ~/trading-bots/passivbot/backtest.py \
  -c configs/coinbase_grid.json \
  --start-date 2024-07-01 --end-date 2024-12-20
```

---

> [!WARNING]
> ## ⚠️ Risk Management Essentials

### Before Running Real Money:

### 1. **Position Sizing** 
   - Never risk >2% of account per trade
   - Formula: Position = (Account × Risk%) / Stop-Loss%
   - Example: $10k account × 1% risk / 5% stop = $200 position

### 2. **Stop-Loss Orders**
   - ALWAYS set stop-loss before entering trade
   - Recommended: 2-5% below entry (spot), 1-3% (futures)
   - Use exchange-level orders (safer than bot software)

### 3. **Daily Loss Limits**
   - If daily loss > 5%, reduce position size by 50%
   - If daily loss > 10%, stop bot and review strategy
   - Set automatic kill-switch at 10% daily loss

### 4. **Leverage Guidelines**
   - Spot trading: 1x (no leverage, safest)
   - Margin trading: 2-3x max (experienced traders only)
   - Perpetual futures: 2-5x (very risky)
   - Never use 10x+ leverage unless you know exactly what you're doing

### 5. **Drawdown Expectations**
   - Good strategies have 30-50% peak-to-trough drawdowns
   - Expect losing streaks of 5-10+ consecutive trades
   - DON'T modify strategy after 2-3 bad trades

### Daily Checklist
```bash
chmod +x ~/trading-bots/daily_checklist.sh
~/trading-bots/daily_checklist.sh

# Should verify:
✓ All bots running
✓ Daily P&L calculated
✓ No alerts triggered
✓ Stop-losses in place
✓ Sufficient balance
```

---

> [!WARNING]
> # 🔐 Security Best Practices

### API Key Safety
```bash
# ✓ DO:
- Use separate read-only key for monitoring
- Restrict IP addresses on Coinbase
- Enable 2FA on Coinbase account
- Store keys in ~/.trading_bot_keys.env (chmod 600)
- Rotate keys every 90 days

# ✗ DON'T:
- Hardcode API keys in config files
- Share keys in chat/email
- Use withdrawal permissions
- Store on GitHub/public repos
- Enable API key emails/SMS
```

### Data Backups
```bash
# Backup daily
tar -czf ~/backups/trades_$(date +%Y%m%d).tar.gz \
  ~/trading-bots/reports/exports \
  ~/.trading_bot_keys.env

# Store offsite (Google Drive, S3, etc)
```

### Network Security
```bash
# Use VPN if on public WiFi
# Firewall: Only allow local/VPN access to ports 3000, 8080, 5000
# SSL/TLS: Use HTTPS (Nginx container handles this)
```

---

## 📊 Supported Exchanges & Strategies

### Exchanges
- **Coinbase** (Advanced API) ✓ Full support
- **Binance** (Optional, for arbitrage)
- **Bybit** (Passivbot native)
- **OKX** (Passivbot native)
- **Kucoin** (Passivbot native)

### Freqtrade Strategies
- DCA (Dollar-Cost Averaging) ✓ Beginner-friendly
- Grid Trading ✓ Sideways markets
- SMA Crossover ✓ Trending markets
- RSI Mean Reversion ✓ Volatile assets
- Bollinger Bands ✓ Breakout trading
- Custom Python strategies ✓ Advanced

### Passivbot Strategies
- Grid Trading ✓ All market conditions
- DCA ✓ Accumulation
- Momentum ✓ Trending
- Custom Rust strategies ✓ High performance

### Barbotine Strategies
- Triangular Arbitrage ✓ 3-leg triangle trades
- Exchange Arbitrage ✓ Price differences
- Dual-exchange ✓ Any pair combination

---

## 🐛 Troubleshooting

### Installation Issues

**Python version not found**
```bash
# Check available versions
python3.11 --version
python3.12 --version

# If missing, install:
# Debian: sudo apt install python3.11 python3.12
# macOS: brew install python@3.11 python@3.12
```

**Docker not running**
```bash
# Start Docker daemon
sudo systemctl start docker  # Linux
open /Applications/Docker.app  # macOS
```

### Connection Issues

**Coinbase API returns 401 (Unauthorized)**
```bash
# Verify credentials
python3 scripts/test_api_connection.py

# Check:
✓ API key has "trade" permission
✓ API key not expired (set 90-day rotation)
✓ IP whitelist includes your server IP
✓ Timestamp is synced (run: sudo ntpdate -q pool.ntp.org)
```

**Bots won't execute trades**
```bash
# Check balance
python3 scripts/check_balance.py

# Check pair whitelist in config
grep "pair_whitelist" user_data/config.json

# Verify minimum balance (e.g., $100 for $100 position)
```

### Performance Issues

**High CPU usage**
```bash
# Reduce backtest workers
# Edit config: "max_workers": 2

# Reduce Grafana refresh rate
# Grafana → Dashboard settings → Refresh
```

**Memory issues (Docker)**
```bash
# Increase Docker memory limit
# Docker Desktop → Settings → Resources
# Or edit /etc/docker/daemon.json (Linux)
```

---

## 📚 Learning Resources

### Included Documentation
1. `DEPLOYMENT_GUIDE.md` - Step-by-step setup
2. `LEARNING_PATH.md` - 7-day learning path
3. `RISK_MANAGEMENT.md` - Position sizing & drawdown
4. `TAX_GUIDE.md` - Capital gains & tax reporting
5. `API_REFERENCE.md` - Coinbase API examples

### External Resources
- **Freqtrade Docs**: https://www.freqtrade.io
- **Passivbot Wiki**: https://github.com/enarjord/passivbot/wiki
- **Coinbase API**: https://docs.cdp.coinbase.com
- **CCXT Library**: https://github.com/ccxt/ccxt
- **TradingView**: Technical analysis & backtesting

---

## 💰 Cost Breakdown

| Component | Cost | Notes |
|-----------|------|-------|
| **Hardware** | $0-500 | Reuse existing computer |
| **VPS** (optional) | $0-10/month | For 24/7 uptime |
| **Coinbase Fees** | Variable | Maker 0.1%, Taker 0.6% |
| **Bots** | $0 | All open-source |
| **Monitoring** | $0 | Grafana+InfluxDB free |
| **Reporting** | $0 | Custom Python scripts |
| **Tax Software** | $0-150/year | Optional (Koinly, CoinLedger) |
| **Annual Total** | $0-500 | Completely optional VPS |

**No subscriptions. No monthly fees. Pure ownership.**

---

## 🤝 Contributing & Community

- Report bugs: [GitHub Issues]
- Suggest features: [GitHub Discussions]
- Share strategies: [Strategy Repository]
- Join Discord: [Community Server]

---

## 📄 License

This package integrates open-source projects:
- **Freqtrade**: GPL-3.0
- **Passivbot**: GPLv3
- **CCXT**: MIT
- **Grafana**: AGPL-3.0
- **InfluxDB**: AGPL-3.0 (cloud), BSL (self-hosted)

See individual repositories for full license terms.

---

## ⚖️ Disclaimer

**This software is provided AS-IS for educational purposes.**

- Trading cryptocurrencies is high-risk
- Bots can fail, orders can be missed, money can be lost
- Past performance ≠ future results
- Thoroughly backtest and paper trade before using real money
- Start with small positions (5% of account)
- This is NOT financial advice

**Use at your own risk.**

---

## 🎓 Getting Started in 3 Steps

### Step 1: Read
Read `DEPLOYMENT_GUIDE.md` (20 min)

### Step 2: Install
Run `bash install.sh` (5 min)

### Step 3: Learn
Follow `LEARNING_PATH.md` for 7 days

**That's it!** You'll have a professional trading setup.

---

**Last Updated**: December 2025  
#### Maintainer: [@jbenz](https://github.com/jbenz/tradingDesk)
**Support**: Check Troubleshooting section first

Happy trading! 🚀📈
