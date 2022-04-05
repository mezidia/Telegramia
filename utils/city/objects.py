from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroupMeta

from utils.db_api.database import Client
from utils.city.checks import check_in_raid, check_in_dungeon, check_health, check_was_in_raid
from utils.city.player_processes import apply_items
from utils.misc.types import types
from data.config import DB_PASSWORD
from states import road, item, horse
from keyboards.default import roads as roads_markup, items as items_markup
from keyboards.inline import recover

from datetime import datetime


async def show_roads(player_info: dict, message: Message) -> Message:
    client = Client(DB_PASSWORD)
    if check_in_dungeon(player_info, client) or check_in_raid(player_info, client):
        return await message.answer("Ви все ще проходите завдання, потрібно зачекати")
    roads = client.get_all("roads", {"from_obj": player_info["current_state"]})
    markup = roads_markup.create_markup(roads)
    await road.Road.first()
    return await message.answer(
        "Оберіть місце, куди хочете відправитись", reply_markup=markup
    )

async def create_markup_for_shop(
    collection_name: str, city_name: str, state: StatesGroupMeta, message: Message, type: str = None
) -> Message:
    client = Client(DB_PASSWORD)
    query = {"city": city_name}
    if type:
        query["type"] = type
    items = client.get_all(collection_name, query)
    markup = items_markup.create_markup(items)
    await state.first()
    return await message.answer(
        "Оберіть предмет, який хочете купити", reply_markup=markup
    )


async def create_recover_markup(
    characteristic: str, text: str, message: Message
) -> Message:
    markup = recover.create_markup(characteristic)
    return await message.answer(
        text,
        reply_markup=markup,
    )


async def show_items(player_info: dict, message: Message, type: str) -> Message:
    return await create_markup_for_shop(
        "items", player_info["current_state"], item.Item, message, type
    )

# TODO: do something with the variable
async def show_item_types(player_info: dict, message: Message) -> Message:
    await item.Item.first()
    markup = items_markup.create_markup_for_types(types.keys())
    return await message.answer("Оберіть тип предмету", reply_markup=markup)


async def show_horses(player_info: dict, message: Message) -> Message:
    return await create_markup_for_shop(
        "horses", player_info["current_state"], horse.Horse, message
    )


async def enter_academy(player_info: dict, message: Message) -> Message:
    return await create_recover_markup(
        "intelligence",
        f'Ви знаходитесь в академії міста {player_info["current_state"]}'
        f' і у вас {player_info["intelligence"]} інтелекту. Ви хочете провести навчання в академії?',
        message,
    )


async def enter_temple(player_info: dict, message: Message):
    return await create_recover_markup(
        "health",
        f'Ви знаходитесь у храмі міста {player_info["current_state"]}'
        f' і у вас {player_info["health"]} здоров\'я. Ви хочете відновити його?',
        message,
    )


async def enter_tavern(player_info: dict, message: Message):
    markup = await create_recover_markup(
        "energy",
        f'Ви знаходитесь у таверні міста {player_info["current_state"]}'
        f' і у вас {player_info["energy"]} енергії. Ви хочете відновити її?',
        message,
    )


async def show_dungeon(player_info: dict, message: Message):
    client = Client(DB_PASSWORD)
    dungeon = client.get({"name": player_info["current_state"]}, "dungeons")
    text = (
        f'🌇Підземелля - {dungeon["name"]}\n\n📖{dungeon["description"]}\n\n'
        f'Буде отримано шкоди - {dungeon["damage"]}\n\n'
        f'💵Буде отримано нагороди - {dungeon["treasure"]}\n\n'
        f'⌚Час взяття підземелля - {dungeon["base_time"]} с'
    )
    await message.answer(text)


async def enter_dungeon(player_info: dict, message: Message):
    client = Client(DB_PASSWORD)
    if check_in_dungeon(player_info, client):
        return await message.answer("Ви вже у підземеллі")
    dungeon = client.get({"name": player_info["current_state"]}, "dungeons")
    if check_health(player_info, dungeon["damage"]):
        date = datetime.now()
        members = dungeon["members"]
        members[player_info["name"]] = date
        player_chars = apply_items(player_info, client)
        user_id = player_info["user_id"]
        client.update(
            {"name": player_info["current_state"]}, {"members": members}, "dungeons"
        )
        client.update(
            {"user_id": user_id},
            {
                "health": player_info["health"]
                - dungeon["damage"]
                + player_chars["strength"] * 0.15,
                "money": player_info["money"]
                + dungeon["treasure"]
                + player_chars["intuition"] * 0.15,
                "experience": player_info["experience"] + dungeon["treasure"] * 0.25,
            },
            "players",
        )
        return await message.answer(
            f"Ви почали захоплення підземелля. "
            f'Повернутись у місто ви можете через {dungeon["base_time"]} секунд'
        )
    return await message.answer(
        "У вас недостатньо здоров'я. Поверніться у місто, щоб вилікуватись"
    )


async def show_raid(player_info: dict, message: Message):
    client = Client(DB_PASSWORD)
    raid = client.get({"name": player_info["current_state"]}, "raids")
    text = f'Рейд - {raid["name"]}\n\n📖{raid["description"]}\n\n'
    raid_levels = client.get_all(
        "raid_levels", {"raid_name": player_info["current_state"]}
    )
    for raid_level in raid_levels:
        text += (
            f'{raid_level["level"]}. Рівень рейду - {raid_level["name"]}\n\n📖{raid_level["description"]}\n\n'
            f'Буде отримано шкоди - {raid_level["damage"]}\n\n'
            f'💵Буде отримано нагороди - {raid_level["treasure"]}\n\n'
            f'⌚Час взяття підземелля - {raid_level["base_time"]} с\n\n'
        )
    await message.answer(text)


async def show_raid_level(player_info: dict, message: Message):
    client = Client(DB_PASSWORD)
    raid = client.get({"name": player_info["current_state"]}, "raids")
    raid_members = raid["members"]
    try:
        player_in_raid_info = raid_members[player_info["name"]]
    except KeyError:
        return await message.answer("Ви ще не увійшли у підземелля")
    if raid_level := client.get(
        {
            "raid_name": player_info["current_state"],
            "level": player_in_raid_info["level"] + 1,
        },
        "raid_levels",
    ):
        text = (
            f'Рівень рейду - {raid_level["name"]}\n\n📖{raid_level["description"]}\n\n'
            f'Буде отримано шкоди - {raid_level["damage"]}\n\n'
            f'⌚Час взяття підземелля - {raid_level["base_time"]} с'
        )
        photo_url = f"https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{raid_level['name']}.jpg"
        return await message.answer_photo(photo_url, text)
    return await message.answer("Більше рівнів немає")


async def enter_raid(player_info: dict, message: Message):
    client = Client(DB_PASSWORD)
    if check_in_raid(player_info, client):
        return await message.answer("Ви вже у підземеллі")
    raid = client.get({"name": player_info["current_state"]}, "raids")
    if level := check_was_in_raid(player_info, client):
        level += 1
        if raid_level := client.get(
            {"raid_name": raid["name"], "level": level}, "raid_levels"
        ):
            pass
        else:
            return await message.answer("Ви вже пройшли усі рівні рейду")
    else:
        raid_level = client.get({"raid_name": raid["name"], "level": 1}, "raid_levels")
    if check_health(player_info, raid_level["damage"]):
        date = datetime.now()
        members = raid["members"]
        player_chars = apply_items(player_info, client)
        members[player_info["name"]] = {"time": date, "level": raid_level["level"]}
        user_id = player_info["user_id"]
        client.update(
            {"name": player_info["current_state"]}, {"members": members}, "raids"
        )
        client.update(
            {"user_id": user_id},
            {
                "health": player_info["health"]
                - raid_level["damage"]
                + player_chars["strength"] * 0.15,
                "money": player_info["money"]
                + raid_level["treasure"]
                + player_chars["intelligence"] * 0.15,
                "experience": player_info["experience"]
                + raid_level["treasure"] * 0.25 * raid_level["level"],
            },
            "players",
        )
        return await message.answer(
            f"Ви почали захоплення рівня {raid_level['level']} рейду. "
            f'Повернутись у місто ви можете через {raid_level["base_time"]} секунд'
        )
    return await message.answer(
        "У вас недостатньо здоров'я. Поверніться у місто, щоб вилікуватись"
    )



city_objects = [
    {"name": "market", "ukr_name": "Ринок", "function": show_item_types},
    {"name": "academy", "ukr_name": "Академія", "function": enter_academy},
    {"name": "temple", "ukr_name": "Храм", "function": enter_temple},
    {"name": "tavern", "ukr_name": "Таверна", "function": enter_tavern},
    {"name": "menagerie", "ukr_name": "Стойло", "function": show_horses},
    {"name": "roads", "ukr_name": "Дороги", "function": show_roads},
    {
        "name": "dungeon_info",
        "ukr_name": "Інформація про підземелля",
        "function": show_dungeon,
    },
    {
        "name": "dungeon_enter",
        "ukr_name": "Увійти у підземелля",
        "function": enter_dungeon,
    },
    {"name": "raid_enter", "ukr_name": "Увійти у рейд", "function": enter_raid},
    {"name": "raid_info", "ukr_name": "Інформація про рейд", "function": show_raid},
    {
        "name": "raid_level_info",
        "ukr_name": "Інформація про наступний рівень рейду",
        "function": show_raid_level,
    },
]
