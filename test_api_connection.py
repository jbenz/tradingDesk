#!/usr/bin/env python3
"""
Coinbase API Connection Tester

Tests connectivity to Coinbase Advanced Trade API and verifies credentials.
Usage: python3 test_api_connection.py
"""

import os
import sys
import base64
import hmac
import hashlib
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser('~/.trading_bot_keys.env'))

def test_connection():
    """Test Coinbase API connection"""
    print("=" * 60)
    print("Coinbase Advanced Trade API - Connection Test")
    print("=" * 60)
    print()

    # Check credentials
    api_key = os.getenv('CB_API_KEY')
    api_secret = os.getenv('CB_API_SECRET')
    api_passphrase = os.getenv('CB_API_PASSPHRASE')

    print("[1/4] Checking API credentials...")
    if not all([api_key, api_secret, api_passphrase]):
        print(" ✗ Missing API credentials")
        print(" Edit: nano ~/.trading_bot_keys.env")
        return False

    print(" ✓ API credentials found")
    print(f" - Key: {api_key[:10]}...{api_key[-5:]}")
    print()

    # Test Python imports
    print("[2/4] Checking Python libraries...")
    try:
        import requests
        print(" ✓ Required libraries available")
    except ImportError as e:
        print(f" ✗ Missing library: {e}")
        return False

    print()

    # Test API connectivity
    print("[3/4] Testing API connectivity...")
    try:
        # Create signature for Coinbase API
        method = 'GET'
        request_path = '/api/v3/accounts'
        body = ''
        timestamp = str(int(time.time()))
        message = timestamp + method + request_path + body

        signature = base64.b64encode(
            hmac.new(
                api_secret.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
        ).decode()

        headers = {
            'CB-ACCESS-KEY': api_key,
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-PASSPHRASE': api_passphrase,
            'Content-Type': 'application/json'
        }

        response = requests.get(
            'https://api.coinbase.com' + request_path,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print(" ✓ Successfully connected to Coinbase API")
            accounts = response.json()
            print(f" ✓ Retrieved {len(accounts)} account(s)")
        elif response.status_code == 401:
            print(" ✗ Authentication failed (401)")
            print(" Check: API key, secret, passphrase, IP whitelist")
            return False
        else:
            print(f" ✗ API Error: {response.status_code}")
            print(f" {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f" ✗ Connection failed: {e}")
        return False

    print()

    # List accounts
    print("[4/4] Account Information...")
    try:
        for account in accounts:
            currency = account.get('currency', 'N/A')
            balance = account.get('available_balance', {})
            amount = balance.get('amount', '0')
            print(f" {currency}: {amount} {balance.get('currency', currency)}")
    except:
        print(" (Unable to parse account data)")

    print()
    print("=" * 60)
    print("✓ All tests passed! API is working correctly.")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
