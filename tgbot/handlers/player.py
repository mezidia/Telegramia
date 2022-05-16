import logging

from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from tgbot.misc.city.city import show_city_info
from tgbot.misc.info import prepare_player_info
from loader import dp


@dp.message_handler(Command('where'), is_player=True, state="*")
async def send_place_info(message: Message, player: dict) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    return await show_city_info(player["current_state"], message)


@dp.message_handler(Command('me'), is_player=True, state="*")
async def show_player_handler(message: Message, player: dict) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    text = await prepare_player_info(player)
    return await message.answer(text)
