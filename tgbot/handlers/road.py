from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from tgbot.config import Config
from tgbot.states.states import Road
from tgbot.misc.parsers import parse_road_name
from tgbot.models.database import Client
from tgbot.misc.checks import check_energy
from tgbot.misc.player_processes import level_up
from tgbot.misc.city import show_city_info
from tgbot.misc.commands import handle_commands
from tgbot.handlers.echo import echo


async def answer_road_choice(message: Message, state: FSMContext):
    road_name = parse_road_name(message.text)
    if road_name == "Назад":
        return await echo(message, state)
    if not road_name.startswith("/"):
        config: Config = message.bot.get("config")
        client = Client(config.db.password)
        user_id = message.from_user.id
        player = client.get({"user_id": user_id}, "players")
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
    else:
        return await handle_commands(message, road_name)


def register_road(dp: Dispatcher):
    dp.register_message_handler(answer_road_choice, state=Road.road_name)
