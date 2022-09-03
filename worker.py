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

token = os.environ.get('TELEGRAM_BOT_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')
SPREADSHEET_ID = "1NVA-zupJLAUEOISPcgUAmfEqcwcqKHBoYn7rds-XdH0"
USD_CODE = 'R01235'
connection = psycopg2.connect(host=DATABASES['default']['HOST'], user=DATABASES['default']['USER'],
                              password=DATABASES['default']['PASSWORD'], database=DATABASES['default']['NAME'])


# b. Разработка функционала проверки соблюдения «срока поставки» из таблицы.
# В случае, если срок прошел, скрипт отправляет уведомление в Telegram.
def check_delivery_time():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT p.order_number, o.message_sent 
            FROM app_product p 
            LEFT JOIN app_overdue o ON o.order_number = p.order_number
            WHERE p.delivery_time < now() AND o.message_sent = FALSE;""")
        rows = cursor.fetchall()
        if len(rows) > 0:
            print(f'{datetime.now()}: {len(rows)} товаров просрочены')
            order_numbers = [str(row[0]) for row in rows]
            text = f'Следующие заказы {", ".join(order_numbers)} просрочены'
            for row in rows:
                print(f'{datetime.now()}: {row[0]} просрочен')
                # send message to telegram about overdue of order
                # update overdue field to prevent sending message again
                cursor.execute(f"UPDATE app_overdue SET message_sent = true WHERE order_number = {row[0]}")
            connection.commit()
            print(token, chat_id, text)
            url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}'
            requests.get(url)

        else:
            print(f'{datetime.now()}: Нет просроченных товаров')


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
        # delete only rows that are not in the spreadsheet
        cursor.execute("SELECT order_number FROM app_product")
        order_numbers = [str(row[0]) for row in cursor.fetchall()]
        data_order_numbers = [str(row[1]) for row in data]
        # compare two lists and get order numbers that are not in the spreadsheet
        order_numbers_to_delete = list(set(order_numbers) - set(data_order_numbers))
        # print(order_numbers_to_delete)
        if len(order_numbers_to_delete) == 0:
            print(f'{datetime.now()}: Нет новых заказов')
        else:

            cursor.execute("DELETE FROM app_product")

            for row in data:
                # insert new rows from the spreadsheet
                # convert usd to rubles
                cost_in_rub = round(float(row[1]) * float(USD_RATE), 2)
                delivery_time = datetime.strptime(row[3], '%d.%m.%Y')

                query = f"""INSERT INTO "public".app_product (id, order_number, cost, delivery_time, cost_in_rub) 
                VALUES ({row[0]}, {row[1]}, '{float(row[2])}', '{delivery_time}', '{cost_in_rub}');"""
                # print(query)
                cursor.execute(query)

            connection.commit()
            print(f'{datetime.now()}: Обновлено успешно {len(data)} строк. Текущий курс доллара: {USD_RATE} рублей')
            check_delivery_time()


if __name__ == '__main__':
    while True:
        worker()
        print('Press Ctrl+C to quit.')
        time.sleep(10)
