"""Binance Futures API client wrapper."""

import hashlib
import hmac
import logging
import time
from typing import Dict, Optional

import requests

from trading_bot.logging_config import get_logger


class BinanceAPIError(Exception):
    """Custom exception for Binance API errors."""

    pass


class BinanceClient:
    """Wrapper for Binance Futures Testnet API."""

    def __init__(self, api_key: str, api_secret: str, base_url: str = None):
        """
        Initialize Binance client.

        Args:
            api_key: Binance API key.
            api_secret: Binance API secret.
            base_url: Base URL for API calls (defaults to testnet).

        Raises:
            ValueError: If API credentials are missing.
        """
        if not api_key or not api_secret:
            raise ValueError("API key and secret are required")

        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url or "https://testnet.binancefuture.com"
        self.logger = get_logger()
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _get_timestamp(self) -> int:
        """
        Get current timestamp in milliseconds.

        Returns:
            Current timestamp in milliseconds.
        """
        return int(time.time() * 1000)

    def _sign_request(self, params: Dict) -> Dict:
        """
        Sign request parameters with API secret.

        Args:
            params: Request parameters.

        Returns:
            Parameters with signature added.
        """
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode(), query_string.encode(), hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        signed: bool = False,
    ) -> Dict:
        """
        Make an API request.

        Args:
            method: HTTP method (GET, POST, etc.).
            endpoint: API endpoint (e.g., /fapi/v1/order).
            params: Request parameters.
            signed: Whether the request needs to be signed.

        Returns:
            Response JSON data.

        Raises:
            BinanceAPIError: If the API request fails.
        """
        url = f"{self.base_url}{endpoint}"
        params = params or {}

        if signed:
            params["timestamp"] = self._get_timestamp()
            params = self._sign_request(params)

        self.logger.debug(f"Making {method} request to {endpoint} with params: {params}")

        try:
            response = self.session.request(method, url, params=params)
            response.raise_for_status()
            data = response.json()
            self.logger.debug(f"Response from {endpoint}: {data}")
            return data
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: {str(e)}"
            self.logger.error(error_msg)
            raise BinanceAPIError(error_msg)
        except requests.exceptions.Timeout as e:
            error_msg = f"Request timeout: {str(e)}"
            self.logger.error(error_msg)
            raise BinanceAPIError(error_msg)
        except requests.exceptions.HTTPError as e:
            try:
                error_data = response.json()
                error_msg = f"API error ({response.status_code}): {error_data.get('msg', str(e))}"
            except:
                error_msg = f"HTTP error {response.status_code}: {str(e)}"
            self.logger.error(error_msg)
            raise BinanceAPIError(error_msg)
        except ValueError as e:
            error_msg = f"Invalid JSON response: {str(e)}"
            self.logger.error(error_msg)
            raise BinanceAPIError(error_msg)

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Dict:
        """
        Place an order on Binance Futures.

        Args:
            symbol: Trading pair (e.g., BTCUSDT).
            side: BUY or SELL.
            order_type: MARKET or LIMIT.
            quantity: Order quantity.
            price: Price (required for LIMIT orders).

        Returns:
            Order response from API.

        Raises:
            BinanceAPIError: If the order placement fails.
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            if price is None:
                raise BinanceAPIError("Price is required for LIMIT orders")
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good till canceled

        self.logger.info(
            f"Placing {order_type} {side} order for {quantity} {symbol} at price {price or 'market price'}"
        )

        try:
            response = self._make_request(
                "POST", "/fapi/v1/order", params=params, signed=True
            )
            self.logger.info(f"Order placed successfully: {response}")
            return response
        except BinanceAPIError as e:
            self.logger.error(f"Failed to place order: {str(e)}")
            raise

    def get_account_info(self) -> Dict:
        """
        Get account information.

        Returns:
            Account information from API.

        Raises:
            BinanceAPIError: If the request fails.
        """
        self.logger.debug("Fetching account information")
        try:
            response = self._make_request("GET", "/fapi/v2/account", signed=True)
            return response
        except BinanceAPIError as e:
            self.logger.error(f"Failed to fetch account info: {str(e)}")
            raise

    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """
        Get order status.

        Args:
            symbol: Trading pair.
            order_id: Order ID.

        Returns:
            Order information from API.

        Raises:
            BinanceAPIError: If the request fails.
        """
        params = {"symbol": symbol, "orderId": order_id}
        self.logger.debug(f"Fetching order status: {params}")
        try:
            response = self._make_request(
                "GET", "/fapi/v1/order", params=params, signed=True
            )
            return response
        except BinanceAPIError as e:
            self.logger.error(f"Failed to fetch order status: {str(e)}")
            raise
