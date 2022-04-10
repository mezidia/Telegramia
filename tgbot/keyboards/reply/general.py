from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Message

from tgbot.models.database import Client
from tgbot.config import Config


async def create_markup(collection_name: str, field_name: str, message: Message) -> ReplyKeyboardMarkup:
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
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
