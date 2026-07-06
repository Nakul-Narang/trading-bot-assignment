"""Input validation for trading bot."""

from typing import Tuple


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


class OrderValidator:
    """Validates order parameters."""

    VALID_SIDES = ["BUY", "SELL"]
    VALID_ORDER_TYPES = ["MARKET", "LIMIT"]

    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """
        Validate trading symbol.

        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT).

        Returns:
            Uppercase symbol.

        Raises:
            ValidationError: If symbol is invalid.
        """
        if not symbol or not isinstance(symbol, str):
            raise ValidationError("Symbol must be a non-empty string")

        symbol = symbol.upper().strip()

        if len(symbol) < 6:
            raise ValidationError(
                f"Symbol '{symbol}' is too short. Expected format: BTCUSDT, ETHUSDT, etc."
            )

        if not symbol.replace("", "").isalpha():
            raise ValidationError(f"Symbol '{symbol}' contains invalid characters")

        return symbol

    @staticmethod
    def validate_side(side: str) -> str:
        """
        Validate order side.

        Args:
            side: Order side (BUY or SELL).

        Returns:
            Uppercase side.

        Raises:
            ValidationError: If side is invalid.
        """
        if not side or not isinstance(side, str):
            raise ValidationError("Side must be a non-empty string")

        side = side.upper().strip()

        if side not in OrderValidator.VALID_SIDES:
            raise ValidationError(
                f"Side must be BUY or SELL, got '{side}'."
            )

        return side

    @staticmethod
    def validate_order_type(order_type: str) -> str:
        """
        Validate order type.

        Args:
            order_type: Order type (MARKET or LIMIT).

        Returns:
            Uppercase order type.

        Raises:
            ValidationError: If order type is invalid.
        """
        if not order_type or not isinstance(order_type, str):
            raise ValidationError("Order type must be a non-empty string")

        order_type = order_type.upper().strip()

        if order_type not in OrderValidator.VALID_ORDER_TYPES:
            raise ValidationError(
                f"Order type must be MARKET or LIMIT, got '{order_type}'."
            )

        return order_type

    @staticmethod
    def validate_quantity(quantity: float) -> float:
        """
        Validate order quantity.

        Args:
            quantity: Order quantity.

        Returns:
            Validated quantity.

        Raises:
            ValidationError: If quantity is invalid.
        """
        try:
            qty = float(quantity)
        except (ValueError, TypeError):
            raise ValidationError(f"Quantity must be a number, got '{quantity}'")

        if qty <= 0:
            raise ValidationError(f"Quantity must be positive, got '{qty}'")

        return qty

    @staticmethod
    def validate_price(price: float, order_type: str) -> float:
        """
        Validate order price.

        Args:
            price: Order price.
            order_type: Type of order (MARKET or LIMIT).

        Returns:
            Validated price.

        Raises:
            ValidationError: If price is invalid.
        """
        if order_type == "MARKET":
            return None  # Price not needed for market orders

        if price is None:
            raise ValidationError(f"Price is required for {order_type} orders")

        try:
            p = float(price)
        except (ValueError, TypeError):
            raise ValidationError(f"Price must be a number, got '{price}'")

        if p <= 0:
            raise ValidationError(f"Price must be positive, got '{p}'")

        return p

    @classmethod
    def validate_order(
        cls, symbol: str, side: str, order_type: str, quantity: float, price: float = None
    ) -> Tuple[str, str, str, float, float]:
        """
        Validate all order parameters.

        Args:
            symbol: Trading pair symbol.
            side: Order side (BUY or SELL).
            order_type: Order type (MARKET or LIMIT).
            quantity: Order quantity.
            price: Order price (required for LIMIT orders).

        Returns:
            Tuple of validated (symbol, side, order_type, quantity, price).

        Raises:
            ValidationError: If any parameter is invalid.
        """
        validated_symbol = cls.validate_symbol(symbol)
        validated_side = cls.validate_side(side)
        validated_order_type = cls.validate_order_type(order_type)
        validated_quantity = cls.validate_quantity(quantity)
        validated_price = cls.validate_price(price, validated_order_type)

        return (
            validated_symbol,
            validated_side,
            validated_order_type,
            validated_quantity,
            validated_price,
        )
