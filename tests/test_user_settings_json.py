from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from src.user_settings_json import get_currency_rates, get_price_stocks


@patch("src.user_settings_json.requests.get")
def test_get_currency_rates(mock_get: MagicMock) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "success": True,
        "query": {"from": "USD", "to": "RUB", "amount": "1"},
        "info": {"timestamp": 1726849624, "rate": 92.349211},
        "date": "2024-09-20",
        "result": 92.349211,
    }
    result = get_currency_rates()
    assert result == [{"currency": "USD", "rate": 92.349211}, {"currency": "EUR", "rate": 92.349211}]


@patch("src.user_settings_json.requests.get")
def test_get_currency_rates_invalid_api(mock_get: MagicMock) -> None:
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {"message": "Invalid authentication credentials"}
    result = get_currency_rates()
    assert result == [{'currency': 'USD', 'rate': None}, {'currency': 'EUR', 'rate': None}]


@patch("src.user_settings_json.requests.get")
def test_get_price_stocks(mock_get: MagicMock) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{'price': 145.775, 'stock': 'AAPL'},
 {'price': 145.775, 'stock': 'AMZN'},
 {'price': 145.775, 'stock': 'GOOGL'},
 {'price': 145.775, 'stock': 'MSFT'},
 {'price': 145.775, 'stock': 'TSLA'}]
    result = get_price_stocks()
    assert result == [{'price': 145.775, 'stock': 'AAPL'},
 {'price': 145.775, 'stock': 'AMZN'},
 {'price': 145.775, 'stock': 'GOOGL'},
 {'price': 145.775, 'stock': 'MSFT'},
 {'price': 145.775, 'stock': 'TSLA'}]


@patch("src.user_settings_json.requests.get")
def test_get_price_stocks_invalid_api(mock_get: MagicMock) -> None:
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {
        "Error Message": "Invalid API KEY. Feel free to create a Free API Key or visit "
        "https://site.financialmodelingprep.com/faqs?search=why-is-my-api-key-invalid for more information."
    }
    result = get_price_stocks()
    assert result == [{'price': None, 'stock': 'AAPL'},
 {'price': None, 'stock': 'AMZN'},
 {'price': None, 'stock': 'GOOGL'},
 {'price': None, 'stock': 'MSFT'},
 {'price': None, 'stock': 'TSLA'}]