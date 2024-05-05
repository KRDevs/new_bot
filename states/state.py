from aiogram.fsm.state import State, StatesGroup


class ContactState(StatesGroup):
    requirementTxt = State()


class DepositState(StatesGroup):
    card = State()
    depositSum = State()


class WithdrawState(StatesGroup):
    card = State()
    withdrawSum = State()


class SellState(StatesGroup):
    currency = State()
    value = State()


class BuyState(StatesGroup):
    currency = State()
    value = State()
