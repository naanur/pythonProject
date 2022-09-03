import gspread
# gspread wraps the Google Sheets API
# see docs at https://docs.gspread.org/en/latest/
import psycopg2

SPREADSHEET_ID = '1NVA-zupJLAUEOISPcgUAmfEqcwcqKHBoYn7rds-XdH0'


def main():
    # if you use gc = gspread.service_account() locate file at %appdata%/gspread/service_account.json
    # using service_account.json file at the root of the project
    gc = gspread.service_account(filename='service_account.json')

    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

    all_rows = (sheet.get_values())
    headers = all_rows[0]
    data = all_rows[1:]
    print(headers)

if __name__ == '__main__':
    main()
