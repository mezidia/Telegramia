from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_markup():
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=3
    )

    markup.add(KeyboardButton("Інформація про підземелля"))
    markup.add(KeyboardButton("Увійти у підземелля"))
    markup.add(KeyboardButton("Дороги"))
    return markup
