import gspread
from google.oauth2.service_account import Credentials

COLORS = {
    "black": "\u001b[30;1m",
    "red": "\u001b[31;1m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33;1m",
    "light-yellow": "\u001b[33m",
    "blue": "\u001b[34;1m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "yellow-background": "\u001b[43m",
    "black-background": "\u001b[0m",
    "cyan-background": "\u001b[46;1m",
    'green-background': '\u001b[42m',
    'bright-black-background': '\u001b[40;1m',
    'blackbb': '\u001b[40m',
    "bold": "\u001b[1m"
}


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    '''
    Get sales figures input from the user
    '''
    while True:
        print(f'{COLORS["black-background"]}Pleas enter sales data from the last market.')
        print(f'{COLORS["bright-black-background"]}Data should be six numbers, seperated by commas.')
        print(f'{COLORS["blackbb"]}Example: 10,20,30,40,50,60\n')

        data_str = input('Enter your data here:\n ')

        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print('Data is valid!')
            break
            
    return sales_data        

def validate_data(values):
    '''
    Get sales figures input from the user.
    Run a while loop to collect a valid string og data from the user
    via the terminal, which must be a string of 6 numbers separated 
    by commas. The loop will repeatedly request data, until it is valid.
    '''
    try: 
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True

def update_worksheet(data, worksheet):
    '''
    Recives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    '''
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfuly\n')


def calculate_surplus_data(sales_row):
    '''
    Compare slaes with stock and calculate the surplus for each item type.

    THe surplus is defined as the sales figures subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    '''
    print('Calcultaing surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stocks_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stocks_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries_sales():
    '''
    Collect collumns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    '''
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculate_stock_data(data):
    '''
    Calculate the average stock for each item type, adding 10%
    '''
    print('Calculating stock data...\n')
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data


def main():
    '''
    Run all program functions
    '''
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')


print('Welcome to Love Sandwiches Data Automation')
main()

