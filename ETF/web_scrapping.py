# import django
# django.setup()


# import yfinance as yf
# import mysql.connector
# from datetime import date, timedelta
# from django.db import connection
# from django.apps import apps
# from Custom_admin.models import BaseTickerData, create_ticker_data_model, ETFDataModel, TickerData

# from django.db.models import Max

# def insert_data_into_model(model, data):
#     existing_dates = set(model.objects.values_list('date', flat=True))
    
#     new_data = [
#         model(
#             date=index,
#             Open=row['Open'],
#             high=row['High'],
#             low=row['Low'],
#             close=row['Close'],
#             volume=row['Volume'],
#             dividends=row['Dividends'],
#             stock_splits=row['Stock Splits'],
#         ) for index, row in data.iterrows() if index not in existing_dates
#     ]

#     if new_data:
#         model.objects.bulk_create(new_data)

# def get_start_date(model, today, num_days=4):
#     latest_date = model.objects.aggregate(Max('date'))['date__max']

#     if latest_date:
#         return (latest_date + timedelta(days=1)).strftime("%Y-%m-%d")

#     return (today - timedelta(days=num_days)).strftime("%Y-%m-%d")

# etf_symbols_and_names = {
#     'MOM50.NS': 'Motilal Oswal M50 ETF',
#     'GOLDBEES.NS': 'Nippon India ETF Gold BeES',
#     'SILVERBEES.NS': 'Nippon India Silver ETF',
#     'ITBEES.NS': 'Nippon India ETF Nifty IT',
#     'SETFNIF50.NS': 'SBI Nifty IT ETF',
#     'NIFTYBEES.NS': 'Nippon India ETF Nifty 50 BeES'
# }

# if __name__ == "__main__":
#     # Loop through each ETF in the dictionary
#     for ticker_symbol, ticker_name in etf_symbols_and_names.items():
#         try:
#             # Get data on the current ticker
#             ticker_data = yf.Ticker(ticker_symbol)
#             print(f"\nFetching data for {ticker_name} ({ticker_symbol})...")

#             # Get the dynamically created model
#             ticker_model = create_ticker_data_model(ticker_symbol)

#             # Get start date dynamically
#             today = date.today()
#             start_date = get_start_date(ticker_model, today)

#             # Get data
#             historical_data = ticker_data.history(period="1y", start='2023-01-24', end='2024-01-23')

#             if not historical_data.empty:
#                 # Insert data into the corresponding model
#                 insert_data_into_model(ticker_model, historical_data)
#                 print(f"Data for {ticker_name} ({ticker_symbol}) saved successfully.")
#             else:
#                 print(f"No new data available for {today} for {ticker_name} ({ticker_symbol}). Existing data remains unchanged.")

#         except Exception as fetch_error:
#             print(f"Error fetching data for {ticker_name} ({ticker_symbol}): {fetch_error}")

#     print("Process completed.")



import django
django.setup()

import yfinance as yf
from datetime import date, timedelta
from django.apps import apps
from Custom_admin.models import Custom_admin_niftybees_ns

from django.db.models import Max

def insert_data_into_model(model, data):
    existing_dates = set(model.objects.values_list('date', flat=True))
    
    new_data = [
        model(
            date=index,
            Open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            volume=row['Volume'],
            dividends=row['Dividends'],
            stock_splits=row['Stock Splits'],
        ) for index, row in data.iterrows() if index not in existing_dates
    ]

    if new_data:
        model.objects.bulk_create(new_data)

def get_start_date(model, today, num_days=4):
    latest_date = model.objects.aggregate(Max('date'))['date__max']

    if latest_date:
        return (latest_date + timedelta(days=1)).strftime("%Y-%m-%d")

    return (today - timedelta(days=num_days)).strftime("%Y-%m-%d")

if __name__ == "__main__":
    try:
        # Get data for NIFTYBEES.NS
        ticker_data = yf.Ticker('NIFTYBEES.NS')
        print("\nFetching data for NIFTYBEES.NS...")

        # Get the model
        ticker_model = Custom_admin_niftybees_ns

        # Get start date dynamically
        today = date.today()
        start_date = get_start_date(ticker_model, today)

        # Get data
        historical_data = ticker_data.history(period="1y", start='2023-01-24', end='2024-01-23')

        if not historical_data.empty:
            # Insert data into the corresponding model
            insert_data_into_model(ticker_model, historical_data)
            print("Data for NIFTYBEES.NS saved successfully.")
        else:
            print(f"No new data available for {today} for NIFTYBEES.NS. Existing data remains unchanged.")

    except Exception as fetch_error:
        print(f"Error fetching data for NIFTYBEES.NS: {fetch_error}")

    print("Process completed.")
