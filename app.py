import asyncio
import datetime
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from database import create_user, db_start, update_balance

from keyboards.common_keyboards import admin_menu
from keyboards.inline_keyboards import services_btn, wallet_btn, market_btn, setting_btn, back_btn
from states.state import ContactState

from utils.crypto_currency import exchange

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

ADMIN_IDS = [1976114820]


@dp.message(Command('start'))
async def start_msg(message: types.Message):
    await message.answer("Botga xush kelibsiz! O'zingizga kerakli bo'lgan xizmat turini tanlang 👇",
                         reply_markup=services_btn())
    await create_user(user_id=message.from_user.id, username=message.from_user.username,
                      firstname=message.from_user.first_name, lastname=message.from_user.last_name,
                      created_at=datetime.datetime.now(), is_bot=message.from_user.is_bot, uz_balance=0, btc_balance=0,
                      eth_balance=0,
                      usdt_balance=0, bnb_balance=0, sol_balance=0, usdc_balance=0, xrp_balance=0, doge_balance=0,
                      ton_balance=0,
                      ada_balance=0)
    await message.delete()


@dp.callback_query(lambda callback_query: callback_query.data == 'wallet')
async def wallet_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="💳 Sizning hisobingiz:\nBTC: 0 BTC\nBNB: 0 BNB\nETH: 0 ETH\nTRX: 0 TRX\nTON: 0 TON\nUSDT: 0 USDT\nnKOTE: 0 nKOTE\nSCALE: 0 SCALE\nTAKE: 0 TAKE\n~ 0 UZS",
                           reply_markup=wallet_btn())
    await callback.message.delete()


@dp.callback_query(lambda callback_query: callback_query.data == 'market')
async def market_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="🗳 P2P Market\n Siz bu bo'limda kriptovalyuta sotib olishingiz yoki sotishingiz mumkin. Agar siz biror muammoga duch kelsangiz iltimos biz bilan bog'laning!",
                           reply_markup=market_btn())
    await callback.message.delete()


@dp.callback_query(lambda callback_query: callback_query.data == 'settings')
async def market_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="⚙️ Sozlamalar",
                           reply_markup=setting_btn())
    await callback.message.delete()


@dp.callback_query(lambda callback_query: callback_query.data == 'currency')
async def market_msg(callback: types.CallbackQuery):
    cryptocurrencies, last_updated = exchange()
    if not cryptocurrencies:
        await bot.send_message(callback.message.chat.id, "Error fetching cryptocurrency data.")
        return

    message = "💵 Kriptovalyuta kursi\n\n\n"
    for crypto in cryptocurrencies:
        name = crypto['name']
        symbol = crypto['symbol']
        price = crypto['quote']['UZS']['price']
        message += f"{name} ({symbol}) ~= {price:.5f} UZS\n\n"
    if last_updated:
        message += f"\n\n⏳ Kurslar {last_updated} vaqti bo'yicha."
    else:
        message += "\nKurslar  yangilanmadi."
    await bot.send_message(callback.message.chat.id, message, reply_markup=setting_btn())
    await callback.message.delete()


@dp.callback_query(lambda callback_query: callback_query.data == 'back')
async def back_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="👨‍💻 Xizmatlar👇",
                           reply_markup=services_btn())
    await callback.message.delete()


@dp.callback_query(lambda callback_query: callback_query.data == 'contact')
async def back_msg(callback: types.CallbackQuery, state=FSMContext):
    await callback.message.delete()
    await callback.answer(chat_id=callback.message.chat.id,
                          text="Botni ishlatishda duch kelgan muammolaringizni yoki o'z talab-takliflaringizni yozing. Sizning har bir fikringiz biz uchun muhim!")
    await state.set_state(ContactState.requirementTxt)


@dp.message(ContactState.requirementTxt)
async def requirement_msg(message: types.Message, state=FSMContext):
    await state.update_data(requirement_txt=message.text)
    state_date = await state.get_data()
    await bot.send_message(chat_id=1976114820,
                           text=f"@{message.chat.username} ning yuborgan talab va taklifi:\n{state_date.get('requirement_txt')}")
    await message.answer("Talab va takliflaringiz uchun rahmat! Xatoliklar uchun uzr so'raymiz",
                         reply_markup=back_btn())
    await state.clear()
    await message.delete()


@dp.message(F.text == "⬅️ Orqaga")
async def start_msg(message: types.Message):
    await message.answer("Xizmatlar 👇",
                         reply_markup=services_btn())
    await message.delete()


@dp.message(Command('admin'), F.from_user.id.in_(ADMIN_IDS))
async def admin_panel(message: types.Message):
    await message.answer(
        "Admin panelga xush kelibsiz 🆒", reply_markup=admin_menu()
    )
    await message.delete()


@dp.message(F.text == "📂 Bazani olish", F.from_user.id.in_(ADMIN_IDS))
async def get_base(message: types.Message):
    await message.answer(text="Ma'lumotlar bazasi")
    base = types.FSInputFile('baza.db')
    await message.answer_document(document=base)


async def main():
    await bot.set_my_commands([
        types.BotCommand(command="/start", description="Botni ishga tushirish"),
    ])
    await db_start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
