from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp
from .filters.is_player import IsPlayer
from utils.db_api.database import Client
from utils.city.objects import city_objects
from utils.city.info import show_city_info
from data.config import DB_PASSWORD


dp.filters_factory.bind(IsPlayer, event_handlers=[dp.message_handlers])


@dp.message_handler(is_player=True)
async def echo(message: Message, state: FSMContext) -> Message:
    client = Client(DB_PASSWORD)
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text
    player = client.get({"user_id": user_id}, "players")

    for city_object in city_objects:
        if city_object["ukr_name"] == text:
            await state.finish()
            return await city_object["function"](player, message)
    return await show_city_info(player["current_state"], chat_id, state)
