from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_markup(items: tuple):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in items:
        markup.add(KeyboardButton(f'Купити {item["name"]} за {item["price"]}'))
    markup.add(KeyboardButton("Назад"))
    return markup


def create_markup_for_types(types: list):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for type_ in types:
        markup.add(KeyboardButton(type_))
    markup.add(KeyboardButton("Назад"))
    return markup
