# Trading Bot - Binance Futures Testnet

A Python application for placing orders on Binance Futures Testnet (USDT-M) with a clean, reusable structure, comprehensive logging, and robust error handling.

## Features

✅ **Core Functionality**
- Place MARKET and LIMIT orders on Binance Futures Testnet
- Support for BUY and SELL sides
- CLI interface for easy order placement
- Structured, reusable code architecture
- Comprehensive logging and error handling
- Input validation and user-friendly error messages

✅ **Project Structure**
```
trading_bot/
├── __init__.py
├── client.py          # Binance API client wrapper
├── orders.py          # Order placement logic
├── validators.py      # Input validation
└── logging_config.py  # Logging configuration

cli.py                # CLI entry point
README.md
requirements.txt
logs/                # Log files directory
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- pip package manager

### 2. Binance Futures Testnet Account
1. Register at: https://testnet.binancefuture.com
2. Complete account verification
3. Generate API Key and Secret:
   - Go to Account Settings → API Management
   - Create a new API key
   - Copy the API Key and Secret

### 3. Installation

```bash
# Clone the repository
git clone https://github.com/Nakul-Narang/trading-bot-assignment.git
cd trading-bot-assignment

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET_URL=https://testnet.binancefuture.com
```

## Usage

### Running the CLI

```bash
python cli.py --help
```

### Place a Market Order

```bash
# BUY 1 BTC at market price
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 1

# SELL 0.5 ETH at market price
python cli.py --symbol ETHUSDT --side SELL --order-type MARKET --quantity 0.5
```

### Place a Limit Order

```bash
# BUY 1 BTC at 50,000 USDT
python cli.py --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 1 --price 50000

# SELL 0.5 ETH at 3,000 USDT
python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.5 --price 3000
```

### Command Options

```
Options:
  --symbol TEXT           Trading pair (e.g., BTCUSDT)               [required]
  --side TEXT             BUY or SELL                               [required]
  --order-type TEXT       MARKET or LIMIT                           [required]
  --quantity FLOAT        Order quantity                            [required]
  --price FLOAT           Price for LIMIT orders                    [optional]
  --help                  Show this message and exit
```

## Logging

All API interactions, responses, and errors are logged to `logs/trading_bot.log`

Log levels:
- **DEBUG**: Detailed information for debugging
- **INFO**: General information about order operations
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failed operations
- **CRITICAL**: Critical errors that stop execution

## Examples

### Example 1: Place a Market BUY Order
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

**Output:**
```
╔════════════════════════════════════════════════╗
║           ORDER PLACEMENT SUMMARY              ║
╚════════════════════════════════════════════════╝

Request Details:
  Symbol: BTCUSDT
  Side: BUY
  Type: MARKET
  Quantity: 0.01

Response Details:
  Order ID: 12345678
  Status: FILLED
  Executed Quantity: 0.01
  Average Price: 45,200.00 USDT

✓ Order placed successfully!
```

### Example 2: Place a Limit SELL Order
```bash
python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.5 --price 2500
```

## Error Handling

The application handles:
- Invalid input parameters
- Missing API credentials
- Network failures
- API errors and rate limiting
- Invalid trading pairs
- Insufficient balance
- Invalid order parameters

All errors are logged and displayed to the user with clear error messages.

## Architecture

### `client.py`
Wrappes Binance Futures API with:
- Authentication
- Request signing
- Error handling
- Response parsing

### `orders.py`
Contains order placement logic:
- Market order execution
- Limit order execution
- Order validation
- Response formatting

### `validators.py`
Validates user input:
- Symbol validation
- Side validation (BUY/SELL)
- Order type validation (MARKET/LIMIT)
- Quantity and price validation

### `logging_config.py`
Configures logging:
- File and console handlers
- Log formatting
- Log level management

## Assumptions

1. The Binance Futures Testnet API follows the same structure as the mainnet API
2. API credentials are valid and have appropriate permissions
3. Network connectivity is available for API calls
4. Trading pairs exist on Binance Futures Testnet (BTCUSDT, ETHUSDT, etc.)
5. User input is case-insensitive (converted to uppercase)
6. Default leverage is set to 1x in testnet account

## Testing

The application includes sample log files demonstrating:
- Successful MARKET order placement
- Successful LIMIT order placement
- Error handling and logging

Check `logs/` directory for example logs.

## Troubleshooting

**Q: "Invalid API credentials" error**
- Verify API Key and Secret are correct in `.env`
- Ensure credentials are for Futures Testnet, not Spot or Mainnet

**Q: "Connection refused" error**
- Check internet connectivity
- Verify testnet URL is correct: https://testnet.binancefuture.com

**Q: "Insufficient balance" error**
- Add USDT to your testnet account balance
- Check account on: https://testnet.binancefuture.com/en/futures/usdt/dashboard

**Q: Order not executing (LIMIT orders)**
- Ensure price is within reasonable range
- Check current market price on testnet

## Resources

- [Binance Futures Testnet](https://testnet.binancefuture.com)
- [Binance Futures API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- [python-binance Documentation](https://python-binance.readthedocs.io/)

## License

MIT
