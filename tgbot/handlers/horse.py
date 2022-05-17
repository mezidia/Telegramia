import logging

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from tgbot.states.states import Horse
from tgbot.models.database import Client
from tgbot.misc.system.parsers import parse_purchase
from tgbot.misc.system.checks import check_money
from tgbot.misc.city.city import show_city_info
from tgbot.handlers.echo import echo
from loader import dp


@dp.message_handler(state=Horse.horse)
async def answer_horse_purchase(message: Message, state: FSMContext, player: dict) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    text = message.text
    if text == "Назад":
        return await echo(message, state, player)
    client: Client = message.bot.get('client')
    user_id = message.from_user.id
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
