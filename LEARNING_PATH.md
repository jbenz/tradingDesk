# First Week Learning Path & Daily Checklist

**Goal**: Set up, configure, test, and deploy your first trading bot safely.

---

## Day 1: Installation & Setup (2-3 hours)

### Morning (1 hour)

- [ ] Read `DEPLOYMENT_GUIDE.md` (this directory)
- [ ] Check system requirements
  ```bash
  python3 --version  # Should be 3.11+
  git --version
  docker --version
  ```
- [ ] Create API keys on Coinbase
  - Go to Settings → API → Create Key
  - Enable: `trade`, `view`
  - Restrict IP address
  - Save: Key ID, Secret, Passphrase

### Afternoon (1.5 hours)

- [ ] Run installer
  ```bash
  bash install.sh
  ```
- [ ] Configure API keys
  ```bash
  nano ~/.trading_bot_keys.env
  # Paste: CB_API_KEY, CB_API_SECRET, CB_API_PASSPHRASE
  chmod 600 ~/.trading_bot_keys.env
  ```
- [ ] Test Coinbase connection
  ```bash
  python3 scripts/test_api_connection.py
  ```
- [ ] Verify all components installed
  ```bash
  ls -la ~/trading-bots/
  # Should show: freqtrade, passivbot, barbotine
  ```

### Evening (30 min)

- [ ] Start Docker services
  ```bash
  docker-compose up -d
  ```
- [ ] Access dashboards (should be empty for now)
  - Grafana: http://localhost:3000 (admin/admin)
  - Freqtrade UI: http://localhost:8080

**Day 1 Summary**: ✓ All installed and connected

---

## Day 2: Configure Freqtrade (2-3 hours)

### Morning (1.5 hours)

**Freqtrade is for spot/margin trading (DCA, Grid, moving average strategies)**

1. Generate initial config:
   ```bash
   cd ~/trading-bots/freqtrade
   source venv/bin/activate
   freqtrade create-userdir --userdir user_data
   freqtrade new-config --config user_data/config.json
   ```

2. Answer setup wizard:
   ```
   Exchange: coinbase
   API key: [Your key]
   API secret: [Your secret]
   Stake currency: USD
   Dry run: YES (for testing)
   Strategy: SMA (Simple Moving Average)
   ```

### Afternoon (1.5 hours)

3. Edit config for safety:
   ```bash
   nano user_data/config.json
   ```
   
   **Critical settings:**
   ```json
   {
     "max_open_trades": 3,
     "stake_amount": 100,
     "dry_run": true,
     "stake_currency": "USD",
     "fiat_display_currency": "USD",
     "exchange": {
       "name": "coinbase",
       "pair_whitelist": ["BTC/USD", "ETH/USD"],
       "ccxt_config": { "sandbox": false },
       "ccxt_async_config": {}
     },
     "telegram": {
       "enabled": false
     },
     "max_stake_amount": 1000,
     "dry_run_wallet": 10000
   }
   ```

4. Test with dry run (simulation):
   ```bash
   freqtrade backtest --config user_data/config.json \
     --strategy SMA \
     --timeframe 1h \
     --timerange 20241101-20241220
   ```
   
   **Expected output:**
   ```
   ============ Backtest result ==========
   Total trades: 45
   Wins: 24 | Losses: 21
   Win rate: 53%
   Total profit: 2.3%
   ```

### Evening (30 min)

- [ ] Review backtest results carefully
- [ ] If win rate < 40%, strategy needs tuning
- [ ] Document findings in `~/trading-bots/logs/day2_findings.txt`

**Day 2 Summary**: ✓ Freqtrade configured and backtested

---

## Day 3: Configure Passivbot (2-3 hours)

### Morning (1.5 hours)

**Passivbot is for perpetual futures trading (high leverage strategies)**

1. Understand Passivbot concepts:
   - Grid trading: Buy at intervals, collect profits
   - DCA: Accumulate position over time
   - Momentum: Trade trends with leverage
   
2. Review sample config:
   ```bash
   cd ~/trading-bots/passivbot
   source venv/bin/activate
   ls configs/
   ```

3. Create your config:
   ```bash
   cp configs/default.json configs/coinbase_btc_grid.json
   nano configs/coinbase_btc_grid.json
   ```
   
   **Example grid trading config:**
   ```json
   {
     "exchange": "coinbase",
     "symbol": "BTCUSDT",
     "mode": "normal",
     "live": false,
     "logging": "info",
     
     "long": {
       "enabled": true,
       "leverage": 2.0,
       "grid_spacing": 0.005,
       "initial_qty": 0.01,
       "max_qty": 0.05
     },
     "short": {
       "enabled": false
     },
     
     "risk_management": {
       "stop_loss_pct": 5.0,
       "take_profit_pct": 2.0
     }
   }
   ```

### Afternoon (1.5 hours)

4. Backtest the strategy:
   ```bash
   python3 backtest.py \
     -c configs/coinbase_btc_grid.json \
     --start-date 2024-10-01 \
     --end-date 2024-12-20
   ```
   
   **Evaluate results:**
   - Win rate > 50%? ✓
   - Sharpe ratio > 1? ✓
   - Max drawdown < 20%? ✓

5. Simulate live mode (paper trading):
   ```bash
   python3 passivbot.py -c configs/coinbase_btc_grid.json
   # Let it run for 1-2 hours, monitor logs
   tail -f logs/passivbot.log
   ```

### Evening

- [ ] Document findings in `~/trading-bots/logs/day3_findings.txt`
- [ ] Note any issues or unexpected behavior
- [ ] Compare to backtest results

**Day 3 Summary**: ✓ Passivbot configured and paper tested

---

## Day 4: Arbitrage Bot Setup (1-2 hours)

### Morning (1 hour)

**Barbotine finds price differences between exchanges**

1. Understand arbitrage:
   - Buy on Coinbase at $95,000
   - Sell on Binance at $95,500
   - Keep $500 profit
   - Zero directional risk

2. Configure exchanges:
   ```bash
   cd ~/trading-bots/barbotine
   source venv/bin/activate
   nano exchange_config.py
   ```
   
   ```python
   EXCHANGES = {
       'coinbase': {
           'api_key': os.getenv('CB_API_KEY'),
           'api_secret': os.getenv('CB_API_SECRET'),
           'api_passphrase': os.getenv('CB_API_PASSPHRASE'),
       },
       'binance': {
           'api_key': os.getenv('BINANCE_KEY'),
           'api_secret': os.getenv('BINANCE_SECRET'),
       },
       # ... more exchanges
   }
   ```

3. Test in fake-money mode:
   ```bash
   python3 main.py fake-money 500 BTC/USDT coinbase,binance,okx
   # Simulates with $500 USDT, no real trades
   ```

### Afternoon (1 hour)

4. Monitor for opportunities:
   ```bash
   # Watch output for detected arbitrage opportunities
   # Example: "Opportunity found: Buy BTC on Coinbase at 95000, Sell on Binance at 95500, Profit: $500"
   ```

5. Run for 30+ minutes to find patterns

- [ ] Document profitable pairs
- [ ] Document execution fees for each exchange pair

**Day 4 Summary**: ✓ Arbitrage bot configured and tested

---

## Day 5: Monitoring & Reporting Setup (2 hours)

### Morning (1 hour)

1. Access Grafana dashboard:
   - URL: http://localhost:3000
   - Login: admin/admin
   - Go to: Configuration → Data Sources
   - Add: InfluxDB (http://influxdb:8086)

2. Create your first dashboard:
   - Click: + → Dashboard
   - Add panel: BTC Balance
   - Query InfluxDB: `from(bucket:"trading-metrics") |> range(start: -7d)`

### Afternoon (1 hour)

3. Set up reporting script:
   ```bash
   cd ~/trading-bots/reports
   python3 generate_reports.py
   # Generates: reports/exports/daily_report_YYYY-MM-DD.csv
   ```

4. Create cron job for daily reports:
   ```bash
   crontab -e
   # Add: 0 22 * * * cd ~/trading-bots && python3 reports/generate_reports.py
   # (Runs daily at 10 PM)
   ```

5. Test report generation:
   ```bash
   python3 reports/generate_reports.py --tax
   # Should create: daily_report_XXX.json, daily_report_XXX.csv, form_8949_2025.csv
   ```

**Day 5 Summary**: ✓ Monitoring and reporting configured

---

## Day 6: Safety Checks & Risk Management (1 hour)

### Setup Risk Limits

1. **Stop-loss limits** (per bot config):
   ```
   Freqtrade: max loss 5% per trade
   Passivbot: stop loss at 5% below entry
   Barbotine: max position 5% of account
   ```

2. **Daily P&L limits**:
   ```bash
   # Add to crontab
   # 23:59 every day: Check daily loss > 10%? → Email alert
   python3 scripts/daily_loss_check.py
   ```

3. **Emergency kill-switch**:
   ```bash
   #!/bin/bash
   # emergency_stop.sh - Stops all bots immediately
   tmux kill-session -t freqtrade
   tmux kill-session -t passivbot
   docker-compose down
   echo "✓ All bots stopped"
   ```

### Create Daily Checklist

```bash
cat > ~/trading-bots/daily_checklist.sh << 'EOF'
#!/bin/bash
# Daily trading bot health check

echo "=== Daily Trading Bot Health Check ==="
echo "Date: $(date)"

echo ""
echo "1. Bot Status:"
docker-compose ps

echo ""
echo "2. Recent Trades (Last 24h):"
python3 reports/get_recent_trades.py

echo ""
echo "3. Daily P&L:"
python3 reports/get_daily_pl.py

echo ""
echo "4. Account Balance:"
python3 scripts/check_balance.py

echo ""
echo "5. Alerts:"
python3 scripts/check_alerts.py

echo ""
echo "Check complete! ✓"
EOF

chmod +x ~/trading-bots/daily_checklist.sh
```

**Day 6 Summary**: ✓ Safety systems configured

---

## Day 7: Go Live (First Real Trade - Small) (1-2 hours)

### CRITICAL: Size Appropriately

**Account Size → First Position Size**
- $100 account → $5 position (5%)
- $500 account → $25 position (5%)
- $1,000 account → $50 position (5%)
- $5,000 account → $250 position (5%)

### Morning (30 min)

1. **Final safety verification**:
   ```bash
   ✓ API keys working
   ✓ Backtest results reviewed (>45% win rate)
   ✓ Daily loss limits set
   ✓ Stop-loss orders configured
   ✓ Emergency stop script tested
   ```

2. **Enable live trading (ONE bot only)**:
   ```bash
   # Option A: Freqtrade DCA (safest for first trade)
   nano ~/trading-bots/freqtrade/user_data/config.json
   # Change: "dry_run": true → "dry_run": false
   # Change: "stake_amount": 100  (adjust to 5% of account)
   ```

3. **Deploy with minimal position**:
   ```bash
   cd ~/trading-bots/freqtrade
   source venv/bin/activate
   freqtrade trade --config user_data/config.json &
   ```

### Afternoon (1-1.5 hours)

4. **Monitor trade execution** (every 15 min for first hour):
   ```bash
   # Watch logs in real-time
   tail -f logs/freqtrade.log
   
   # Check positions
   python3 scripts/check_positions.py
   
   # Monitor P&L
   python3 reports/get_daily_pl.py
   ```

5. **Verify first trade**:
   - Order appeared in Coinbase?
   - Price matched expectations?
   - Fees reasonable?
   - Stop-loss set?

### Evening (30 min)

6. **If everything OK**:
   - ✓ Keep bot running
   - ✓ Set up email alerts (optional)
   - ✓ Schedule 9 PM daily health check

7. **If issues**:
   - STOP all bots
   - Review logs
   - Adjust config
   - Test again in dry-run

---

## Daily Routine (Ongoing)

### Every Morning (5 min)
```bash
~/trading-bots/daily_checklist.sh

# Check for alerts
mail  # If configured
```

### Every Day at 10 PM (Automatic)
- Daily P&L report generated
- Tax data recorded
- Database backed up
- Alert email sent (if P&L < threshold)

### Weekly (Sunday)
```bash
# Backtest strategy with latest data
python3 ~/trading-bots/freqtrade/backtest.py \
  --config user_data/config.json \
  --timerange 20250101-$(date +%Y%m%d)

# Review performance
python3 reports/weekly_summary.py
```

### Monthly (1st of month)
```bash
# Export monthly tax records
python3 reports/generate_reports.py --tax --month $(date +%m)

# Review profit attribution
python3 reports/profit_attribution.py
```

### Quarterly
```bash
# Generate tax report for upcoming payment
python3 reports/generate_tax_report.py --year 2025

# File estimated taxes (Form 1040-ES)
# Payments due: Apr 15, Jun 15, Sep 15, Jan 15
```

---

## Common Issues & Fixes

### **Bot won't start**
```bash
# Check API connection
python3 scripts/test_api_connection.py

# Check logs
docker-compose logs freqtrade
tail -f ~/trading-bots/freqtrade/logs/*.log
```

### **No trades executing**
```bash
# Check balance
python3 scripts/check_balance.py

# Check if pairs have sufficient balance
# If $100 USDT account, need at least $100 for 1 position

# Increase logging verbosity
nano user_data/config.json
# Set: "verbosity": "info"
```

### **Losing money fast**
```bash
# IMMEDIATELY STOP
pkill -f freqtrade
pkill -f passivbot

# Analyze what went wrong
python3 reports/trade_analysis.py

# Adjust strategy or reduce position size
# Never risk more than 1-2% per trade
```

### **Monitoring not showing data**
```bash
# Check InfluxDB
curl http://localhost:8086/health

# Verify data is being written
influx bucket list -o trading

# Check Grafana data source connection
# Settings → Data Sources → InfluxDB → Test
```

---

## Week 1 Completion Checklist

- [ ] Day 1: All components installed
- [ ] Day 2: Freqtrade configured and backtested
- [ ] Day 3: Passivbot configured and tested
- [ ] Day 4: Barbotine running in simulation
- [ ] Day 5: Monitoring and reporting working
- [ ] Day 6: Safety systems in place
- [ ] Day 7: First real trade executed (small position)
- [ ] Daily checklist automated
- [ ] Emergency stop procedure tested

**Congratulations!** You now have a fully operational open-source trading ecosystem. 🚀
