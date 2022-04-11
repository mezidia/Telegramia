from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import Config
from tgbot.models.database import Client


async def delete_handler(message: Message) -> Message:
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    client.delete({'user_id': message.from_user.id}, 'players')
    return await message.answer('Ви успішно видалили свій профіль!')


def register_delete_handler(dp: Dispatcher):
    dp.register_message_handler(delete_handler, commands=["delete"], state='*')
