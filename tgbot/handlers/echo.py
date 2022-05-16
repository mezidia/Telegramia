import logging

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from tgbot.misc.city.city_objects import city_objects
from tgbot.misc.city.city import show_city_info

from loader import dp


@dp.message_handler(is_player=True)
async def echo(message: Message, state: FSMContext, player: dict) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    text = message.text

    for city_object in city_objects:
        if city_object["ukr_name"] == text:
            await state.finish()
            return await city_object["function"](player, message)
    return await show_city_info(player["current_state"], message, state)
