from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import Config
from tgbot.misc.city import show_city_info
from tgbot.misc.info import prepare_player_info
from tgbot.models.database import Client
from loader import dp


@dp.message_handler(is_player=True, commands=["where"], state="*")
async def send_place_info(message: Message) -> Message:
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    user_id = message.from_user.id
    city_name = client.get({"user_id": user_id}, "players")
    return await show_city_info(city_name["current_state"], message)

@dp.message_handler(is_player=True, commands=["me"], state="*")
async def show_player_handler(message: Message) -> Message:
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    user_id = message.from_user.id
    player = client.get({"user_id": user_id}, "players")
    text = await prepare_player_info(player)
    return await message.answer(text)
