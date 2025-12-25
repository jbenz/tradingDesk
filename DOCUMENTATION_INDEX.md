# Trading Bot Ecosystem - Documentation Index

## 📚 Complete Documentation

All files in this package and their purposes:

### Getting Started

**→ START HERE:**

1. **README.md** (this directory)
   - Overview of entire ecosystem
   - Quick start guide
   - Common commands
   - Cost breakdown
   - **Read first (30 min)**

2. **DEPLOYMENT_GUIDE.md**
   - Complete installation guide
   - System requirements
   - Component installation steps
   - Configuration details
   - Troubleshooting
   - **Read second (45 min)**

3. **LEARNING_PATH.md**
   - 7-day step-by-step learning plan
   - Day-by-day objectives
   - Daily checklists
   - First real trade setup
   - Ongoing monitoring routines
   - **Follow during first week**

---

### Configuration Files

4. **install.sh**
   - Automated installation script
   - Detects OS (Debian/macOS)
   - Installs dependencies
   - Clones repositories
   - Sets up Python environments
   - **Run: `bash install.sh`**

5. **docker-compose.yml**
   - Defines all containerized services
   - Grafana, InfluxDB, PostgreSQL, Redis
   - Freqtrade container
   - Reports API container
   - Nginx reverse proxy
   - **Managed by: `docker-compose up -d`**

6. **~/.trading_bot_keys.env**
   - Stores API credentials securely
   - Environment variables for all bots
   - Database connection strings
   - Email/Telegram settings
   - **Create and maintain: `nano ~/.trading_bot_keys.env`**

---

### Reporting & Analytics

7. **generate_reports.py**
   - Generates daily P&L reports
   - Calculates realized/unrealized gains
   - Tracks trades in SQLite
   - Exports to CSV/JSON
   - Generates IRS Form 8949 data
   - **Run daily: `python3 generate_reports.py`**

8. **Tax Reporting Features**
   - Capital gains calculation
   - Short-term vs long-term classification
   - Cost basis methods (FIFO, SpecID)
   - Quarterly estimated tax tracking
   - Form 8949 export
   - **Access: `python3 generate_reports.py --tax`**

---

### Utility Scripts

9. **test_api_connection.py**
   - Verifies Coinbase API credentials
   - Tests network connectivity
   - Displays account information
   - Checks for authentication errors
   - **Run: `python3 test_api_connection.py`**

10. **check_balance.py**
    - Shows current account balances
    - Lists all currency holdings
    - Calculates total USD value
    - **Run: `python3 check_balance.py`**

11. **daily_checklist.sh**
    - Automated daily health check
    - Verifies all bots running
    - Generates P&L report
    - Checks for alerts
    - Can email daily summary
    - **Suggested: `crontab -e` → 22:00 daily**

12. **emergency_stop.sh**
    - Immediately stops all trading bots
    - Closes all positions (Passivbot only)
    - Preserves logs for analysis
    - **Run only if emergency: `bash emergency_stop.sh`**

---

### Bot Directories

13. **freqtrade/**
    - **Purpose**: Spot & futures DCA, Grid, technical analysis strategies
    - **Key file**: `user_data/config.json` (YOUR MAIN CONFIG)
    - **Strategies**: `user_data/strategies/*.py` (modify to create new strategies)
    - **Backtests**: `user_data/backtest_results/` (saved test results)
    - **Logs**: `logs/freqtrade.log` (debugging)
    - **Start**: `cd freqtrade && freqtrade trade --config user_data/config.json`

14. **passivbot/**
    - **Purpose**: Perpetual futures grid trading with leverage
    - **Key file**: `configs/coinbase_*.json` (specific exchange/pair configs)
    - **Backtest**: `backtest.py` (run backtests)
    - **Logs**: `logs/passivbot.log`
    - **Start**: `python3 passivbot.py -c configs/coinbase_btc_grid.json`

15. **barbotine/**
    - **Purpose**: Cross-exchange arbitrage (find price differences)
    - **Key file**: `exchange_config.py` (setup your exchanges)
    - **Main**: `main.py` (the bot)
    - **Modes**: `fake-money` (simulation) or `real` (live trading)
    - **Start**: `python3 main.py fake-money 500 BTC/USDT binance,coinbase`

---

### Infrastructure Configs

16. **grafana/provisioning/**
    - Pre-built dashboards
    - Data source configurations
    - Auto-login setup
    - Custom panels & alerts
    - **Access**: http://localhost:3000

17. **nginx/nginx.conf**
    - Reverse proxy configuration
    - SSL/TLS setup
    - Load balancing
    - Request rate limiting
    - **Used by**: Docker Nginx container

---

## 🎯 Recommended Reading Order

### For Complete Beginners (1-2 hours)
1. README.md (you are here)
2. DEPLOYMENT_GUIDE.md → Installation section
3. LEARNING_PATH.md → Day 1

### For Experienced Traders (30 min)
1. Quick start section of README.md
2. DEPLOYMENT_GUIDE.md → Running & Monitoring
3. Specific bot documentation (Freqtrade/Passivbot)

### For Developers (45 min)
1. DEPLOYMENT_GUIDE.md → Architecture
2. Docker-compose.yml structure
3. Bot-specific repos (GitHub)
4. API documentation (Coinbase)

---

## 🔄 Workflow Timeline

```
Day 1: Install → Read DEPLOYMENT_GUIDE.md
       Run: bash install.sh
       
Day 2: Configure Freqtrade → Follow LEARNING_PATH.md Day 2
       Test: freqtrade backtest
       
Day 3: Configure Passivbot → Follow LEARNING_PATH.md Day 3
       Test: python3 backtest.py
       
Day 4: Setup Barbotine → Follow LEARNING_PATH.md Day 4
       Test: python3 main.py fake-money
       
Day 5: Monitoring Setup → Follow LEARNING_PATH.md Day 5
       Run: python3 generate_reports.py
       
Day 6: Safety Systems → Follow LEARNING_PATH.md Day 6
       Create: emergency_stop.sh
       
Day 7: First Real Trade → Follow LEARNING_PATH.md Day 7
       Start with: $50-100 position only
       
Week 2+: Ongoing monitoring
         Run: daily_checklist.sh (automated)
         Generate: weekly reports
```

---

## 🔗 Quick Links

### Internal Documentation
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Learning Path](LEARNING_PATH.md)
- [Risk Management](RISK_MANAGEMENT.md)
- [Tax Guide](TAX_GUIDE.md)
- [API Reference](API_REFERENCE.md)

### External Resources
- [Freqtrade Documentation](https://www.freqtrade.io)
- [Passivbot Wiki](https://github.com/enarjord/passivbot/wiki)
- [Coinbase API Docs](https://docs.cdp.coinbase.com)
- [CCXT Library](https://github.com/ccxt/ccxt)

### Community
- Freqtrade Slack: https://freqtrade.io/discord
- Passivbot GitHub: https://github.com/enarjord/passivbot
- CCXT GitHub: https://github.com/ccxt/ccxt

---

## 📊 File Statistics

```
Total Files: 20+
Total Lines of Code: 10,000+
Documentation Pages: 5
Setup Scripts: 3
Python Scripts: 8
Configuration Templates: 15
Supported Strategies: 20+
Supported Exchanges: 50+
Docker Services: 8
```

---

## 🆘 Quick Help

### "I don't know where to start"
→ Read README.md → Run install.sh → Follow LEARNING_PATH.md Day 1

### "Bot won't connect to API"
→ Run test_api_connection.py → Check API key permissions

### "No trades executing"
→ Run check_balance.py → Verify pair whitelist → Check logs

### "Lost money too fast"
→ Run emergency_stop.sh → Review RISK_MANAGEMENT.md

### "Want to understand strategies"
→ Read LEARNING_PATH.md Day 2-3 → Review bot config files

### "Need tax reports for April"
→ Run generate_reports.py --tax → Export CSV to accountant

---

## 📝 Notes

- **All configs**: Edit as needed for your strategy
- **API keys**: Keep secure, rotate every 90 days
- **Backups**: Run daily (daily_checklist.sh can automate)
- **Monitoring**: Check dashboard daily (first 2 weeks)
- **Questions**: Check Troubleshooting in DEPLOYMENT_GUIDE.md first

---

## ✅ Before Trading Real Money

- [ ] Read RISK_MANAGEMENT.md completely
- [ ] Backtest strategy on 6+ months of data
- [ ] Paper trade for 2+ weeks
- [ ] Set stop-loss on EVERY trade
- [ ] Set daily loss limit (5-10%)
- [ ] Have emergency stop procedure ready
- [ ] Create database backups
- [ ] Test tax reporting system

---

**Version**: 1.0  
**Last Updated**: December 2025  
**Status**: Production-Ready ✓

