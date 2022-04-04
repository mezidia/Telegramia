from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from loader import dp
from utils.db_api.database import Client
from utils.city.info import show_city_info
from utils.player.info import prepare_player_info
from data.config import DB_PASSWORD


class IsPlayer(BoundFilter):
    key = 'is_player'

    def __init__(self, is_player: bool):
        self.is_player = is_player
    
    async def check(self, message: Message) -> bool:
        client = Client(DB_PASSWORD)
        user_id = message.from_user.id
        if client.get({'user_id': user_id}, 'players') is not None:
            return True
        return False

dp.filters_factory.bind(IsPlayer, event_handlers=[dp.message_handlers])


@dp.message_handler(is_player=True, commands=["where"])
async def send_place_info(message: Message) -> Message:
    client = Client(DB_PASSWORD)
    user_id = message.from_user.id
    chat_id = message.chat.id
    city_name = client.get({"user_id": user_id}, "players")
    await show_city_info(city_name["current_state"], chat_id)


@dp.message_handler(is_player=True, commands=["me"])
async def show_player_handler(message: Message) -> Message:
    client = Client(DB_PASSWORD)
    user_id = message.from_user.id
    player = client.get({"user_id": user_id}, "players")
    text = await prepare_player_info(player)
    await message.answer(text)
