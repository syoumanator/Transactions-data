from pathlib import Path
from typing import Any

import pandas as pd
import logging
from datetime import datetime
# import datetime
import os

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_EXCEL = BASE_DIR / "data" / "operations.xlsx"
PATH_UTILS_LOG = BASE_DIR / "logs" / "utils.log"


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



# Приветствие
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


# print(greeting('2021-11-21 23:50:17'))
# print(read_file_excel(PATH_TO_EXCEL))
# input_time = input()
# # 02.11.2021 23:50:17
#
# current_transactions = []
# def get_json(current_date: str, file_info) -> list:
#     transactions = file_info.to_dict(orient="records")
#     for transaction in transactions:
#         if (
#                 str(transaction["Дата платежа"])[2:10] == current_date[2:10]
#                 and str(transaction["Дата платежа"])[:2] <= current_date[:2]
#         ):
#             current_transactions.append(transaction)
#     return current_transactions
#
#
# print(get_json(input_time, read_file_excel(PATH_TO_EXCEL)))



# Топ-5 транзакций по сумме платежа
# def top_transactions(transactions_df: pd.DataFrame) -> list[dict[str, Any | None]]:
#     """Функция принимает на вход датафрейм с транзакциями, сортирует и выводит топ-5 транзакций по сумме платежа"""
#     try:
#         UTILS_LOG.info("Сортировка транзакций по сумме платежа")
#         transactions_df = transactions_df.sort_values(by="Сумма платежа", ascending=False, key=lambda x: abs(x))
#         # Выбор топ-5 транзакций
#         top_5_transactions = transactions_df.head(5).to_dict('records')
#         # Преобразование результатов в список словарей
#         result = []
#         for transaction in top_5_transactions:
#             operation = {"date": transaction.get("Дата операции"), "amount": transaction.get("Сумма платежа"),
#                          "category": transaction.get("Категория"), "description": transaction.get("Описание")}
#             result.append(operation)
#         UTILS_LOG.info("Выполнение сортировки транзакций по сумме платежа завершено")
#
#         return result
#     except Exception as e:
#         UTILS_LOG.error(f"Произошла ошибка {e}")
#         return []
# print(top_transactions(read_file_excel(PATH_TO_EXCEL)))



# Стоимость акций из S&P500






