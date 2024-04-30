from aiogram import types


def admin_menu():
    kb = [
        [(types.KeyboardButton(text="📂 Bazani olish"))]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
