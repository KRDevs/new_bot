import asyncio
import datetime
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from database import create_user, db_start, update_balance, get_balance, insert_history, db_history, \
    export_history_to_excel

from keyboards.common_keyboards import admin_menu, crypto_currency
from keyboards.inline_keyboards import services_btn, wallet_btn, market_btn, setting_btn, back_btn

from states.state import ContactState, DepositState, WithdrawState, SellState, BuyState

from utils.crypto_currency import exchange
from utils.calc import get_crypto_price

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
                      created_at=datetime.datetime.now(), is_bot=message.from_user.is_bot, uz_balance=0.0,
                      btc_balance=0.0,
                      eth_balance=0.0,
                      usdt_balance=0.0, bnb_balance=0.0, sol_balance=0.0, usdc_balance=0.0, xrp_balance=0.0,
                      doge_balance=0.0,
                      ton_balance=0.0,
                      ada_balance=0.0)
    await message.delete()


@dp.callback_query(lambda callback_query: callback_query.data == 'wallet')
async def wallet_msg(callback: types.CallbackQuery):
    uz_balance = await get_balance(user_id=callback.from_user.id, valute="uz")
    btc_balance = await get_balance(user_id=callback.from_user.id, valute="btc")
    eth_balance = await get_balance(user_id=callback.from_user.id, valute="eth")
    usdt_balance = await get_balance(user_id=callback.from_user.id, valute="usdt")
    bnb_balance = await get_balance(user_id=callback.from_user.id, valute="bnb")
    sol_balance = await get_balance(user_id=callback.from_user.id, valute="sol")
    usdc_balance = await get_balance(user_id=callback.from_user.id, valute="usdc")
    xrp_balance = await get_balance(user_id=callback.from_user.id, valute="xrp")
    doge_balance = await get_balance(user_id=callback.from_user.id, valute="doge")
    ton_balance = await get_balance(user_id=callback.from_user.id, valute="ton")
    ada_balance = await get_balance(user_id=callback.from_user.id, valute="ada")
    await bot.send_message(chat_id=callback.message.chat.id,
                           text=f"Sizning hisobingiz \n\nUZS: {uz_balance}\n\nBTC: {btc_balance}\n\nETH: {eth_balance}\n\nUSDT: {usdt_balance}\n\nBNB: {bnb_balance}\n\nSOL: {sol_balance}\n\nUSDC: {usdc_balance}\n\nXRP: {xrp_balance}\n\nDOGE: {doge_balance}\n\nTON: {ton_balance}\n\nADA: {ada_balance}",
                           reply_markup=wallet_btn())
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@dp.callback_query(lambda callback_query: callback_query.data == 'deposit')
async def deposit_msg(callback: types.CallbackQuery, state=FSMContext):
    await bot.send_message(chat_id=callback.message.chat.id, text="Iltimos karta raqamingizni kiriting!")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(DepositState.card)


@dp.message(DepositState.card)
async def deposit_card(message: types.Message, state=FSMContext):
    await state.update_data(card_number=message.text)
    if message.text.isdigit():
        await message.answer("Iltimos summani kiriting")
        await state.set_state(DepositState.depositSum)
    else:
        await message.answer("Karta raqami noto'g'ri, iltimos qaytadan kiriting!")
        await state.set_state(DepositState.card)


@dp.message(DepositState.depositSum)
async def deposit_sum(message: types.Message, state=FSMContext):
    if message.text.replace(".", "").isdigit() and float(message.text) > 0:
        await state.update_data(deposit_sum=message.text)
        state_date = await state.get_data()
        card = state_date.get('card_number')
        deposit = state_date.get('deposit_sum')
        await update_balance(user_id=message.from_user.id, valute="uz", new_balance=float(deposit))
        await message.answer(
            f"{message.chat.first_name} {message.chat.last_name} hisobingizga {deposit} UZS {card} kartasidan muvaffaqiyatli o'tkazildi 🥳",
            reply_markup=back_btn())
        await insert_history(user_id=message.from_user.id, username=message.from_user.username,
                             firstname=message.from_user.first_name, lastname=message.from_user.last_name,
                             created_at=datetime.datetime.now(), action_type="Hisobni to'ldirish",
                             uz_sum=float(deposit),
                             crypto_sum=0.0,
                             crypto_name="None",
                             card=card)
        await state.clear()
    else:
        await message.answer("Iltimos summani to'g'ri kiriting ⚠️")
        await state.set_state(DepositState.depositSum)


@dp.callback_query(lambda callback_query: callback_query.data == 'withdraw')
async def withdraw_msg(callback: types.CallbackQuery, state=FSMContext):
    await bot.send_message(chat_id=callback.message.chat.id, text="Iltimos karta raqamingizni kiriting!")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(WithdrawState.card)


@dp.message(WithdrawState.card)
async def withdraw_card(message: types.Message, state=FSMContext):
    if message.text.isdigit():
        await state.update_data(card_number=message.text)
        await message.answer("Iltimos summani kiriting")
        await state.set_state(WithdrawState.withdrawSum)
    else:
        await message.answer("Karta raqami noto'g'ri iltimos karta raqamini qaytadan kiriting!")
        await state.set_state(WithdrawState.card)


@dp.message(WithdrawState.withdrawSum)
async def withdraw_sum(message: types.Message, state=FSMContext):
    if message.text.replace(".", "").isdigit() and float(message.text) > 0:
        await state.update_data(withdraw_sum=message.text)
        state_date = await state.get_data()
        card = state_date.get('card_number')
        withdraw = state_date.get('withdraw_sum')
        current_balance = await get_balance(user_id=message.from_user.id, valute="uz")
        if float(withdraw) >= float(current_balance):
            await message.answer("Hisobingizda yetarlicha mablag' yo'q")
            await state.set_state(WithdrawState.withdrawSum)
            await message.delete()
        else:
            await update_balance(user_id=message.from_user.id, valute="uz", new_balance=-1 * float(withdraw))
            await message.answer(
                f"{message.chat.first_name} {message.chat.last_name} hisobingizdan {withdraw} UZS muvaffaqiyatli qirqildi 🥳",
                reply_markup=back_btn())
            await insert_history(user_id=message.from_user.id, username=message.from_user.username,
                                 firstname=message.from_user.first_name, lastname=message.from_user.last_name,
                                 created_at=datetime.datetime.now(), action_type="Hisobdan mablag' chiqarish",
                                 uz_sum=float(withdraw),
                                 crypto_name="None",
                                 crypto_sum=0.0,
                                 card=card)
            await state.clear()
    else:
        await message.answer("Iltimos summani to'g'ri kiriting ⚠️")
        await state.set_state(WithdrawState.withdrawSum)


@dp.callback_query(lambda callback_query: callback_query.data == 'market')
async def market_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="🗳 P2P Market\n Siz bu bo'limda kriptovalyuta sotib olishingiz yoki sotishingiz mumkin. Agar siz biror muammoga duch kelsangiz iltimos biz bilan bog'laning!",
                           reply_markup=market_btn())
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@dp.callback_query(lambda callback_query: callback_query.data == 'sell')
async def sell_msg(callback: types.CallbackQuery, state=FSMContext):
    await bot.send_message(chat_id=callback.message.chat.id, text="Sotmoqchi bo'lgan kriptovalyutani tanlang",
                           reply_markup=crypto_currency())
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(SellState.currency)


@dp.message(SellState.currency)
async def sell_currency(message: types.Message, state: FSMContext):
    await state.update_data(currency=message.text)
    uz_balance = await get_balance(user_id=message.from_user.id, valute="uz")
    await message.answer(f"Sizning balansingiz:{uz_balance}UZS. Kriptovalyuta miqdorini kiriting!",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SellState.value)


@dp.message(SellState.value)
async def sell_value(message: types.Message, state=FSMContext):
    if message.text.replace(".", "").isdigit():
        await state.update_data(value=message.text)
        state_date = await state.get_data()
        crypto_value = float(state_date.get('value'))
        crypto_valute = state_date.get('currency')
        crypto_balance = await get_balance(user_id=message.from_user.id, valute=crypto_valute)
        crypto_price = get_crypto_price(crypto_valute.upper())
        if crypto_balance >= crypto_value:
            await message.answer(
                f"{crypto_value} {crypto_valute.upper()} muvaffaqiyatli sotildi.1 {crypto_valute.upper()} == {crypto_price} UZS",
                reply_markup=back_btn())
            await update_balance(user_id=message.from_user.id, valute=crypto_valute, new_balance=-1 * crypto_value)
            await update_balance(user_id=message.from_user.id, valute="uz", new_balance=crypto_price * crypto_value)
            await insert_history(user_id=message.from_user.id, username=message.from_user.username,
                                 firstname=message.from_user.first_name, lastname=message.from_user.last_name,
                                 created_at=datetime.datetime.now(), action_type="Kriptovalyuta sotish",
                                 uz_sum=0.0,
                                 crypto_name=crypto_valute,
                                 crypto_sum=crypto_value,
                                 card="None")
            await state.clear()
        else:
            await message.answer(f"Hisobingizda yetarlicha {crypto_valute} yo'q")
            await state.set_state(SellState.value)
    else:
        await message.answer("Iltimos kriptovalyuta miqdorini to'g'ri kiriting")
        await state.set_state(SellState.value)


@dp.callback_query(lambda callback_query: callback_query.data == 'buy')
async def buy_msg(callback: types.CallbackQuery, state=FSMContext):
    await bot.send_message(chat_id=callback.message.chat.id, text="Sotib olmoqchi bo'lgan kriptovalyutani tanlang",
                           reply_markup=crypto_currency())
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(BuyState.currency)


@dp.message(BuyState.currency)
async def buy_currency(message: types.Message, state: FSMContext):
    await state.update_data(currency=message.text)
    uz_balance = await get_balance(user_id=message.from_user.id, valute="uz")
    await message.answer(f"Sizning balansingiz:{uz_balance}UZS. Kriptovalyuta miqdorini kiriting!",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(BuyState.value)


@dp.message(BuyState.value)
async def buy_value(message: types.Message, state=FSMContext):
    if message.text.replace(".", "").isdigit():
        await state.update_data(value=message.text)
        state_date = await state.get_data()
        crypto_value = float(state_date.get('value'))
        crypto_valute = state_date.get('currency')
        uz_balance = await get_balance(user_id=message.from_user.id, valute="uz")
        crypto_price = get_crypto_price(crypto_valute.upper())
        if uz_balance >= crypto_value * crypto_price:
            await message.answer(
                f"{crypto_value} {crypto_valute} muvaffaqiyatli sotib olindi.1 {crypto_valute.upper()} == {crypto_price} UZS",
                reply_markup=back_btn())
            await insert_history(user_id=message.from_user.id, username=message.from_user.username,
                                 firstname=message.from_user.first_name, lastname=message.from_user.last_name,
                                 created_at=datetime.datetime.now(), action_type="Kriptovalyuta sotib olish",
                                 uz_sum=0.0,
                                 crypto_name=crypto_valute,
                                 crypto_sum=crypto_value,
                                 card="None")
            await update_balance(user_id=message.from_user.id, valute=crypto_valute, new_balance=crypto_value)
            await update_balance(user_id=message.from_user.id, valute="uz",
                                 new_balance=-1 * crypto_price * crypto_value)
            await state.clear()
        else:
            await message.answer(f"Hisobingizda yetarlicha mablag' yo'q")
            await state.set_state(BuyState.value)
    else:
        await message.answer("Iltimos kriptovalyuta miqdorini to'g'ri kiriting!")
        await state.set_state(BuyState.value)


@dp.callback_query(lambda callback_query: callback_query.data == 'settings')
async def settings_msg(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="⚙️ Sozlamalar",
                           reply_markup=setting_btn())
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@dp.callback_query(lambda callback_query: callback_query.data == 'currency')
async def crypto_course(callback: types.CallbackQuery):
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
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    else:
        message += "\nKurslar  yangilanmadi."
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.send_message(callback.message.chat.id, message, reply_markup=back_btn())


@dp.callback_query(lambda callback_query: callback_query.data == 'back')
async def back_msg(callback: types.CallbackQuery):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="👨‍💻 Xizmatlar👇",
                           reply_markup=services_btn())


@dp.callback_query(lambda callback_query: callback_query.data == 'contact')
async def back_msg(callback: types.CallbackQuery, state=FSMContext):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="Botni ishlatishda duch kelgan muammolaringizni yoki o'z talab-takliflaringizni yozing. Sizning har bir fikringiz biz uchun muhim!")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
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


@dp.callback_query(lambda callback_query: callback_query.data == 'monitoring')
async def history(callback: types.CallbackQuery):
    base_xsl = export_history_to_excel(callback.from_user.id)
    res = types.FSInputFile(base_xsl)
    await bot.send_document(chat_id=callback.message.chat.id, document=res,
                            caption="Sizning barcha amaliyotlariz ro'yxati", reply_markup=back_btn())
    os.remove(f'{callback.from_user.id}.xlsx')


@dp.message(F.text == "⬅️ Orqaga")
async def start_msg(message: types.Message):
    await message.answer("Xizmatlar 👇",
                         reply_markup=services_btn())


@dp.message(Command('admin'), F.from_user.id.in_(ADMIN_IDS))
async def admin_panel(message: types.Message):
    await message.answer(
        "Admin panelga xush kelibsiz 🆒", reply_markup=admin_menu()
    )


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
    await db_history()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
