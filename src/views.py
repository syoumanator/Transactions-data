import json

# from src.utils import read_file_excel, PATH_TO_EXCEL
# from user_settings_json import get_current_stock, get_currencies, currency_stock, currency_list
#
# current_transactions = []
# cards = []
# top_list = []
# transaction_for_print = [{}]
#
#
# def get_json(current_date: str) -> list:
#     for transaction in read_file_excel(PATH_TO_EXCEL):
#         if (
#                 str(transaction["Дата платежа"])[2:10] == current_date[2:10]
#                 and str(transaction["Дата платежа"])[:2] <= current_date[:2]
#         ):
#             current_transactions.append(transaction)
#     return current_transactions


# def get_card() -> list:
#     for information in current_transactions:
#         card = {"last_digits": information["Номер карты"],
#                 "total_spent": information["Сумма операции"],
#                 "cashback": round(information["Сумма операции"] / 100, 2)}
#         cards.append(card)
#     return cards
#
#
# def filtered_top():
#     sort_transactions = sorted(current_transactions, reverse=True, key=lambda x: abs(x["Сумма платежа"]))
#     for transactions in sort_transactions:
#         top_transactions = {"date": transactions["Дата платежа"],
#                             "amount": transactions["Сумма платежа"],
#                             "category": transactions["Категория"],
#                             "description": transactions["Описание"]
#                             }
#         top_list.append(top_transactions)
#         if len(top_list) == 5:
#             break
#     return top_list
#





# import json
# import logging
# import os
# from pathlib import Path
# from typing import Any
#
# from dotenv import load_dotenv
#
# from src.utils import PATH_TO_EXCEL, read_file_excel, greeting
# from src.user_settings_json import get_currency_rates, get_price_stocks
#
#
# BASE_DIR = Path(__file__).resolve().parent.parent
# PATH_VIEWS_LOG = BASE_DIR / "logs" / "views.log"
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s",
#     filename=PATH_VIEWS_LOG,
#     filemode="w",
#     encoding="utf-8",
# )
#
# VIEWS_LOG = logging.getLogger(__name__)
#
#
# def response_json(date: str) -> Any:
#     """Основная функция принимающая на вход строку с датой и временем в формате
#         YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ"""
#     # transactions = read_file_excel(PATH_TO_EXCEL)
#     greetings = greeting(date)
#     currency_rates = get_currency_rates()
#     price_stocks = get_price_stocks()
#     user_data = {
#         "greeting": greetings,
#         "exchange_rates": currency_rates,
#         "stocks": price_stocks,
#     }
#     VIEWS_LOG.info("Формирование JSON-ответа")
#     return json.dumps(user_data, ensure_ascii=False, indent=4)