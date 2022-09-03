import gspread
# gspread wraps the Google Sheets API
# see docs at https://docs.gspread.org/en/latest/
from datetime import datetime
import requests
import time
import os
from xml.etree import ElementTree as ET
import psycopg2
from TestProject.TestProject.settings import DATABASES

SPREADSHEET_ID = "1NVA-zupJLAUEOISPcgUAmfEqcwcqKHBoYn7rds-XdH0"
USD_CODE = 'R01235'
connection = psycopg2.connect(host=DATABASES['default']['HOST'], user=DATABASES['default']['USER'],
                              password=DATABASES['default']['PASSWORD'], database=DATABASES['default']['NAME'])


def worker():
    # if you use gc = gspread.service_account() locate file at %appdata%/gspread/service_account.json
    # using service_account.json file at the root of the project
    gc = gspread.service_account(filename='service_account.json')

    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

    all_rows = (sheet.get_values())
    headers = all_rows[0]
    data = all_rows[1:]

    # parse xml and get dollar rate
    # dollar rate is used to convert dollar to ruble
    rates_url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={datetime.now().date().strftime('%d/%m/%Y')}"
    rates_request = requests.get(rates_url)
    rates_xml = rates_request.text
    root_xml = ET.fromstring(rates_xml)
    USD_RATE = root_xml.find(f'Valute[@ID="{USD_CODE}"]').find('Value').text.replace(',', '.')
    # print(USD_RATE)


    with connection.cursor() as cursor:
        # delete all rows from table
        cursor.execute("DELETE FROM app_product")

        for row in data:

            # insert new rows from the spreadsheet
            # convert usd to rubles
            cost_in_rub = round(float(row[1]) * float(USD_RATE), 2)
            # p = Product(_id=row[0], order_number=row[1], cost=row[2], delivery_time=row[3], cost_in_rub=float(row[4]))
            query = f"""INSERT INTO "public".app_product (id, order_number, cost, delivery_time, cost_in_rub) 
            VALUES ({row[0]}, {row[1]}, '{float(row[2])}', '{row[3]}', '{cost_in_rub}');"""
            # print(query)
            cursor.execute(query)

        connection.commit()
        print(f'{datetime.now()}: Обновлено успешно {len(data)} строк. Текущий курс доллара: {USD_RATE} рублей')

if __name__ == '__main__':
    while True:
        worker()
        print('Press Ctrl+C to quit.')
        time.sleep(10)
        os.system('cls')
