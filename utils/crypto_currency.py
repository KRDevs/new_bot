import requests
from datetime import datetime
import pytz


def exchange():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'UZS'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '8b213bc4-7ef6-4670-84ac-8131b00c70a4',
    }

    response = requests.get(url, params=parameters, headers=headers)
    if response.status_code == 200:
        data = response.json()
        cryptocurrencies = data['data']
        last_updated_str = data['status']['timestamp']
        last_updated_utc = datetime.strptime(last_updated_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        tz = pytz.timezone('Asia/Tashkent')
        last_updated = last_updated_utc.replace(tzinfo=pytz.utc).astimezone(tz)
        return cryptocurrencies, last_updated
    else:
        print("Error fetching data from CoinMarketCap API")
        return [], None
