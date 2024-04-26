import requests

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '15',
    'convert': 'UZS'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '8b213bc4-7ef6-4670-84ac-8131b00c70a4',
}

currency = requests.get(url, params=parameters, headers=headers).json()
coins = currency['data']
for x in coins:
    print(x)
    # print(x['symbol'])
