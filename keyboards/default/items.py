from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_markup(items: list):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in items:
        markup.add(KeyboardButton(f'Купити {item["name"]} за {item["price"]}'))
    markup.add(KeyboardButton("Назад"))
    return markup
