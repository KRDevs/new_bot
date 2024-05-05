import re


def card_validate_type(card_number: str) -> bool:
    humo_regex = re.compile(r'^9860\d{2}\s\d{4}\s\d{4}\s\d{4}$')
    uzcard_regex = re.compile(r'^5614\d{12}$|^8600\d{12}$|^6262\d{12}$')

    if humo_regex.match(card_number) or uzcard_regex.match(card_number):
        return True
    else:
        return False
