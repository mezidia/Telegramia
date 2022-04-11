from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from tgbot.states.states import Horse
from tgbot.config import Config
from tgbot.models.database import Client
from tgbot.misc.commands import handle_commands
from tgbot.misc.parsers import parse_purchase
from tgbot.misc.checks import check_money
from tgbot.misc.city import show_city_info
from tgbot.handlers.echo import echo


async def answer_horse_purchase(message: Message, state: FSMContext):
    text = message.text
    if text == "Назад":
        return await echo(message, state)
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
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
    return await show_city_info(player["current_state"], message, state)


def register_answer_horse(dp: Dispatcher):
    dp.register_message_handler(answer_horse_purchase, state=Horse.horse)
