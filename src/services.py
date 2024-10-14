import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

# from src.utils import read_file_excel, PATH_TO_EXCEL


BASE_DIR = Path(__file__).resolve().parent.parent
PATH_SERVICES_LOG = BASE_DIR / "logs" / "services.log"


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s",
    filename=PATH_SERVICES_LOG,
    filemode="w",
    encoding="utf-8",
)
SERVICES_LOG = logging.getLogger(__name__)


def transaction_analysis(data: pd.DataFrame, year: int, month: int) -> str | None:
    """Функция принимает: data - данные с транзакциями;
                       year — год, за который проводится анализ;
                       month — месяц, за который проводится анализ.
    Возвращает: JSON с анализом, сколько на каждой категории можно
                заработать кешбэка в указанном месяце года."""
    try:
        transactions = data.to_dict(orient="records")
        cashback_analysis: dict = {}
        for transaction in transactions:
            transaction_date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
            if transaction_date.year == year and transaction_date.month == month:
                category = transaction["Категория"]
                amount = transaction["Сумма платежа"]
                if amount < 0:
                    cashback = transaction["Кэшбэк"]
                    if cashback is not None and cashback >= 0:
                        cashback = float(cashback)
                    else:
                        cashback = round(amount * -0.01, 2)
                    if category in cashback_analysis:
                        cashback_analysis[category] += cashback
                    else:
                        cashback_analysis[category] = cashback
                else:
                    continue
        SERVICES_LOG.info("Посчитана сумма кэшбэка по категориям")
        return json.dumps(cashback_analysis, ensure_ascii=False, indent=4)
    except Exception as e:
        SERVICES_LOG.error(f"Произошла ошибка {e}")
        print(f"Произошла ошибка {e}")
        return None
# print(transaction_analysis(read_file_excel(PATH_TO_EXCEL), 2021, 2))
