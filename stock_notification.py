import requests
import time
from datetime import datetime, timedelta

STOCK_API_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&apikey=<API KEY>'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/<IFTTTKey>'


def get_price_of_stock(companyName):
    stock_url = STOCK_API_URL.format(companyName)
    response = requests.get(stock_url)
    response_json = response.json()
    current_data_keys = list(response_json['Time Series (5min)'].keys())
    current_data_key = current_data_keys[0]
    return float(response_json['Time Series (5min)'][current_data_key]['4. close']), current_data_key

def post_ifttt_webhook(event, company_name, stock_price, current_time):
    data = {'value1': company_name, 'value2': current_time, 'value3': stock_price}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)


def main():
    while True:
        current_price, current_time = get_price_of_stock('YESBANK.BSE')
        print(current_price,current_time)
        post_ifttt_webhook('<EventName>', 'YESBANK.BSE', current_price, current_time)
        time.sleep(300)

if __name__ == "__main__":
    main()