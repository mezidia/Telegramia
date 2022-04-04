from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from states.horse import Horse
from utils.db_api.database import Client
from utils.misc import commands
from utils.city.parsers import parse_purchase
from utils.city.checks import check_money
from utils.city.info import show_city_info
from data.config import DB_PASSWORD
from handlers.users.echo import echo


@dp.message_handler(state=Horse.horse)
async def answer_horse_purchase(message: Message, state: FSMContext):
    text = message.text
    if text == "Назад":
        return await echo(message, state)
    if not text.startswith("/"):
        client = Client(DB_PASSWORD)
        user_id = message.from_user.id
        player = client.get({"user_id": user_id}, "players")
        horse, price = parse_purchase(text)
        if check_money(player, price):
            try:
                player_mount = client.get({"name": player["mount"]["name"]}, "horses")
            except KeyError:
                player_mount = {"name": "", "price": 0}
            if player_mount["name"] == horse:
                await message.answer("У вас вже є цей кінь")
            else:
                await state.finish()
                mount = client.get({"name": horse}, "horses")
                client.update(
                    {"user_id": user_id},
                    {
                        "mount": mount,
                        "money": player["money"] - price + player_mount["price"],
                    },
                    "players",
                )
                client.update(
                    {"name": mount["name"]},
                    {"count": 1},
                    "horses",
                    "$inc",
                )
                await message.answer(f"Ви успішно купили {horse}")
        else:
            await message.answer("У вас недостатньо грошей")
        return await show_city_info(player["current_state"], message.chat.id, state)
    else:
        return await commands.handle_commands(message, text)