from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from states.road import Road
from utils.city.parsers import parse_road_name
from utils.db_api.database import Client
from utils.city.checks import check_energy
from utils.city.player_processes import level_up
from utils.city.info import show_city_info
from utils.misc import commands
from data.config import DB_PASSWORD
from handlers.users.echo import echo


@dp.message_handler(state=Road.road_name)
async def answer_road_choice(message: Message, state: FSMContext):
    road_name = parse_road_name(message.text)
    if road_name == "Назад":
        return await echo(message, state)
    if not road_name.startswith("/"):
        client = Client(DB_PASSWORD)
        user_id = message.from_user.id
        player = client.get({"user_id": user_id}, "players")
        road = client.get({"name": road_name}, "roads")
        road_energy = float(road["energy"])
        if check_energy(player, road_energy):
            await state.finish()
            if mount := player["mount"]:
                road_energy -= mount["bonus"]
            experience, level_to_add = level_up(player["experience"])
            experience += road_energy * 0.35
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
        return await show_city_info(road["to_obj"], message.chat.id, state)
    else:
        return await commands.handle_commands(message, road_name)
