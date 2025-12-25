# TRADING BOT ECOSYSTEM - QUICK REFERENCE CARD

Print this page and keep it next to your monitor.

---

## 🚀 60-Second Setup

```bash
# 1. Install everything
bash install.sh

# 2. Add API keys
nano ~/.trading_bot_keys.env

# 3. Start all services
docker-compose up -d

# 4. Verify connection
python3 test_api_connection.py

# 5. Access dashboards
# Grafana: http://localhost:3000 (admin/admin)
# Freqtrade: http://localhost:8080
```

✓ Done! Now read LEARNING_PATH.md Day 1

---

## 📋 Daily Commands Cheat Sheet

| Task | Command |
|------|---------|
| **Check account balance** | `python3 scripts/check_balance.py` |
| **Generate daily P&L** | `python3 reports/generate_reports.py` |
| **Health check** | `~/trading-bots/daily_checklist.sh` |
| **View logs** | `docker-compose logs -f freqtrade` |
| **Emergency stop** | `bash emergency_stop.sh` |
| **Test API** | `python3 test_api_connection.py` |
| **Start bots** | `~/trading-bots/start_all.sh` |
| **Stop bots** | `docker-compose down` |
| **Backtest Freqtrade** | `freqtrade backtest --config user_data/config.json --timerange 20240701-20241220` |
| **Backtest Passivbot** | `python3 passivbot/backtest.py -c configs/coinbase_grid.json --start-date 2024-07-01` |

---

## 🎯 Critical Risk Rules

### Position Sizing Formula
```
Position Size = (Account × 1-2%) / Stop-Loss %

Example: $10,000 × 1% = $100
         If stop-loss is 5%, max position = $2,000

NEVER: Risk >2% per trade or >10% of account in one position
```

### Daily Loss Limits
```
If daily loss > 5%   → Reduce all positions by 50%
If daily loss > 10%  → STOP all bots immediately
If daily loss > 20%  → Emergency situation, review all configs
```

### Leverage Guidelines
```
Spot trading:           1x (no leverage)    ✓ Safest
Margin trading:         2-3x max            ⚠️ Risky
Perpetual futures:      2-5x max            ⚠️⚠️ Very risky
DO NOT use:             10x+ leverage       ✗ Bankruptcy
```

---

## 🔐 Security Checklist

Before trading real money:

- [ ] Store API key in `~/.trading_bot_keys.env` (chmod 600)
- [ ] Use read-only API key for monitoring
- [ ] IP whitelist enabled on Coinbase
- [ ] 2FA enabled on Coinbase account
- [ ] NO withdrawal permissions on API key
- [ ] Daily backups running
- [ ] Emergency stop script tested
- [ ] Stop-loss on every single trade
- [ ] Account separate from personal funds
- [ ] Never share API keys in chat/email

---

## 🎓 7-Day Crash Course

| Day | Focus | Time |
|-----|-------|------|
| 1 | Installation & API setup | 2 hrs |
| 2 | Freqtrade config & backtest | 2 hrs |
| 3 | Passivbot config & test | 2 hrs |
| 4 | Barbotine arbitrage setup | 1.5 hrs |
| 5 | Monitoring & reporting | 1.5 hrs |
| 6 | Safety systems | 1 hr |
| 7 | First real trade ($50-100) | 1.5 hrs |

**Total Time**: ~12 hours of setup, then 30 min/day monitoring

---

## 📊 What Each Bot Does

### Freqtrade
- **Trades**: Spot & futures (Coinbase)
- **Strategies**: DCA, Grid, Moving Averages, RSI
- **Timeframes**: 1h to daily
- **Risk**: Low-medium (no leverage by default)
- **Best for**: Beginners, consistent income
- **Start**: `cd freqtrade && freqtrade trade --config user_data/config.json`

### Passivbot
- **Trades**: Perpetual futures (Bybit, OKX, Kucoin)
- **Strategies**: Grid trading, DCA
- **Leverage**: 2-5x configurable
- **Risk**: Medium-high
- **Best for**: Experienced traders, sideways markets
- **Start**: `python3 passivbot/passivbot.py -c configs/coinbase_grid.json`

### Barbotine
- **Trades**: Arbitrage (Coinbase + Binance + OKX)
- **Strategies**: Buy low exchange, sell high exchange
- **Leverage**: 1x (no leverage)
- **Risk**: Low-medium (delta-neutral)
- **Best for**: Finding free money between exchanges
- **Start**: `python3 barbotine/main.py fake-money 500 BTC/USDT coinbase,binance`

---

## 💾 Database Commands

### View Trade History
```bash
sqlite3 ~/trading-bots/reports/trades.db
> SELECT * FROM trades WHERE DATE(timestamp) = '2025-01-01';
> .quit
```

### Export Daily P&L
```bash
python3 reports/generate_reports.py
# Creates: reports/exports/daily_report_YYYY-MM-DD.csv
```

### Generate Tax Report
```bash
python3 reports/generate_reports.py --tax --year 2025
# Creates: form_8949_2025.csv (for IRS)
```

---

## 🐛 Troubleshooting Flowchart

```
Bot not trading?
├─ No balance? → Run: check_balance.py
├─ API error? → Run: test_api_connection.py
├─ Market closed? → Check: pair whitelist in config
├─ Stop-loss hit? → Check: logs/freqtrade.log
└─ Still broken? → STOP bot + review DEPLOYMENT_GUIDE.md

Lost money?
├─ Win rate <40%? → Retest strategy on more data
├─ Slippage issue? → Use limit orders instead of market
├─ Bad entry? → Tune strategy parameters
└─ Leverage too high? → Reduce leverage immediately

Can't connect to API?
├─ Clock sync? → Run: sudo ntpdate -q pool.ntp.org
├─ IP whitelist? → Check: Coinbase API settings
├─ Key expired? → Create new API key
└─ Wrong passphrase? → Verify: ~/.trading_bot_keys.env
```

---

## 🎓 Strategy Selection Guide

### I'm a beginner
→ Use **Freqtrade DCA** (Dollar-Cost Averaging)
- Buys fixed amount daily
- No leverage
- Consistent, predictable
- Safest option

### I want steady income
→ Use **Freqtrade Grid** or **Passivbot Grid**
- Buys dips, sells rallies
- Works in sideways markets
- 5-10% monthly returns possible
- Requires $1,000+ capital

### I want to catch trends
→ Use **Freqtrade SMA Crossover**
- Trades moving average signals
- Good in trending markets
- 20-50% annual returns
- More volatile than grid

### I want zero risk trading
→ Use **Barbotine Arbitrage**
- Buys on low exchange, sells on high
- Zero directional risk
- 1-5% profit per cycle
- Requires multiple exchange accounts

### I'm experienced
→ Combine all three strategies
- Hedge portfolio with multiple bots
- Diversify risk across strategies
- Use Passivbot with leverage (2-3x)
- Monitor daily

---

## 💰 Sample Position Sizes

### $1,000 Account
```
Freqtrade DCA:     $100-200 per trade (buy every 4 hours)
Max open trades:   2-3 at once
Max loss/day:      5-10% = $50-100
Stop loss:         5% below entry
```

### $5,000 Account
```
Freqtrade Grid:    $500 per grid (buy every 1% drop)
Passivbot:         $1,000 with 2x leverage = $2,000 exposure
Max loss/day:      5-10% = $250-500
Barbotine:         $500 per arbitrage cycle
```

### $10,000+ Account
```
Freqtrade:         $1,000-2,000 per position
Passivbot:         $2,000-5,000 with 2-3x leverage
Barbotine:         $1,000-2,000 per cycle
Total:             3-4 concurrent bots
```

---

## 📈 Success Metrics

### Good Performance
```
Win rate:           >45% (grid) or >50% (momentum)
Sharpe ratio:       >1.0 (risk-adjusted returns)
Max drawdown:       <30% of peak
Monthly return:     2-5% (realistic)
Winning days:       >60% of days
```

### Red Flags
```
Win rate <40%:      Strategy needs refinement
Daily loss >10%:    Stop bot, reduce position
Sharpe <0.5:        Risk too high relative to returns
Losing 5+ days:     Review fundamentals
Balance declining:  Fees eating profits
```

---

## 🔄 Monthly Checklist

**First of Month:**
- [ ] Export monthly P&L report
- [ ] Review performance metrics
- [ ] Rotate API keys (every 90 days)
- [ ] Backup database
- [ ] Check for code updates (git pull)

**Mid-Month:**
- [ ] Verify backtests with latest data
- [ ] Adjust position sizes if needed
- [ ] Review risk metrics

**End of Month:**
- [ ] Generate tax records
- [ ] Calculate quarterly estimate (if needed)
- [ ] Email reports to accountant

---

## 📞 Getting Help

### Installation issues
→ DEPLOYMENT_GUIDE.md → Troubleshooting section

### Strategy questions
→ LEARNING_PATH.md → Day 2-3 (Freqtrade/Passivbot setup)

### Risk management
→ RISK_MANAGEMENT.md (included)

### Tax questions
→ TAX_GUIDE.md (included)

### Bot not working
→ Run: `python3 test_api_connection.py`
→ Check: `docker-compose logs`

### Emergency situation
→ Run: `bash emergency_stop.sh`
→ Stop all bots immediately
→ Review logs before restarting

---

## ✅ Pre-Live Trading Checklist

Before you risk real money, verify:

- [ ] Backtest shows >40% win rate
- [ ] Tested in dry-run mode for 1 week
- [ ] Account has 3-6 months expenses in savings
- [ ] Stop-loss configured
- [ ] Daily loss limit set
- [ ] Position size is <5% of account
- [ ] Emergency stop script tested
- [ ] Monitoring dashboard accessible
- [ ] Daily reports generating correctly
- [ ] Tax tracking working

---

## 🎯 30-Day Goals

**Week 1:**
- [ ] Complete installation
- [ ] Configure 1 bot
- [ ] Paper trade

**Week 2:**
- [ ] Deploy 2nd bot
- [ ] Monitor daily
- [ ] Backtest additional strategies

**Week 3:**
- [ ] First real trade ($50-200)
- [ ] Monitor 24/7 (first few days)
- [ ] Generate weekly reports

**Week 4:**
- [ ] Scale to $500-1,000 positions
- [ ] Automate daily monitoring
- [ ] Plan next month improvements

---

## 📞 Emergency Numbers (For You)

**Save these numbers to your phone:**

```
Critical loss detected (>15%):
├─ Stop bots: bash emergency_stop.sh
├─ Review logs: docker-compose logs
├─ Call your risk management advisor

API not working:
├─ Test: python3 test_api_connection.py
├─ Check: Coinbase status page
├─ Contact: Coinbase support

Account compromised:
├─ IMMEDIATELY: Disable API key (Coinbase settings)
├─ CREATE: New API key
├─ REVIEW: Account activity
├─ MOVE: Funds to hardware wallet
```

---

## 🚀 Next Steps

1. **Right now**: Read README.md
2. **Next 5 min**: Run `bash install.sh`
3. **Next 30 min**: Read DEPLOYMENT_GUIDE.md
4. **Next 1-2 hours**: Follow LEARNING_PATH.md Day 1
5. **This week**: Complete Days 2-7 of LEARNING_PATH.md
6. **Week 2+**: Trade with real money (small positions)

---

**Good luck! You've got this. 🚀**

*Questions? Check DOCUMENTATION_INDEX.md for full guide locations.*
