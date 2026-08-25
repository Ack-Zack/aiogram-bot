from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    salary = State()
    bill = State()
    graphic = State()


class Name(StatesGroup):
    name = State()


class PayWages(StatesGroup):
    name = State()
    salary = State()
