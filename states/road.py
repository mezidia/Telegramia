from aiogram.dispatcher.filters.state import State, StatesGroup

class Road(StatesGroup):
    road_name = State()
