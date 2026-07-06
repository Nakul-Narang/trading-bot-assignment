"""Order placement logic and formatting."""

from typing import Dict, Optional

from trading_bot.client import BinanceAPIError, BinanceClient
from trading_bot.logging_config import get_logger
from trading_bot.validators import OrderValidator, ValidationError


class OrderProcessor:
    """Processes and places orders."""

    def __init__(self, client: BinanceClient):
        """
        Initialize order processor.

        Args:
            client: Binance API client instance.
        """
        self.client = client
        self.logger = get_logger()
        self.validator = OrderValidator()

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Dict:
        """
        Place an order after validation.

        Args:
            symbol: Trading pair.
            side: BUY or SELL.
            order_type: MARKET or LIMIT.
            quantity: Order quantity.
            price: Price for LIMIT orders.

        Returns:
            Formatted order response.

        Raises:
            ValidationError: If validation fails.
            BinanceAPIError: If the API call fails.
        """
        # Validate inputs
        validated_symbol, validated_side, validated_type, validated_qty, validated_price = (
            self.validator.validate_order(
                symbol, side, order_type, quantity, price
            )
        )

        self.logger.info(
            f"Order validation passed: {validated_symbol} {validated_side} {validated_type} {validated_qty}"
        )

        # Place order via API
        order_response = self.client.place_order(
            validated_symbol,
            validated_side,
            validated_type,
            validated_qty,
            validated_price,
        )

        return self._format_order_response(
            validated_symbol,
            validated_side,
            validated_type,
            validated_qty,
            validated_price,
            order_response,
        )

    @staticmethod
    def _format_order_response(
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float],
        api_response: Dict,
    ) -> Dict:
        """
        Format API response into user-friendly format.

        Args:
            symbol: Trading pair.
            side: BUY or SELL.
            order_type: MARKET or LIMIT.
            quantity: Order quantity.
            price: Order price.
            api_response: Raw API response.

        Returns:
            Formatted response dictionary.
        """
        return {
            "request": {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity,
                "price": price,
            },
            "response": {
                "order_id": api_response.get("orderId"),
                "status": api_response.get("status"),
                "executed_quantity": api_response.get("executedQty"),
                "average_price": api_response.get("avgPrice"),
                "commission": api_response.get("commission"),
                "commission_asset": api_response.get("commissionAsset"),
                "timestamp": api_response.get("time"),
                "raw_response": api_response,
            },
        }

    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """
        Get status of an existing order.

        Args:
            symbol: Trading pair.
            order_id: Order ID.

        Returns:
            Order status information.

        Raises:
            BinanceAPIError: If the API call fails.
        """
        return self.client.get_order_status(symbol, order_id)

    def get_account_info(self) -> Dict:
        """
        Get account information.

        Returns:
            Account information.

        Raises:
            BinanceAPIError: If the API call fails.
        """
        return self.client.get_account_info()
