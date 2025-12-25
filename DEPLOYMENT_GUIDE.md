# Crypto Trading Bot Ecosystem - Deployment & Setup Guide

**Version**: 1.0  
**Last Updated**: December 2025  
**Supported Platforms**: Debian 12/13, macOS Sequoia (M4 Max)  
**License**: Open Source (Various - See individual repos)

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Quick Start (5 minutes)](#quick-start)
5. [Component Installation](#component-installation)
6. [Configuration](#configuration)
7. [Running & Monitoring](#running--monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This ecosystem includes:

| Component | Purpose | Tech Stack | Cost |
|-----------|---------|-----------|------|
| **Freqtrade** | DCA, Grid, MA strategies | Python 3.11+ | Free |
| **Passivbot** | Perpetual futures strategies | Python 3.12+ | Free |
| **Barbotine** | Arbitrage (cross-exchange) | Python 3.10+ | Free |
| **Monitoring** | Real-time dashboards | Grafana + InfluxDB | Free |
| **Reporting** | P&L, tax, trade analysis | Python + SQLite | Free |
| **API Wrapper** | Coinbase Advanced API | Python SDK | Free |

**Total First-Year Cost**: $0 (self-hosted)  
**Hardware**: Minimal (any Debian box or macOS works)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Trading Bots                        │
├──────────────────┬──────────────────┬──────────────────┐
│  Freqtrade       │  Passivbot       │  Barbotine       │
│  (Spot/Futures)  │  (Perpetuals)    │  (Arbitrage)     │
└──────────┬───────┴────────┬─────────┴─────────┬────────┘
           │                │                   │
           │    APIs        │                   │
           ├────────────────┴───────────────────┤
           │                                    │
      ┌────┴─────────────────────────────────┐
      │   Coinbase Advanced Trade API        │
      │   (REST + WebSocket)                 │
      └────┬────────────────────────────────┘
           │
     ┌─────┴──────────────────────────────────┐
     │      Data Pipeline & Reporting         │
     ├─────────────────┬──────────────────────┤
     │  InfluxDB       │  SQLite (Trades)     │
     │  (Metrics)      │  (History & Tax)     │
     └────┬────────────┴────────┬─────────────┘
          │                     │
     ┌────┴─────────────────────┴─────────┐
     │     Analysis & Visualization        │
     ├──────────────┬──────────────────────┤
     │  Grafana     │  Python Reports      │
     │  (Live)      │  (Daily/Tax)         │
     └──────────────┴──────────────────────┘
```

---

## Prerequisites

### System Requirements

**Debian 12/13:**
```bash
# Check OS version
lsb_release -a

# Minimum specs:
# - 2GB RAM (4GB recommended for all bots)
# - 20GB SSD (50GB if running backtests)
# - 1 CPU (2+ recommended)
```

**macOS Sequoia (M4 Max):**
```bash
# Check version
sw_vers

# Should show: ProductName: macOS
#               ProductVersion: 15.x (Sequoia)
```

### Required Software

**Debian 12/13 - Install prerequisites:**
```bash
sudo apt update
sudo apt install -y \
  python3.11 python3.12 python3-pip \
  git curl wget build-essential \
  libssl-dev libffi-dev python3-dev \
  sqlite3 postgresql postgresql-contrib \
  docker.io docker-compose \
  nodejs npm \
  tmux screen
```

**macOS Sequoia - Install prerequisites:**
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install python@3.11 python@3.12 git node postgres docker docker-compose tmux

# Add to PATH (add to ~/.zshrc)
export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"
```

### Coinbase API Setup

1. **Create API Key:**
   - Go to: `coinbase.com → Settings → API → Create New Key`
   - Enable: `trade`, `view` (NOT `transfer`)
   - Restrict to IP address (your server)
   - Note: Key ID and Secret

2. **Test Access:**
```bash
# Save these temporarily
export CB_API_KEY="your_key_id"
export CB_API_SECRET="your_secret"
export CB_PASSPHRASE="your_passphrase"
```

---

## Quick Start (5 minutes)

### One-Line Installation (Automated)

```bash
# Download and run installer
curl -sSL https://raw.githubusercontent.com/yourusername/trading-bot-ecosystem/main/install.sh | bash

# This installs ALL components automatically
```

### Manual Quick Start (If One-Liner Fails)

```bash
# 1. Clone the ecosystem repo
git clone https://github.com/yourusername/trading-bot-ecosystem.git
cd trading-bot-ecosystem

# 2. Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Configure APIs
cp config/api_keys.example.json config/api_keys.json
# Edit with your Coinbase keys

# 4. Start all services
docker-compose up -d

# 5. Access dashboards
# Grafana: http://localhost:3000
# Freqtrade UI: http://localhost:8080
# Passivbot Web: http://localhost:8081
```

### Verify Installation

```bash
# Check all services running
docker-compose ps

# Check logs
docker-compose logs -f freqtrade

# Test Coinbase connection
python3 scripts/test_api_connection.py
```

---

## Component Installation

### 1. Freqtrade (DCA, Grid, MA Strategies)

**Recommended**: Use Docker (easiest)

```bash
# Docker installation (Recommended)
docker pull freqtradeorg/freqtrade:stable
docker run -it --name freqtrade \
  -v $PWD/freqtrade/config:/freqtrade/config \
  -v $PWD/freqtrade/user_data:/freqtrade/user_data \
  -p 8080:8080 \
  freqtradeorg/freqtrade:stable

# OR Manual installation
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade
git checkout stable
./setup.sh -i

# Create config
freqtrade create-userdir --userdir user_data
freqtrade new-config --config user_data/config.json

# Start
freqtrade trade --config user_data/config.json
```

**Configuration for Coinbase:**
```json
{
  "exchange": {
    "name": "coinbase",
    "key": "YOUR_API_KEY",
    "secret": "YOUR_API_SECRET",
    "pair_whitelist": ["BTC/USD", "ETH/USD", "SOL/USD"],
    "sandbox": false
  },
  "stake_currency": "USD",
  "dry_run": true
}
```

---

### 2. Passivbot (Perpetual Futures)

**Setup:**
```bash
# Clone Passivbot
git clone https://github.com/enarjord/passivbot.git
cd passivbot

# Install Rust (required)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"

# Create venv
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build Rust components
cd passivbot-rust
maturin develop --release
cd ..
```

**Configuration:**
```bash
# Copy config template
cp configs/default.json configs/coinbase_config.json

# Edit with your settings
nano configs/coinbase_config.json
```

**Run live:**
```bash
source venv/bin/activate
python3 passivbot.py -c configs/coinbase_config.json
```

**Run backtester:**
```bash
python3 backtest.py -c configs/coinbase_config.json --start-date 2024-01-01 --end-date 2024-12-31
```

---

### 3. Barbotine (Cross-Exchange Arbitrage)

**Setup:**
```bash
# Clone Barbotine
git clone https://github.com/nelso0/barbotine-arbitrage-bot.git
cd barbotine-arbitrage-bot

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure exchanges
cp exchange_config.py.example exchange_config.py
nano exchange_config.py
```

**Run in simulation mode (safest):**
```bash
python3 main.py fake-money 500 BTC/USDT coinbase,binance,okx
```

**Run live (with real balance):**
```bash
python3 main.py real 15 1000 ETH/USDT coinbase,binance
```

---

### 4. Monitoring Stack (Grafana + InfluxDB)

**Docker setup (Easiest):**
```bash
# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana
# URL: http://localhost:3000
# Default: admin / admin
```

**Manual setup:**
```bash
# Install InfluxDB
curl https://repos.influxdata.com/influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
sudo apt update && sudo apt install -y influxdb2

# Start InfluxDB
sudo systemctl start influxdb

# Install Grafana
sudo apt install -y grafana-server
sudo systemctl start grafana-server
```

---

### 5. Reporting Suite (Python + SQLite)

**Setup:**
```bash
# Create reports directory
mkdir -p reports
cd reports

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python3 init_db.py

# Run daily report generator
python3 generate_daily_report.py

# Generate tax report
python3 generate_tax_report.py --year 2025
```

---

## Configuration

### API Keys Setup

**Create secure config file:**
```bash
cat > ~/.trading_bot_keys.env << 'EOF'
# Coinbase Advanced API
CB_API_KEY="your_key_id_here"
CB_API_SECRET="your_secret_here"
CB_API_PASSPHRASE="your_passphrase_here"

# Additional exchanges (optional)
BINANCE_KEY="your_binance_key"
BINANCE_SECRET="your_binance_secret"

# Database
DB_URL="sqlite:///trades.db"
INFLUX_TOKEN="your_influx_token"
EOF

# Set permissions
chmod 600 ~/.trading_bot_keys.env

# Load in shell
source ~/.trading_bot_keys.env
```

### Bot-Specific Configs

See individual sections above for:
- Freqtrade config.json
- Passivbot configs/
- Barbotine exchange_config.py

---

## Running & Monitoring

### Start All Services (Docker)

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

### Start Individual Bots

```bash
# Terminal 1: Freqtrade
tmux new-session -d -s freqtrade
tmux send-keys -t freqtrade "cd freqtrade && source venv/bin/activate && freqtrade trade --config user_data/config.json" Enter

# Terminal 2: Passivbot
tmux new-session -d -s passivbot
tmux send-keys -t passivbot "cd passivbot && source venv/bin/activate && python3 passivbot.py -c configs/coinbase_config.json" Enter

# Terminal 3: Monitoring
tmux new-session -d -s monitoring
tmux send-keys -t monitoring "docker-compose -f docker-compose.monitoring.yml up" Enter

# Terminal 4: Reporting
tmux new-session -d -s reporting
tmux send-keys -t reporting "cd reports && python3 report_server.py" Enter

# List sessions
tmux list-sessions

# Attach to session
tmux attach -t freqtrade
```

### Monitor via Web Dashboards

| Service | URL | Credentials |
|---------|-----|-------------|
| Freqtrade UI | http://localhost:8080 | None (local) |
| Grafana | http://localhost:3000 | admin/admin |
| Passivbot Web | http://localhost:8081 | See config |
| Reports API | http://localhost:5000 | None (local) |

### Daily Monitoring Checklist

Every morning, check:

```bash
#!/bin/bash
# daily_health_check.sh

echo "=== Bot Status ==="
docker-compose ps

echo "=== Freqtrade Trades Last 24h ==="
curl http://localhost:8080/api/v1/trades -s | jq '.[] | select(.close_date > now - 86400) | {pair, profit_abs, close_date}' | head -10

echo "=== Latest P&L ==="
python3 reports/get_daily_pl.py

echo "=== Alerts (if any) ==="
python3 reports/check_alerts.py

# Email daily report
python3 reports/send_email_report.py
```

---

## Troubleshooting

### Common Issues

#### **Bot won't connect to Coinbase API**

```bash
# Test connection
python3 << 'EOF'
from cbpro_advanced import RESTClient
import os

client = RESTClient(
    api_key=os.getenv("CB_API_KEY"),
    api_secret=os.getenv("CB_API_SECRET"),
    api_passphrase=os.getenv("CB_API_PASSPHRASE")
)

try:
    accounts = client.get_accounts()
    print("✓ Connected successfully")
    print(f"Accounts: {len(accounts)}")
except Exception as e:
    print(f"✗ Connection failed: {e}")
EOF
```

**Solutions:**
- Verify API key permissions (trade + view enabled)
- Check IP whitelist
- Verify keys are not expired
- Check system clock sync: `ntpdate -q pool.ntp.org`

#### **Insufficient balance for bot orders**

```bash
# Check account balance
python3 scripts/check_balance.py

# Expected output:
# BTC: 0.5
# ETH: 10.0
# USD: 5000
```

**Solution**: Deposit funds to Coinbase account

#### **InfluxDB not receiving metrics**

```bash
# Check InfluxDB connectivity
curl http://localhost:8086/health

# Check database exists
influx bucket list -o yourorg

# Create bucket if missing
influx bucket create -n trading-metrics
```

#### **Grafana dashboard blank**

```bash
# Check data source configuration
# Grafana → Configuration → Data Sources → InfluxDB
# Verify: URL (http://localhost:8086), Token, Organization, Bucket

# Manually query data
influx query 'from(bucket:"trading-metrics") |> range(start: -24h)'
```

---

## Next Steps

1. **Week 1**: Complete installation + test with $100-500
2. **Week 2**: Run all bots in simulation mode, backtest strategies
3. **Week 3**: Deploy with real money on ONE strategy
4. **Week 4**: Add second bot/strategy, monitor P&L
5. **Week 5+**: Scale, optimize, automate reporting

See `LEARNING_PATH.md` for detailed week-by-week guide.
