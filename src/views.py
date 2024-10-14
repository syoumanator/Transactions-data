import json
import logging
from pathlib import Path
from typing import Any

from src.utils import (
    PATH_TO_EXCEL,
    card_information,
    get_currency_rates,
    get_price_stocks,
    greeting,
    read_file_excel,
    top_transactions,
)

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_JSON = BASE_DIR / "data" / "data.json"
PATH_VIEWS_LOG = BASE_DIR / "logs" / "views.log"


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s",
    filename=PATH_VIEWS_LOG,
    filemode="w",
    encoding="utf-8",
)

VIEWS_LOG = logging.getLogger(__name__)


def response_json(date: str) -> Any:
    """Основная функция принимающая на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ"""
    transactions = read_file_excel(PATH_TO_EXCEL)
    greetings = greeting(date)
    cards = card_information(transactions)
    top_5 = top_transactions(transactions)
    currency_rates = get_currency_rates()
    price_stocks = get_price_stocks()
    user_data = {
        "greeting": greetings,
        "cards": cards,
        "top_transactions": top_5,
        "exchange_rates": currency_rates,
        "stocks": price_stocks,
    }
    VIEWS_LOG.info("Формирование JSON-ответа")
    return user_data


# print(response_json("2021-12-15 16:59:20"))


with open(PATH_TO_JSON, "w") as file:
    json.dump(response_json("2021-12-15 16:59:20"), file, ensure_ascii=False, indent=4)
