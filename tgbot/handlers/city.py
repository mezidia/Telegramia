from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from tgbot.states.states import CityObject
from tgbot.config import Config
from tgbot.models.database import Client
from tgbot.misc.city_objects import city_objects
from tgbot.misc.commands import handle_commands
from tgbot.handlers.echo import echo


async def answer_city_object(message: Message, state: FSMContext):
    text = message.text
    if text == "Назад":
        return await echo(message, state)
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    user_id = message.from_user.id
    player = client.get({"user_id": user_id}, "players")
    for city_object in city_objects:
        if city_object["ukr_name"] == text:
            await state.finish()
            return await city_object["function"](player_info=player, message=message)


def register_city_object(dp: Dispatcher):
    dp.register_message_handler(answer_city_object, state=CityObject.city_object)
