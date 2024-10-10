from datetime import datetime

from src.services import transaction_analysis
from src.utils import read_file_excel
from src.views import PATH_TO_EXCEL, response_json

if __name__ == "__main__":
    transactions = read_file_excel(PATH_TO_EXCEL)
    date_now = datetime.now()
    current_time = datetime.strftime(date_now, "%Y-%m-%d %H:%M:%S")
    home_page = response_json(current_time)
    print(home_page)
    cashback_category = transaction_analysis(transactions, 2021, 3)
    print(cashback_category)
