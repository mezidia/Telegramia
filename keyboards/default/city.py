from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.city.objects import city_objects


def create_markup(city: dict):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=3
    )
    buttons = []
    for city_object in city_objects:
        try:
            if city[city_object["name"]]:
                buttons.append(KeyboardButton(city_object["ukr_name"]))
        except KeyError:
            pass
    buttons.append(KeyboardButton("Дороги"))
    markup.add(*buttons)
    return markup
