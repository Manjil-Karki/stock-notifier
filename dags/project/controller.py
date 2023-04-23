import requests
import os
import csv
import pandas as pd
import yfinance as yf

storage_dir = r'dags/project/storage/'
filename = r'user_data.csv'

def ticker_available(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}'
    response = requests.get(url)
    if response.status_code == 200:
        # check if the response contains data for the ticker
        if 'No results for' in response.text:
            return False
        else:
            return True
    else:
        return False
    

def init_storage():
    if not os.path.exists(storage_dir):
        os.mkdir(storage_dir)

def init_file(data):
    if not os.path.exists(storage_dir+filename):
        with open(storage_dir+filename, "w", newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(data.keys())

def write_users_data(data):
    
    init_storage()
    init_file(data)

    with open(storage_dir+filename, 'a', newline='') as file:
        fieldnames = data.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)

def read_data(group_by):
    df = pd.read_csv(storage_dir+filename)
    df = df[df['options'] == group_by]
    print(df[0])
    df.to_csv(storage_dir+group_by+'.csv', index = False)
    print("Written")


def check_threshold(group):
    file_path = storage_dir+group+'.csv'
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        
        ticker = yf.Ticker(row['ticker'])
        current_price = ticker.info['currentPrice']
        if current_price > row['lower'] and current_price < row['upper']:
            df = df.drop(index=index)
        else:
            df.loc[index, 'currentPrice'] = current_price

    df.to_csv(file_path, index=False)
    return

def compose_message(row):
    message = f"Dear {row['name']} the stock {row['ticker']} "
    if row['currentPrice'] > row['upper']:
        message += 'has exceeded the threshold. '
    else:
        message += 'is below the threshold limit. '
    message += f"Current price being ${row['currentPrice']}"
    return message

def send_sms(message, phone):
    print("SMS sent to", phone)
    print(message)

def send_mail(message, email):
    print("Email sent to ", email)
    print(message)

def send_message(group):
    file_path = storage_dir+group+'.csv'
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        message = compose_message(row)
        if row['notification'] == 'SMS':
            send_sms(message, row['phone'])
        else:
            send_mail(message, row['email'])