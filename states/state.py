from aiogram.fsm.state import State, StatesGroup


class ContactState(StatesGroup):
    requirementTxt = State()
