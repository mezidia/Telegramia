import logging
from pprint import pprint

from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from tgbot.config import Config
from tgbot.misc.city import show_city_info
from tgbot.misc.info import prepare_player_info
from tgbot.models.database import Client
from loader import dp


@dp.message_handler(Command('where'), is_player=True, state="*")
async def send_place_info(message: Message, user: dict) -> Message:
    pprint(user)
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    user_id = message.from_user.id
    city_name = client.get({"user_id": user_id}, "players")
    return await show_city_info(city_name["current_state"], message)


@dp.message_handler(Command('me'), is_player=True, state="*")
async def show_player_handler(message: Message, user: dict) -> Message:
    pprint(user)
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    user_id = message.from_user.id
    player = client.get({"user_id": user_id}, "players")
    text = await prepare_player_info(player)
    return await message.answer(text)
