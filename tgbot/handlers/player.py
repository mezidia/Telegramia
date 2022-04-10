from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import Config
from tgbot.misc.city import show_city_info
from tgbot.misc.info import prepare_player_info
from tgbot.models.database import Client


async def send_place_info(message: Message) -> Message:
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    user_id = message.from_user.id
    city_name = client.get({"user_id": user_id}, "players")
    return await show_city_info(city_name["current_state"], message)


async def show_player_handler(message: Message) -> Message:
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    user_id = message.from_user.id
    player = client.get({"user_id": user_id}, "players")
    text = await prepare_player_info(player)
    return await message.answer(text)


def register_player(dp: Dispatcher):
    dp.register_message_handler(send_place_info, is_player=True, commands=["where"])
    dp.register_message_handler(show_player_handler, is_player=True, commands=["me"])
