import logging

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from tgbot.states.states import Road
from tgbot.misc.parsers import parse_road_name
from tgbot.models.database import Client
from tgbot.misc.checks import check_energy
from tgbot.misc.player_processes import level_up
from tgbot.misc.city import show_city_info
from tgbot.handlers.echo import echo
from loader import dp


@dp.message_handler(state=Road.road_name)
async def answer_road_choice(message: Message, state: FSMContext, player: dict):
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    road_name = parse_road_name(message.text)
    if road_name == "Назад":
        return await echo(message, state, player)
    client: Client = message.bot.get('client')
    user_id = message.from_user.id
    road = client.get({"name": road_name}, "roads")
    road_energy = float(road["energy"])
    if check_energy(player, road_energy):
        await state.finish()
        experience, level_to_add = level_up(player["experience"])
        experience += road_energy * 0.35
        if mount := player["mount"]:
            road_energy -= mount["bonus"]
        client.update(
            {"user_id": user_id},
            {
                "current_state": road["to_obj"],
                "level": player["level"] + level_to_add,
                "energy": player["energy"] - road_energy + player["agility"] * 0.15,
                "experience": experience,
            },
            "players",
        )
        client.update(
            {"name": road["name"]},
            {
                "travelers": 1,
            },
            "roads",
            "$inc",
        )
    else:
        await message.answer("У вас недостатньо енергії")
    return await show_city_info(road["to_obj"], message, state)
