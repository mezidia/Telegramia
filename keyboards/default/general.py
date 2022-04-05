from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from utils.db_api.database import Client
from data.config import DB_PASSWORD


async def create_markup(collection_name: str, field_name: str) -> ReplyKeyboardMarkup:
    client = Client(DB_PASSWORD)
    objects = client.get_all(collection_name)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for object_ in objects:
        btn = KeyboardButton(object_[field_name])
        buttons.append(btn)
    markup.add(*buttons)
    return markup


async def delete_markup() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
