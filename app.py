import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from keyboards.inline_keyboards import services_btn, wallet_btn, market_btn, setting_btn
from states.state import ContactState

logging.basicConfig(level=logging.INFO)
bot = Bot(token="7061261172:AAFUNRyf4rbgiQFM7SEHOrZDWB7eZ3omfBs")
dp = Dispatcher()


@dp.message(Command('start'))
async def start_msg(message: types.Message):
    await message.answer("Botga xush kelibsiz! O'zingizga kerakli bo'lgan xizmat turini tanlang 👇",
                         reply_markup=services_btn())


@dp.callback_query(lambda callback_query: callback_query.data == 'wallet')
async def wallet_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="💳 Sizning hisobingiz:\nBTC: 0 BTC\nBNB: 0 BNB\nETH: 0 ETH\nTRX: 0 TRX\nTON: 0 TON\nUSDT: 0 USDT\nnKOTE: 0 nKOTE\nSCALE: 0 SCALE\nTAKE: 0 TAKE\n~ 0 UZS",
                           reply_markup=wallet_btn())


@dp.callback_query(lambda callback_query: callback_query.data == 'market')
async def market_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="🗳 P2P Market\n Siz bu bo'limda kriptovalyuta sotib olishingiz yoki sotishingiz mumkin. Agar siz biror muammoga duch kelsangiz iltimos biz bilan bog'laning!",
                           reply_markup=market_btn())


@dp.callback_query(lambda callback_query: callback_query.data == 'settings')
async def market_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="⚙️ Sozlamalar",
                           reply_markup=setting_btn())


@dp.callback_query(lambda callback_query: callback_query.data == 'currency')
async def market_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="💵 Kriptovalyuta kursi\n1 BNB ~= 5444727.75 UZS\n1 ETH ~=37802500.0 UZS\n1 TON ~=67534.95 UZS\n1 TRX ~=1331.6 UZS\n1 USDT ~=11802.82 UZS",
                           reply_markup=setting_btn())


@dp.callback_query(lambda callback_query: callback_query.data == 'back')
async def back_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="👨‍💻 Xizmatlar👇",
                           reply_markup=services_btn())


@dp.callback_query(lambda callback_query: callback_query.data == 'contact')
async def back_msg(callback: types.CallbackQuery, state=FSMContext):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="Botni ishlatishda duch kelgan muammolaringizni yoki o'z talab-takliflaringizni yozing. Siznig har bir fikringiz biz uchun muhim!")
    await state.set_state(ContactState.requirementTxt)


@dp.message(ContactState.requirementTxt)
async def requirement_msg(message: types.Message, state=FSMContext):
    await state.update_data(requirement_txt=message.text)
    state_date = await state.get_data()
    await bot.send_message(chat_id=1976114820,
                           text=f"@{message.chat.username}ning yuborgan talab va taklifi:\n{state_date.get('requirement_txt')}")
    await message.answer("Talab va takliflaringiz uchun rahmat! Xatoliklar uchun uzr so'raymiz")
    await state.clear()


async def main():
    await bot.set_my_commands([
        types.BotCommand(command="/start", description="Botni ishga tushirish"),
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
