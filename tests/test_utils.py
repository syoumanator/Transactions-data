from pathlib import Path
from unittest.mock import MagicMock, patch
import pandas as pd
import pytest
from datetime import datetime

from src.utils import read_file_excel, greeting, top_transactions, card_information


# def test_correct_time():
#     input_time = "2023-08-10 14:30:00"
#     expected_output = "10.08.2023 14:30:00"
#     assert correct_time(input_time) == expected_output
#
#
# def test_invalid_input_format():
#     input_time = "not"
#     with pytest.raises(ValueError):
#         correct_time(input_time)


def test_read_excel_success(read_file: Path) -> None:
    with patch(
        "pandas.read_excel",
        return_value=pd.DataFrame({"Дата": ["01.01.2024"], "Тип транзакции": ["Расход"], "Сумма": [-100]}),
    ):
        result = read_file_excel(read_file)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result["Дата"].iloc[0] == "01.01.2024"
        assert result["Тип транзакции"].iloc[0] == "Расход"
        assert result["Сумма"].iloc[0] == -100


def test_read_excel_empty(read_file: Path) -> None:
    with patch("pandas.read_excel", side_effect=pd.errors.EmptyDataError("File is empty")):
        result = read_file_excel(read_file)
        assert result is None


def test_read_excel_not_found(read_file: Path) -> None:
    with patch("pandas.read_excel", side_effect=FileNotFoundError("File not found")):
        result = read_file_excel(read_file)
        assert result is None



def test_read_excel_wrong_path(wrong_file: Path) -> None:
    with patch("pandas.read_excel", side_effect=FileNotFoundError("File not found")):
        result = read_file_excel(wrong_file)
        assert result is None


@pytest.mark.parametrize(
    "time, result",
    [
        ("2021-12-15 16:59:20", "Добрый день"),
        ("2021-12-15 10:59:20", "Доброе утро"),
        ("2021-12-15 02:59:20", "Доброй ночи"),
        ("2021-12-15 20:59:20", "Добрый вечер"),
    ],
)
def test_greeting(time: str, result: str) -> None:
    assert greeting(time) == result


def test_top_transactions_empty(test_empty_df: pd.DataFrame) -> None:
    assert top_transactions(test_empty_df) == []


def test_top_transactions(test_top_5: pd.DataFrame) -> None:
    result = [
        {"amount": -400.0, "category": "Магазины", "date": "25.06.2023 12:00:00", "description": "Покупка техники"},
        {"amount": -300.0, "category": "Магазины", "date": "23.06.2023 12:00:00", "description": "Покупка одежды"},
        {"amount": -200.0, "category": "Транспорт", "date": "21.06.2023 12:00:00", "description": "Оплата проезда"},
        {"amount": -100.0, "category": "Еда", "date": "20.06.2023 12:00:00", "description": "Покупка еды"},
        {"amount": -50.0, "category": "Развлечения", "date": "22.06.2023 12:00:00", "description": "Кино"},
    ]
    assert top_transactions(test_top_5) == result


def test_card_information_data_empty(test_empty_df: pd.DataFrame) -> None:
    assert card_information(test_empty_df) == []


def test_get_cards_data_single_transaction(test_df: pd.DataFrame) -> None:
    expected_result = [
        {"last_digits": "1234", "total_spent": 300.0, "cashback": 3.0},
        {"last_digits": "5678", "total_spent": 50.0, "cashback": 0.5},
    ]
    assert card_information(test_df) == expected_result


def test_get_cards_data_nan_card_number(test_df_nan: pd.DataFrame) -> None:
    expected_result = [
        {"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0},
        {"last_digits": "5678", "total_spent": 50.0, "cashback": 0.5},
    ]
    assert card_information(test_df_nan) == expected_result


def test_get_cards_data_cashback(test_df_not_cashback: pd.DataFrame) -> None:
    expected_result = [
        {"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0},
        {"last_digits": "5678", "total_spent": 50.0, "cashback": 0.5},
    ]
    assert card_information(test_df_not_cashback) == expected_result


def test_get_cards_data_nan_card_number_2(test_df_nan_zero: pd.DataFrame) -> None:
    expected_result = [{'cashback': 1.0, 'last_digits': '1234', 'total_spent': 100.0},
 {'cashback': 0.5, 'last_digits': '5678', 'total_spent': 50.0}]
    assert card_information(test_df_nan_zero) == expected_result



