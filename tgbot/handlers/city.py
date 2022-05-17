import logging

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from tgbot.states.states import CityObject
from tgbot.misc.city.city_objects import city_objects
from tgbot.handlers.echo import echo

from loader import dp


@dp.message_handler(state=CityObject.city_object)
async def answer_city_object(message: Message, state: FSMContext, player: dict) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    text = message.text
    if text == "Назад":
        return await echo(message, state, player)
    for city_object in city_objects:
        if city_object["ukr_name"] == text:
            await state.finish()
            return await city_object["function"](player_info=player, message=message)
