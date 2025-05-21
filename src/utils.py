import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.user_settings_json import settings

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_EXCEL = BASE_DIR / "data" / "operations.xlsx"
PATH_UTILS_LOG = BASE_DIR / "logs" / "utils.log"
PATH_ENV = BASE_DIR / ".env"

load_dotenv(dotenv_path=PATH_ENV)
API_KEY_CURRENCIES = os.getenv("API_KEY_CURRENCIES")
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
headers = {"apikey": API_KEY_CURRENCIES}


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s",
    filename=PATH_UTILS_LOG,
    filemode="w",
    encoding="utf-8",
)


UTILS_LOG = logging.getLogger(__name__)


def read_file_excel(path: Path) -> pd.DataFrame:
    """Функция принимает на вход путь до excel-файла
    и возвращает датафрейм с банковскими операциями."""
    try:
        transactions_df = pd.read_excel(path)
        UTILS_LOG.info(f"Чтение данных из файла: {PATH_TO_EXCEL}")
        return transactions_df
    except pd.errors.EmptyDataError as e:
        UTILS_LOG.error(f"Произошла ошибка: {e}")
        print(f"Произошла ошибка: {e}")
    except FileNotFoundError:
        UTILS_LOG.warning("Файл не найден")
        print("Файл не найден")


def greeting(date: str) -> str:
    """Приветствие в формате "???", где ??? — «Доброе утро» /
    «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени."""
    now = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    current_hour = now.hour
    if 0 <= current_hour < 6:
        UTILS_LOG.info("Приветствие: 'Доброй ночи'")
        return "Доброй ночи"
    elif 6 <= current_hour < 12:
        UTILS_LOG.info("Приветствие: 'Доброе утро'")
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        UTILS_LOG.info("Приветствие: 'Добрый день'")
        return "Добрый день"
    elif 18 <= current_hour < 24:
        UTILS_LOG.info("Приветствие: 'Добрый вечер'")
        return "Добрый вечер"


def top_transactions(transactions_df: pd.DataFrame) -> list[dict[str, Any | None]]:
    """Функция принимает на вход датафрейм с транзакциями, сортирует и выводит топ-5 транзакций по сумме платежа"""
    try:
        UTILS_LOG.info("Сортировка транзакций по сумме платежа")
        transactions_df = transactions_df.sort_values(by="Сумма платежа", ascending=False, key=lambda x: abs(x))
        top_5_transactions = transactions_df.head(5).to_dict("records")
        result = []
        for transaction in top_5_transactions:
            operation = {
                "date": transaction.get("Дата операции"),
                "amount": transaction.get("Сумма платежа"),
                "category": transaction.get("Категория"),
                "description": transaction.get("Описание"),
            }
            result.append(operation)
        UTILS_LOG.info("Выполнение сортировки транзакций по сумме платежа завершено")

        return result
    except Exception as e:
        UTILS_LOG.error(f"Произошла ошибка {e}")
        return []


# print(top_transactions(read_file_excel(PATH_TO_EXCEL)))


def card_information(transactions_df: pd.DataFrame) -> list[dict]:
    """Функция принимает на вход DataFrame c финансовыми операциями и
    выводит информацию по каждой карте:
    последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей)."""
    UTILS_LOG.info("Преобразование DataFrame в список словарей")
    transactions = transactions_df.to_dict(orient="records")
    card_info = {}
    UTILS_LOG.info("Сортировка по номерам карт,подсчет суммы платежей и кэшбэка")
    for transaction in transactions:
        card_number = transaction.get("Номер карты")
        if not card_number or str(card_number).strip().lower() == "nan":
            continue
        amount = float(transaction["Сумма операции"])
        if card_number not in card_info:
            card_info[card_number] = {"total_spent": 0.0, "cashback": 0.0}
        if amount < 0:
            card_info[card_number]["total_spent"] += abs(amount)
            cashback_value = transaction.get("Кэшбэк")
            if transaction["Категория"] != "Переводы" and transaction["Категория"] != "Наличные":
                if cashback_value is not None:
                    cashback_amount = float(cashback_value)
                    if cashback_amount >= 0:
                        card_info[card_number]["cashback"] += cashback_amount
                    else:
                        card_info[card_number]["cashback"] += amount * -0.01
                else:
                    card_info[card_number]["cashback"] += amount * -0.01
    cards_data = []
    for last_digits, data in card_info.items():
        cards_data.append(
            {
                "last_digits": last_digits,
                "total_spent": round(data["total_spent"], 2),
                "cashback": round(data["cashback"], 2),
            }
        )
    UTILS_LOG.info("получен словарь по тратам и кэшбэку по каждой карте")
    return cards_data


# print(card_information(read_file_excel(PATH_TO_EXCEL)))


def get_currency_rates() -> list[dict]:
    """Функция принимает список с кодами валют,
    а возвращает список словарей с текущими курсами"""
    currency_list = []
    for currency in settings["user_currencies"]:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"
        UTILS_LOG.info(f"Запрос курса валюты {currency}")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            UTILS_LOG.info("Успешный запрос")
            result = response.json()
            ruble_cost = result["result"]
            currency_list.append({"currency": currency, "rate": ruble_cost})
        else:
            UTILS_LOG.warning(f"Ошибка: {response.status_code}, {response.text}")
            print(f"Ошибка: {response.status_code}, {response.text}")
            currency_list.append({"currency": currency, "rate": None})
    UTILS_LOG.info("Курсы валют созданы")
    return currency_list


# print(get_currency_rates())


def get_price_stocks() -> list[dict]:
    """Функция принимает список с кодами компаний
    и возвращает список словарей со стоимостью акций каждой компании"""
    price_stocks = []
    for stock in settings["user_stocks"]:
        url = f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey={API_KEY_STOCK}"
        UTILS_LOG.info(f"Запрос стоимости акций компании {stock}")
        response = requests.get(url)
        if response.status_code == 200:
            UTILS_LOG.info("Успешный запрос")
            result = response.json()
            price = result[0]["price"]
            price_stocks.append({"stock": stock, "price": price})
        else:
            UTILS_LOG.warning(f"Ошибка: {response.status_code}, {response.text}")
            print(f"Ошибка: {response.status_code}, {response.text}")
            price_stocks.append({"stock": stock, "price": None})
    UTILS_LOG.info("Стоимость акций создана")
    return price_stocks


# print(get_price_stocks())
