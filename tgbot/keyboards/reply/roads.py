from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def create_markup(roads: tuple):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for road in roads:
        markup.add(KeyboardButton(f'{road["name"]} - {road["energy"]} енергії'))
    markup.add(KeyboardButton("Назад"))
    return markup
