import os
from typing import Any

import requests
from dotenv import load_dotenv
from pathlib import Path
import logging


settings = {
    "user_currencies": ["USD", "EUR"],
    "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
}


BASE_DIR = Path(__file__).resolve().parent.parent
filename = BASE_DIR / ".env"
PATH_USER_SETTINGS_LOG = BASE_DIR / "logs" / "user_settings.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s",
    filename=PATH_USER_SETTINGS_LOG,
    filemode="w",
    encoding="utf-8",
)

USER_SETTINGS_LOG = logging.getLogger(__name__)


load_dotenv(dotenv_path=filename)
API_KEY_CURRENCIES = os.getenv("API_KEY_CURRENCIES")
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
headers = {"apikey": API_KEY_CURRENCIES}
payload = {}

currency_stock = []


def get_currency_rates() -> list[dict]:
    """Функция принимает список с кодами валют,
    а возвращает список словарей с текущими курсами"""
    currency_list = []
    for currency in settings["user_currencies"]:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"
        USER_SETTINGS_LOG.info(f"Запрос курса валюты {currency}")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            USER_SETTINGS_LOG.info("Успешный запрос")
            result = response.json()
            ruble_cost = result["result"]
            currency_list.append({"currency": currency, "rate": ruble_cost})
        else:
            USER_SETTINGS_LOG.warning(f"Ошибка: {response.status_code}, {response.text}")
            print(f"Ошибка: {response.status_code}, {response.text}")
            currency_list.append({"currency": currency, "rate": None})
    USER_SETTINGS_LOG.info("Курсы валют созданы")
    return currency_list


def get_price_stocks() -> list[dict]:
    """Функция принимает список с кодами компаний
    и возвращает список словарей со стоимостью акций каждой компании"""
    price_stocks = []
    for stock in settings["user_stocks"]:
        url = f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey={API_KEY_STOCK}"
        USER_SETTINGS_LOG.info(f"Запрос стоимости акций компании {stock}")
        response = requests.get(url)
        if response.status_code == 200:
            USER_SETTINGS_LOG.info("Успешный запрос")
            result = response.json()
            price = result[0]["price"]
            price_stocks.append({"stock": stock, "price": price})
        else:
            USER_SETTINGS_LOG.warning(f"Ошибка: {response.status_code}, {response.text}")
            print(f"Ошибка: {response.status_code}, {response.text}")
            price_stocks.append({"stock": stock, "price": None})
    USER_SETTINGS_LOG.info("Стоимость акций создана")
    return price_stocks


# print(get_price_stocks())
# print(get_currency_rates())



