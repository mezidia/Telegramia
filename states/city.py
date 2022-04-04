from aiogram.dispatcher.filters.state import State, StatesGroup


class CityObject(StatesGroup):
    city_object = State()
