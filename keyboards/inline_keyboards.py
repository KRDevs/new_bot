from aiogram import types


def services_btn():
    kb = [
        [(types.InlineKeyboardButton(text="💳 Hamyon", callback_data="wallet"))],
        [(types.InlineKeyboardButton(text="🗳 P2P Market", callback_data="market"))],
        [(types.InlineKeyboardButton(text="💵 Kriptovalyuta kursi", callback_data="currency"))],
        [(types.InlineKeyboardButton(text="📞 Biz bilan bog'lanish", callback_data="contact"))],
        [(types.InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings"))]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, one_time_keyboard=True)
    return keyboard


def wallet_btn():
    kb = [
        [(types.InlineKeyboardButton(text="📥 Kiritish", callback_data="deposit")),
         (types.InlineKeyboardButton(text="📤 Chiqarish", callback_data="withdraw"))],
        [(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back"))]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, one_time_keyboard=True)
    return keyboard


def market_btn():
    kb = [
        [(types.InlineKeyboardButton(text="Sotish", callback_data="sell")),
         (types.InlineKeyboardButton(text="Sotib olish", callback_data="buy"))],
        [(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back"))]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, one_time_keyboard=True)
    return keyboard


def setting_btn():
    kb = [
        [(types.InlineKeyboardButton(text="🆘 Yordam", callback_data="support"))],
        [(types.InlineKeyboardButton(text="📄 Monitoring", callback_data="monitoring"))],
        [(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back"))]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, one_time_keyboard=True)
    return keyboard


def back_btn():
    kb = [
        [(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back"))]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb, one_time_keyboard=True)
    return keyboard
