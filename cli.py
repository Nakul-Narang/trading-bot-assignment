"""CLI interface for trading bot."""

import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv

from trading_bot.client import BinanceAPIError, BinanceClient
from trading_bot.logging_config import setup_logging
from trading_bot.orders import OrderProcessor
from trading_bot.validators import ValidationError

# Setup
load_dotenv()
setup_logging()
console = Console()
app = typer.Typer(help="Trading Bot CLI for Binance Futures Testnet")


def get_client() -> BinanceClient:
    """
    Initialize Binance client from environment variables.

    Returns:
        Configured BinanceClient instance.

    Raises:
        ValueError: If API credentials are missing.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    testnet_url = os.getenv("BINANCE_TESTNET_URL", "https://testnet.binancefuture.com")

    if not api_key or not api_secret:
        console.print(
            "[red]Error: Missing API credentials![/red]\n"
            "Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file",
            style="bold",
        )
        raise ValueError("API credentials not configured")

    return BinanceClient(api_key, api_secret, testnet_url)


def display_order_summary(formatted_response: dict) -> None:
    """
    Display formatted order summary to user.

    Args:
        formatted_response: Formatted order response from OrderProcessor.
    """
    request = formatted_response["request"]
    response = formatted_response["response"]

    # Create request table
    request_table = Table(title="Request Details", show_header=False)
    request_table.add_row("Symbol", request["symbol"])
    request_table.add_row("Side", request["side"])
    request_table.add_row("Type", request["type"])
    request_table.add_row("Quantity", str(request["quantity"]))
    if request["price"]:
        request_table.add_row("Price", f"{request['price']:.2f} USDT")

    # Create response table
    response_table = Table(title="Response Details", show_header=False)
    response_table.add_row("Order ID", str(response["order_id"]))
    response_table.add_row("Status", response["status"])
    response_table.add_row("Executed Quantity", response["executed_quantity"])
    if response["average_price"]:
        response_table.add_row("Average Price", f"{float(response['average_price']):.2f} USDT")
    if response["commission"]:
        response_table.add_row(
            "Commission",
            f"{response['commission']} {response['commission_asset']}",
        )

    # Display summary
    console.print("\n")
    summary_panel = Panel(
        "[bold cyan]ORDER PLACEMENT SUMMARY[/bold cyan]",
        expand=False,
        border_style="blue",
    )
    console.print(summary_panel)
    console.print(request_table)
    console.print(response_table)
    console.print("\n[bold green]✓ Order placed successfully![/bold green]\n")


@app.command()
def place_order(
    symbol: str = typer.Option(
        ..., "--symbol", help="Trading pair (e.g., BTCUSDT)", prompt=False
    ),
    side: str = typer.Option(
        ..., "--side", help="BUY or SELL", prompt=False
    ),
    order_type: str = typer.Option(
        ..., "--order-type", help="MARKET or LIMIT", prompt=False
    ),
    quantity: float = typer.Option(
        ..., "--quantity", help="Order quantity", prompt=False
    ),
    price: Optional[float] = typer.Option(
        None, "--price", help="Price for LIMIT orders", prompt=False
    ),
) -> None:
    """
    Place an order on Binance Futures Testnet.

    Examples:
        # Place a market BUY order
        python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01

        # Place a limit SELL order
        python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.5 --price 2500
    """
    try:
        # Initialize client and processor
        client = get_client()
        processor = OrderProcessor(client)

        # Place order
        console.print("\n[yellow]Processing order...[/yellow]")
        formatted_response = processor.place_order(
            symbol=symbol, side=side, order_type=order_type, quantity=quantity, price=price
        )

        # Display success
        display_order_summary(formatted_response)

    except ValueError as e:
        console.print(f"[red]Configuration Error:[/red] {str(e)}", style="bold")
        sys.exit(1)
    except ValidationError as e:
        console.print(f"[red]Validation Error:[/red] {str(e)}", style="bold")
        sys.exit(1)
    except BinanceAPIError as e:
        console.print(f"[red]API Error:[/red] {str(e)}", style="bold")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected Error:[/red] {str(e)}", style="bold")
        sys.exit(1)


if __name__ == "__main__":
    app()
