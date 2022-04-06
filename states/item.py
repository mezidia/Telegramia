from aiogram.dispatcher.filters.state import State, StatesGroup


class Item(StatesGroup):
    item = State()
    type = State()
