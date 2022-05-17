import logging

from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from tgbot.models.database import Client

from loader import dp


@dp.message_handler(Command('delete'), state='*')
async def delete_handler(message: Message) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    client: Client = message.bot.get('client')
    client.delete({'user_id': message.from_user.id}, 'players')
    return await message.answer('Ви успішно видалили свій профіль!')
