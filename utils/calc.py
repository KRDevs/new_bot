from .crypto_currency import exchange


def get_crypto_price(symbol):
    cryptocurrencies, last_updated = exchange()

    for crypto in cryptocurrencies:
        if crypto['symbol'] == symbol:
            return crypto['quote']['UZS']['price']

    return None
