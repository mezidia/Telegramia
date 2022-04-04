from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from states.city import CityObject
from utils.db_api.database import Client
from data.config import DB_PASSWORD
from utils.city.objects import city_objects
from utils.misc import commands
from handlers.users.echo import echo


@dp.message_handler(state=CityObject.city_object)
async def answer_city_object(message: Message, state: FSMContext):
    text = message.text
    if text == "Назад":
        return await echo(message, state)
    if not text.startswith("/"):
        client = Client(DB_PASSWORD)
        user_id = message.from_user.id
        player = client.get({"user_id": user_id}, "players")
        for city_object in city_objects:
            if city_object["ukr_name"] == text:
                await state.finish()
                return await city_object["function"](player, message)
    else:
        return await commands.handle_commands(message, text)
