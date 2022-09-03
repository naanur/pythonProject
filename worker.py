import gspread
# gspread wraps the Google Sheets API
# see docs at https://docs.gspread.org/en/latest/
import datetime
import time
from .models import Product

SPREADSHEET_ID = "1NVA-zupJLAUEOISPcgUAmfEqcwcqKHBoYn7rds-XdH0"


def worker():
    # if you use gc = gspread.service_account() locate file at %appdata%/gspread/service_account.json
    # using service_account.json file at the root of the project
    gc = gspread.service_account(filename='service_account.json')

    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

    all_rows = (sheet.get_values())
    headers = all_rows[0]
    data = all_rows[1:]

    # delete all rows in the database
    Product.objects.all().delete()

    # parse xml and get dollar rate
    # dollar rate is used to convert dollar to ruble
    rates_url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={datetime.today().strftime('%d/%m/%Y')}"
    print(rates_url)

    # insert new rows from the spreadsheet
    for row in data:
        p = Product(id=row[0], order_number=row[1], cost=row[2], delivery_time=row[3], cost_in_rub=row[4])


if __name__ == '__main__':
    while True:
        worker()
        print('Press Ctrl+C to quit.')
        time.sleep(10)
