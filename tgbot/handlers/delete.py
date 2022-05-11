import logging

from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import Config
from tgbot.models.database import Client

from loader import dp


@dp.message_handler(commands=["delete"], state='*')
async def delete_handler(message: Message) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    client.delete({'user_id': message.from_user.id}, 'players')
    return await message.answer('Ви успішно видалили свій профіль!')
