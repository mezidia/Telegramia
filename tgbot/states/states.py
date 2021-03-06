from aiogram.dispatcher.filters.state import State, StatesGroup


class Player(StatesGroup):
    user_id = State()
    telegram_name = State()
    name = State()
    level = State()
    experience = State()
    health = State()
    energy = State()
    strength = State()
    agility = State()
    intuition = State()
    intelligence = State()
    hero_class = State()
    nation = State()
    money = State()
    items = State()
    mount = State()
    current_state = State()


class Road(StatesGroup):
    road_name = State()


class Item(StatesGroup):
    item = State()
    type = State()


class Horse(StatesGroup):
    horse = State()


class CityObject(StatesGroup):
    city_object = State()
