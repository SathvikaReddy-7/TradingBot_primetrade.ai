from binance.client import Client
from binance.enums import *
import logging
import sys
import os

# Ensure logs folder exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(filename='logs/trading_bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class BasicSpotBot:
    def __init__(self, api_key, api_secret):
        # Initialize Binance Client
        self.client = Client(api_key, api_secret)
        # Force API URL to Spot Testnet
        self.client.API_URL = 'https://testnet.binance.vision/api'
        logging.info("Initialized Binance Spot Testnet Client")
        print("✅ Connected to Binance Spot Testnet")

        # Optional: Test API key by fetching account info
        try:
            account_info = self.client.get_account()
            logging.info("Account information retrieved successfully")
            print("👤 Account Info fetched. API key is valid.")
        except Exception as e:
            logging.error(f"Error fetching account info: {str(e)}")
            print("❌ Error validating API key:", str(e))
            sys.exit(1)  # Exit if API key is invalid

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == 'MARKET':
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_LIMIT,
                    quantity=quantity,
                    price=price,
                    timeInForce=TIME_IN_FORCE_GTC
                )
            else:
                raise ValueError("Unsupported order type")

            logging.info(f"Order placed: {order}")
            print("✅ Order placed successfully:", order)
        except Exception as e:
            logging.error(f"Error placing order: {str(e)}")
            print("❌ Error placing order:", str(e))


def main():
    # Get API credentials from user
    api_key = input("Enter your Binance API Key: ").strip()
    api_secret = input("Enter your Binance API Secret: ").strip()

    bot = BasicSpotBot(api_key, api_secret)

    # User input for trade
    symbol = input("Enter trading pair (e.g., BTCUSDT): ").strip().upper()
    side = input("Enter side (BUY/SELL): ").strip().upper()
    order_type = input("Enter order type (MARKET/LIMIT): ").strip().upper()
    quantity = float(input("Enter quantity: "))

    price = None
    if order_type == 'LIMIT':
        price = float(input("Enter limit price: "))

    bot.place_order(symbol, side, order_type, quantity, price)


if __name__ == "__main__":
    main()
