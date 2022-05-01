from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from tgbot.config import Config
from tgbot.models.database import Client
from tgbot.misc.city_objects import city_objects
from tgbot.misc.city import show_city_info


async def echo(message: Message, state: FSMContext) -> Message:
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    user_id = message.from_user.id
    text = message.text
    player = client.get({"user_id": user_id}, "players")

    for city_object in city_objects:
        if city_object["ukr_name"] == text:
            await state.finish()
            return await city_object["function"](player, message)
    return await show_city_info(player["current_state"], message, state)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo, is_player=True, state="*")