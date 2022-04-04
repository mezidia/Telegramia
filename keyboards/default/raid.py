from pickletools import markobject
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_markup():
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=3
    )
    markup.add(KeyboardButton("Інформація про рейд"))
    markup.add(KeyboardButton("Інформація про наступний рівень рейду"))
    markup.add(KeyboardButton("Увійти у рейд"))
    markup.add(KeyboardButton("Дороги"))
    return markobject
