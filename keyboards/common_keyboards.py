from aiogram import types


def admin_menu():
    kb = [
        [(types.KeyboardButton(text="📂 Bazani olish"))]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def crypto_currency():
    kb = [
        [types.KeyboardButton(text="btc")],
        [types.KeyboardButton(text="eth")],
        [types.KeyboardButton(text="usdt")],
        [types.KeyboardButton(text="bnb")],
        [types.KeyboardButton(text="sol")],
        [types.KeyboardButton(text="usdc")],
        [types.KeyboardButton(text="xrp")],
        [types.KeyboardButton(text="doge")],
        [types.KeyboardButton(text="ton")],
        [types.KeyboardButton(text="ada")],
        [types.KeyboardButton(text="⬅️ Orqaga")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
    return keyboard
