#!/bin/bash

# Automated Installation Script for Crypto Trading Bot Ecosystem
# Supports: Debian 12/13, macOS Sequoia
# Usage: bash install.sh
# TESTED: Debian 13 (Trixie) with Python 3.13

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect OS
OS="unknown"
PYTHON_VERSION=""

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    if grep -q "Debian\|Ubuntu" /etc/os-release 2>/dev/null; then
        DISTRO="debian"
    fi
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1-2)
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    ARCH=$(uname -m)
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1-2)
fi

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Crypto Trading Bot Ecosystem Installer${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "Detected OS: $OS ($DISTRO)"
echo "Detected Python: $PYTHON_VERSION"
echo ""

# Check requirements
check_requirements() {
    echo -e "${YELLOW}[1/5] Checking requirements...${NC}"
    
    local missing=0
    
    # Check Python (any 3.9+)
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}✗ Python 3 not found${NC}"
        missing=1
    else
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"
    fi
    
    # Check Git
    if ! command -v git &> /dev/null; then
        echo -e "${RED}✗ Git not found${NC}"
        missing=1
    else
        echo -e "${GREEN}✓ Git installed${NC}"
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}✗ Docker not found (optional, but recommended)${NC}"
    else
        echo -e "${GREEN}✓ Docker installed${NC}"
    fi
    
    if [ $missing -eq 1 ]; then
        echo ""
        echo -e "${RED}Missing required dependencies. Please install:${NC}"
        if [ "$OS" = "linux" ]; then
            echo "sudo apt update && sudo apt install -y python3 python3-pip python3-venv git build-essential"
        else
            echo "brew install python3 git"
        fi
        exit 1
    fi
}

# Install system dependencies
install_dependencies() {
    echo ""
    echo -e "${YELLOW}[2/5] Installing system dependencies...${NC}"
    
    if [ "$OS" = "linux" ]; then
        sudo apt update
        sudo apt install -y \
            python3-pip python3-venv \
            git curl wget build-essential \
            libssl-dev libffi-dev python3-dev \
            sqlite3 \
            tmux screen
        
        # Add user to docker group (non-sudo docker commands)
        if command -v docker &> /dev/null; then
            sudo usermod -aG docker $USER 2>/dev/null || true
            echo -e "${YELLOW}⚠ You may need to relogin for Docker permissions${NC}"
        fi
        
        echo -e "${GREEN}✓ Dependencies installed${NC}"
    else
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python3 git
        echo -e "${GREEN}✓ Dependencies installed${NC}"
    fi
}

# Clone repositories
clone_repositories() {
    echo ""
    echo -e "${YELLOW}[3/5] Cloning repositories...${NC}"
    
    mkdir -p ~/trading-bots
    cd ~/trading-bots
    
    # Freqtrade
    if [ ! -d "freqtrade" ]; then
        echo "Cloning Freqtrade..."
        git clone https://github.com/freqtrade/freqtrade.git
        cd freqtrade
        git checkout stable
        cd ..
        echo -e "${GREEN}✓ Freqtrade cloned${NC}"
    else
        echo -e "${GREEN}✓ Freqtrade already exists${NC}"
    fi
    
    # Passivbot
    if [ ! -d "passivbot" ]; then
        echo "Cloning Passivbot..."
        git clone https://github.com/enarjord/passivbot.git
        echo -e "${GREEN}✓ Passivbot cloned${NC}"
    else
        echo -e "${GREEN}✓ Passivbot already exists${NC}"
    fi
    
    # Barbotine
    if [ ! -d "barbotine" ]; then
        echo "Cloning Barbotine..."
        git clone https://github.com/nelso0/barbotine-arbitrage-bot.git barbotine
        echo -e "${GREEN}✓ Barbotine cloned${NC}"
    else
        echo -e "${GREEN}✓ Barbotine already exists${NC}"
    fi
}

# Setup Python environments
setup_python_envs() {
    echo ""
    echo -e "${YELLOW}[4/5] Setting up Python virtual environments...${NC}"
    
    cd ~/trading-bots
    
    # Freqtrade venv
    if [ ! -d "freqtrade/venv" ]; then
        echo "Creating Freqtrade venv..."
        cd freqtrade
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip setuptools wheel
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
        fi
        deactivate
        cd ..
        echo -e "${GREEN}✓ Freqtrade venv ready${NC}"
    else
        echo -e "${GREEN}✓ Freqtrade venv already exists${NC}"
    fi
    
    # Passivbot venv
    if [ ! -d "passivbot/venv" ]; then
        echo "Creating Passivbot venv..."
        cd passivbot
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip setuptools wheel
        
        # Install Rust if needed (for Passivbot)
        if ! command -v rustc &> /dev/null; then
            echo "Installing Rust (required for Passivbot)..."
            curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
            source "$HOME/.cargo/env"
        fi
        
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
        fi
        
        # Try to build Rust components if they exist
        if [ -d "passivbot-rust" ]; then
            cd passivbot-rust
            maturin develop --release 2>/dev/null || echo -e "${YELLOW}⚠ Rust build optional, continuing...${NC}"
            cd ..
        fi
        
        deactivate
        cd ..
        echo -e "${GREEN}✓ Passivbot venv ready${NC}"
    else
        echo -e "${GREEN}✓ Passivbot venv already exists${NC}"
    fi
    
    # Barbotine venv
    if [ ! -d "barbotine/venv" ]; then
        echo "Creating Barbotine venv..."
        cd barbotine
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip setuptools wheel
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
        fi
        deactivate
        cd ..
        echo -e "${GREEN}✓ Barbotine venv ready${NC}"
    else
        echo -e "${GREEN}✓ Barbotine venv already exists${NC}"
    fi
}

# Setup configuration
setup_configuration() {
    echo ""
    echo -e "${YELLOW}[5/5] Setting up configuration...${NC}"
    
    mkdir -p ~/.trading_bot_config
    mkdir -p ~/trading-bots/reports
    
    # Create environment file
    if [ ! -f ~/.trading_bot_keys.env ]; then
        cat > ~/.trading_bot_keys.env << 'EOF'
# Crypto Trading Bot API Keys
# IMPORTANT: Keep this file secure (chmod 600)

# Coinbase Advanced API
CB_API_KEY=""
CB_API_SECRET=""
CB_API_PASSPHRASE=""

# Binance (optional, for arbitrage)
BINANCE_KEY=""
BINANCE_SECRET=""

# OKX (optional, for arbitrage)
OKX_KEY=""
OKX_SECRET=""
OKX_PASSPHRASE=""

# Database
DB_URL="sqlite:///trades.db"
INFLUX_TOKEN=""
INFLUX_ORG="trading"
INFLUX_BUCKET="trading-metrics"

# Email Notifications (optional)
EMAIL_FROM=""
EMAIL_PASSWORD=""
EMAIL_TO=""

# Telegram Bot (optional)
TELEGRAM_BOT_TOKEN=""
TELEGRAM_CHAT_ID=""
EOF
        chmod 600 ~/.trading_bot_keys.env
        echo -e "${GREEN}✓ Created ~/.trading_bot_keys.env${NC}"
    else
        echo -e "${GREEN}✓ ~/.trading_bot_keys.env already exists${NC}"
    fi
    
    # Create startup script
    cat > ~/trading-bots/start_all.sh << 'EOF'
#!/bin/bash
# Start all trading bots

export $(cat ~/.trading_bot_keys.env | xargs)

echo "Starting Freqtrade..."
tmux new-session -d -s freqtrade -c ~/trading-bots/freqtrade \
    "source venv/bin/activate && freqtrade trade --config user_data/config.json"

echo "Starting Passivbot..."
tmux new-session -d -s passivbot -c ~/trading-bots/passivbot \
    "source venv/bin/activate && python3 passivbot.py -c configs/coinbase_config.json"

echo "Starting Monitoring..."
tmux new-session -d -s monitoring -c ~/trading-bots \
    "docker-compose up -d"

echo ""
echo "All bots started. View with: tmux list-sessions"
EOF
    chmod +x ~/trading-bots/start_all.sh
    echo -e "${GREEN}✓ Created start_all.sh${NC}"
}

# Main execution
main() {
    check_requirements
    install_dependencies
    clone_repositories
    setup_python_envs
    setup_configuration
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Installation Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Edit API keys: nano ~/.trading_bot_keys.env"
    echo "2. Configure Freqtrade:"
    echo "   cd ~/trading-bots/freqtrade"
    echo "   source venv/bin/activate"
    echo "   freqtrade new-config --config user_data/config.json"
    echo ""
    echo "3. Configure Passivbot:"
    echo "   nano ~/trading-bots/passivbot/configs/coinbase_config.json"
    echo ""
    echo "4. Start bots: ~/trading-bots/start_all.sh"
    echo ""
    echo "Access dashboards:"
    echo "• Freqtrade UI: http://localhost:8080"
    echo "• Grafana: http://localhost:3000"
    echo ""
    echo "For detailed setup, read LEARNING_PATH.md"
    echo ""
}

main
