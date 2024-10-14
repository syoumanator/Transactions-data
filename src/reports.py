import logging
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd

from src.utils import PATH_TO_EXCEL, read_file_excel

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_REPORTS_LOG = BASE_DIR / "logs" / "reports.log"
PATH_TXT = BASE_DIR / "data" / "function_operation_report.txt"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s",
    filename=PATH_REPORTS_LOG,
    filemode="w",
    encoding="utf-8",
)
REPORTS_LOG = logging.getLogger(__name__)


def report_to_file(filename: Path = PATH_TXT) -> Callable:
    """Декоратор для функций-отчетов, который записывает в файл результат функции, формирующая отчет.
    Декоратор — принимает имя файла в качестве параметра."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                with open(filename, "w", encoding="utf-8") as file:
                    REPORTS_LOG.info(f"Запись результата работы функции {func} в файл {filename}")
                    file.write(result)
            except Exception as e:
                REPORTS_LOG.error(f"Произошла ошибка: {e}")
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(f"{func.__name__} error: {e} Inputs: {args}, {kwargs}\n")

                raise

            return result

        return wrapper

    return decorator


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[Any] = None) -> str | None:
    """Функция принимает на вход: датафрейм с транзакциями, название категории, опциональную дату.
        Если дата не передана, то берется текущая дата.
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    try:
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, "%d.%m.%Y")
        start_date = date - timedelta(days=date.day - 1) - timedelta(days=3 * 30)
        REPORTS_LOG.info(f"Фильтрация транзакций по категории {category} за последние 3 месяца")
        filtered_transaction = transactions[
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= date)
            & (transactions["Категория"] == category)
        ]
        grouped_transaction = filtered_transaction.groupby("Дата операции").sum()
        REPORTS_LOG.info("Транзакции отфильтрованы и сгруппированы")
        return grouped_transaction.to_json(orient="records", force_ascii=False, indent=4)
    except Exception as e:
        REPORTS_LOG.error(f"Произошла ошибка: {e}")
        print(f"Произошла ошибка: {e}")
        return ""
# print(spending_by_category(read_file_excel(PATH_TO_EXCEL), "Супермаркеты", "15.12.2021"))
