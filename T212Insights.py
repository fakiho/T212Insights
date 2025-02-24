"""
title: T212 Insights Assistant
description: Integration with Trading212 brokerage API for account management and trading
author: @fakiho
author_url: https://github.com/fakiho
version: 1.0.0
license: MIT
requirements:
    - diskcache
    - httpx>=0.27.0
    - pydantic>=2.5.2
    - cachetools>=4.2.4
"""

import logging
from pydantic import BaseModel, Field
import httpx
from typing import Union, Dict, Union, Any, List, Callable, Awaitable
from datetime import datetime
import diskcache
from cachetools.keys import hashkey

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("trading212.log"), logging.StreamHandler()],
)
logger = logging.getLogger("Trading212Tool")

api_cache = diskcache.Cache("./api_cache")


def format_order_info(json_data):
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    formatted_orders = []
    for item in data.get("items", []):
        order_info = (
            f"Order ID: {item['id']}\n"
            f"Ticker: {item['ticker']}\n"
            f"Status: {item['status']}\n"
            f"Type: {item['type']}\n"
            f"Ordered Quantity: {item['orderedQuantity']}\n"
            f"Filled Quantity: {item['filledQuantity']}\n"
            f"Limit Price: {item['limitPrice']}\n"
            f"Stop Price: {item['stopPrice']}\n"
            f"Filled Price: {item['fillPrice']}\n"
            f"Execution Time: {item['dateExecuted']}\n"
            f"Time Validity: {item['timeValidity']}\n"
            "-"
        )
        formatted_orders.append(order_info)

    return "\n".join(formatted_orders) if formatted_orders else "No orders found."


def extract_position_info(item):
    """Extracts and formats a single position's information."""
    return (
        f"Ticker: {item['ticker']}\n"
        f"Quantity: {item['quantity']}\n"
        f"Average Price: {item['averagePrice']}\n"
        f"Current Price: {item['currentPrice']}\n"
        f"Profit/Loss: {item['ppl']}\n"
        f"FX Profit/Loss: {item['fxPpl']}\n"
        f"Initial Fill Date: {item['initialFillDate']}\n"
        "-"
    )


def format_positions_info(json_data):
    """Iterates over the JSON array and formats all positions."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    formatted_positions = [extract_position_info(item) for item in data]

    return (
        "\n".join(formatted_positions)
        if formatted_positions
        else "No open positions found."
    )


def extract_open_order_info(item):
    """Extracts and formats a single open order's information."""
    return (
        f"Order ID: {item['id']}\n"
        f"Status: {item['status']}\n"
        f"Progress: {item['progress'] * 100}%\n"
        f"Cash: {item['cash']}\n"
        f"Dividend Gained: {item['dividendDetails']['gained']}\n"
        f"Dividend in Cash: {item['dividendDetails']['inCash']}\n"
        f"Dividend Reinvested: {item['dividendDetails']['reinvested']}\n"
        f"Avg Invested Value: {item['result']['priceAvgInvestedValue']}\n"
        f"Avg Result: {item['result']['priceAvgResult']}\n"
        f"Avg Result Coefficient: {item['result']['priceAvgResultCoef']}\n"
        f"Avg Value: {item['result']['priceAvgValue']}\n"
        "-"
    )


def format_open_orders_info(json_data):
    """Iterates over the JSON array and formats all open orders."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    formatted_orders = [extract_open_order_info(item) for item in data]

    return "\n".join(formatted_orders) if formatted_orders else "No open orders found."


import json


def format_order_info(json_data):
    """Extracts and formats order information from the provided JSON data."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    formatted_orders = []
    for item in data.get("items", []):
        order_info = (
            f"Order ID: {item['id']}\n"
            f"Ticker: {item['ticker']}\n"
            f"Status: {item['status']}\n"
            f"Type: {item['type']}\n"
            f"Ordered Quantity: {item['orderedQuantity']}\n"
            f"Filled Quantity: {item['filledQuantity']}\n"
            f"Limit Price: {item['limitPrice']}\n"
            f"Stop Price: {item['stopPrice']}\n"
            f"Filled Price: {item['fillPrice']}\n"
            f"Execution Time: {item['dateExecuted']}\n"
            f"Time Validity: {item['timeValidity']}\n"
            "-"
        )
        formatted_orders.append(order_info)

    return "\n".join(formatted_orders) if formatted_orders else "No orders found."


def extract_position_info(item):
    """Extracts and formats a single position's information."""
    return (
        f"Ticker: {item['ticker']}\n"
        f"Quantity: {item['quantity']}\n"
        f"Average Price: {item['averagePrice']}\n"
        f"Current Price: {item['currentPrice']}\n"
        f"Profit/Loss: {item['ppl']}\n"
        f"FX Profit/Loss: {item['fxPpl']}\n"
        f"Initial Fill Date: {item['initialFillDate']}\n"
        "-"
    )


def format_positions_info(json_data):
    """Iterates over the JSON array and formats all positions."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    formatted_positions = [extract_position_info(item) for item in data]

    return (
        "\n".join(formatted_positions)
        if formatted_positions
        else "No open positions found."
    )


def extract_open_order_info(item):
    """Extracts and formats a single open order's information."""
    return (
        f"Order ID: {item['id']}\n"
        f"Status: {item['status']}\n"
        f"Progress: {item['progress'] * 100}%\n"
        f"Cash: {item['cash']}\n"
        f"Dividend Gained: {item['dividendDetails']['gained']}\n"
        f"Dividend in Cash: {item['dividendDetails']['inCash']}\n"
        f"Dividend Reinvested: {item['dividendDetails']['reinvested']}\n"
        f"Avg Invested Value: {item['result']['priceAvgInvestedValue']}\n"
        f"Avg Result: {item['result']['priceAvgResult']}\n"
        f"Avg Result Coefficient: {item['result']['priceAvgResultCoef']}\n"
        f"Avg Value: {item['result']['priceAvgValue']}\n"
        "-"
    )


def format_open_orders_info(json_data):
    """Iterates over the JSON array and formats all open orders."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    formatted_orders = [extract_open_order_info(item) for item in data]

    return "\n".join(formatted_orders) if formatted_orders else "No open orders found."


def extract_instrument_info(item):
    """Extracts and formats a single instrument's information."""
    return (
        f"Name: {item['name']}\n"
        f"Short Name: {item['shortName']}\n"
        f"Ticker: {item['ticker']}\n"
        f"Type: {item['type']}\n"
        f"Currency: {item['currencyCode']}\n"
        f"ISIN: {item['isin']}\n"
        f"Max Open Quantity: {item['maxOpenQuantity']}\n"
        f"Min Trade Quantity: {item['minTradeQuantity']}\n"
        f"Added On: {item['addedOn']}\n"
        "-"
    )


def format_instruments_info(json_data):
    """Iterates over the JSON array and formats all instruments."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    formatted_instruments = [extract_instrument_info(item) for item in data]

    return (
        "\n".join(formatted_instruments)
        if formatted_instruments
        else "No instruments found."
    )


def extract_cash_info(item):
    """Extracts and formats cash balance information."""
    return (
        f"Blocked: {item['blocked']}\n"
        f"Free: {item['free']}\n"
        f"Invested: {item['invested']}\n"
        f"Pie Cash: {item['pieCash']}\n"
        f"Profit/Loss: {item['ppl']}\n"
        f"Result: {item['result']}\n"
        f"Total: {item['total']}\n"
        "-"
    )

def format_cash_info(json_data):
    """Formats the cash balance information."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data
    return extract_cash_info(data)

# PIE Extraction
def extract_dividend_details(dividend_details):
    """Formats dividend details."""
    return (
        f"Dividend Details:\n"
        f"  - Gained: {dividend_details['gained']}\n"
        f"  - Reinvested: {dividend_details['reinvested']}\n"
        f"  - In Cash: {dividend_details['inCash']}\n"
    )

def extract_pie_details(result):
    """Formats result details."""
    return (
        f"Result:\n"
        f"  - Price Avg Invested Value: {result['priceAvgInvestedValue']}\n"
        f"  - Price Avg Value: {result['priceAvgValue']}\n"
        f"  - Price Avg Result: {result['priceAvgResult']}\n"
        f"  - Price Avg Result Coef: {result['priceAvgResultCoef']:.4f}\n"
    )

def extract_pie(item):
    """Extracts and formats a single JSON object."""
    return (
        f"ID: {item['id']}\n"
        f"Cash: {item['cash']}\n"
        f"Progress: {item['progress']:.4f}\n"
        f"Status: {item['status']}\n"
        f"{extract_dividend_details(item['dividendDetails'])}"
        f"{extract_pie_details(item['result'])}"
    )

def extract_pie_array_content(json_data):
    """Extracts and formats the content of a JSON array."""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data
    return "\n".join(extract_pie(item) for item in data)


class Tools:
    class Valves(BaseModel):
        api_key: str = Field(
            "", description="Trading212 API key (36-character alphanumeric)"
        )
        demo_mode: bool = Field(True, description="Use demo trading environment")

    def __init__(self):
        try:
            self.valves = self.Valves()
            self.base_url = (
                "https://demo.trading212.com"
                if self.valves.demo_mode
                else "https://live.trading212.com"
            )
            self.headers = {"Authorization": self.valves.api_key}
            self.citation = False
            logger.info("Tool initialized successfully")
        except Exception as e:
            logger.error(f"Tool initialization failed: {str(e)}")
            raise

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Union[Dict[str, Union[int, str]]] = None,
        data: Union[Dict[str, Any]] = None,
        force_refresh: bool = False
    ) -> Dict[str, Any]:
        """Generic request handler with full type annotations"""
        # Normalize `params` to avoid cache misses due to empty vs. None
        params_tuple = tuple(sorted(params.items())) if params else ()
        cache_key = hashkey(method, endpoint, params_tuple)

        if not force_refresh and cache_key in api_cache:
            logger.info(f"Cache hit for {endpoint} with params {params}")
            return api_cache[cache_key]

        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = await client.request(
                    method,
                    f"{self.base_url}{endpoint}",
                    headers=self.headers,
                    params=params,
                    json=data,
                )
                response.raise_for_status()
                # Store in cache under lock
                api_cache.set(
                    cache_key, response.json(), expire=300
                )  # Store with TTL 5 min
                logger.info(
                    f"Stored in cache: {cache_key} | Cache size: {len(api_cache)}"
                )
                return response.json()
            except httpx.HTTPStatusError as e:
                return {
                    "error": f"API Error {e.response.status_code}",
                    "details": e.response.text,
                    "endpoint": endpoint,
                }
            except Exception as e:
                return {"error": str(e)}

    async def get_account_cash(
        self, __event_emitter__: Union[Callable[[Any], Awaitable[None]]] = None
    ) -> str:
        """
        Create a report of the account balance with full type hints.
        Create a detailed report of the account's cash holdings.
        :return: A comprehensive detailed info of the account's cash holdings as a formatted string.
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Fetching account cash balance",
                        "done": False,
                    },
                }
            )

        result = await self._make_request(
            "GET", "/api/v0/equity/account/cash"
        )
        currency = await self.get_account_meta()
        total = result["total"]
        ppl = result["ppl"]
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Retrieved total balance: {total}  PPL: {ppl}",
                        "done": True,
                    },
                }
            )

        formatted_cash = format_cash_info(result)
        return formatted_cash + " currency: " + currency

    async def get_account_meta(
        self, __event_emitter__: Union[Callable[[Any], Awaitable[None]]] = None
    ) -> str:
        """
        This will Get the current account's currency.
        :return: currency code as a formatted string.
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Fetching account cash balance",
                        "done": False,
                    },
                }
            )

        result = await self._make_request("GET", "/api/v0/equity/account/info")
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Retrieved account meta ",
                        "done": True,
                    },
                }
            )
        currencyCode = result["currencyCode"]
        return "Account Currency Code: " + currencyCode

    async def get_portfolio_positions(
        self, __event_emitter__: Union[Callable[[Any], Awaitable[None]]] = None
    ) -> str:
        """
        This will get List of the current open positions in the portfolio.
        Create a list of the current open position with detailed explained.
        :return: A comprehensive List of the portfolio as a formatted string.
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Fetching portfolio positions",
                        "done": False,
                    },
                }
            )

        result = await self._make_request("GET", "/api/v0/equity/portfolio")

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Found {len(result)} positions",
                        "done": True,
                    },
                }
            )

        portfoloio_positions = format_positions_info(result)
        return portfoloio_positions

    async def get_specific_positions(
        self,
        ticker: str,
        __event_emitter__: Union[Callable[[Any], Awaitable[None]]] = None,
    ) -> str:
        """
        Search/find an open position in profolio by a ticker with proper nested typing 
        :param ticker: The ticker symbol of the instrument to get positions for like `AAPL_US_EQ`.
        :return: A comprehensive analysis report of the portfolio as a formatted string.
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Fetching portfolio positions",
                        "done": False,
                    },
                }
            )

        result = await self._make_request(
            "GET", "/api/v0/equity/portfolio/" + str(ticker)
        )

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Found {len(result)} positions",
                        "done": True,
                    },
                }
            )
        portfoloio_position = extract_position_info(result)
        return portfoloio_position

    async def get_order_history(
        self,
        limit: int = 20,
        cursor: Union[int] = 0,
        __event_emitter__: Union[Callable[[Any], Awaitable[None]]] = None,
    ) -> str:
        """
        Get a Historical orders with pagination typing
        :param limit: The number of orders to fetch.
        :param cursor: The cursor for pagination.
        :return: A comprehensive analysis report of the order history as a formatted string.
        """
        params: Dict[str, Union[int, str]] = {"limit": limit}
        if cursor:
            params["cursor"] = cursor

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": "Fetching order history", "done": False},
                }
            )

        result = await self._make_request(
            "GET", "/api/v0/equity/history/orders", params=params
        )

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Retrieved {len(result.get('items', []))} orders",
                        "done": True,
                    },
                }
            )
        formatted_orders = format_order_info(result)
        return formatted_orders

    async def get_instruments(
        self, __event_emitter__: Union[Callable[[Any], Awaitable[None]]] = None
    ) -> str:
        """
        fetxch/search an Instruments list with detailed information.
        Create a list of the tradable instruments with detailed information.
        :return: A comprehensive list of the instruments as a formatted string
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Fetching tradable instruments",
                        "done": False,
                    },
                }
            )

        result = await self._make_request("GET", "/api/v0/equity/metadata/instruments")

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Found {len(result)} instruments",
                        "done": True,
                    },
                }
            )
        formatted_instruments = format_instruments_info(result)
        return formatted_instruments

    async def get_instrument_by_name(
        self,
        search_term: str,
        shortname: str,
        __event_emitter__: Union[Callable[[Any], Awaitable[None]]] = None,
    ) -> str:
        """
        Fetches a specific instrument by name or shortName.
        :param search_term: The name of the instrument.
        :param shortname: The shortName of the instrument.
        :return: The formatted string of the matching instrument(s).
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Searching for instrument: {search_term}",
                        "done": False,
                    },
                }
            )

        result = await self._make_request("GET", "/api/v0/equity/metadata/instruments")

        logger.info(f"searching for instrument: {search_term}, {shortname}")
        # Filter instruments based on name or shortName
        matching_instruments = [
            instrument
            for instrument in result
            if search_term.lower() in instrument["name"].lower()
            and shortname.lower() in instrument["shortName"].lower()
        ]

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Found {len(matching_instruments)} matching instruments",
                        "done": True,
                    },
                }
            )
        logger.info(f"Found {len(result)} matching instruments for '{search_term}'")

        return (
            format_instruments_info(matching_instruments)
            if matching_instruments
            else f"No instruments found for '{search_term}'."
        )
    

    async def getAllPies(
        self,
        __event_emitter__: Union[Callable[[Any], Awaitable[None]]] = None,
    ) -> str:
        """
        Fetches all the pies in the account.
        A pie is a collection of securities - stocks & ETFs.
        Each security is represented as a slice of the pie. Each pie can hold up to 50 securities. You can have multiple pies.
        :return: The formatted string of the existing pie(s) and the dividend(s).
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Fetching all pies",
                        "done": False,
                    },
                }
            )

        result = await self._make_request("GET", "/api/v0/equity/pies")

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Found {len(result)} Pie/s",
                        "done": True,
                    },
                }
            )
        return (
            extract_pie_array_content(result)
            if result
            else f"No pies found."
        )
