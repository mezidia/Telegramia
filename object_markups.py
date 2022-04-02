from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroupMeta

from database import Client
from config import DB_PASSWORD
from states import Item, Road, Horse
from utils import (
    check_health,
    check_in_dungeon,
    check_in_raid,
    check_was_in_raid,
    apply_items,
)

from datetime import datetime


async def show_roads(player_info: dict, message: types.Message) -> types.Message:
    client = Client(DB_PASSWORD)
    if check_in_dungeon(player_info, client) or check_in_raid(player_info, client):
        return await message.answer("Ви все ще проходите завдання, потрібно зачекати")
    roads = client.get_all("roads", {"from_obj": player_info["current_state"]})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for road in roads:
        # TODO - add energy value and then parse road name
        markup.add(types.KeyboardButton(road["name"]))
    markup.add(types.KeyboardButton("Назад"))
    await Road.first()
    return await message.answer(
        "Оберіть місце, куди хочете відправитись", reply_markup=markup
    )


async def create_markup_for_shop(
    collection_name: str, city_name: str, state: StatesGroupMeta, message: types.Message
) -> types.ReplyKeyboardMarkup:
    client = Client(DB_PASSWORD)
    items = client.get_all(collection_name, {"city": city_name})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in items:
        markup.add(types.KeyboardButton(f'Купити {item["name"]} за {item["price"]}'))
    markup.add(types.KeyboardButton("Назад"))
    await state.first()
    return await message.answer(
        "Оберіть предмет, який хочете купити", reply_markup=markup
    )


async def create_recover_markup(
    characteristic: str, text: str, message: types.Message
) -> types.Message:
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text=f"Отримати 5 одиниць {characteristic} за 5 монет",
            callback_data=f"5{characteristic}5",
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            text=f"Отримати 15 одиниць {characteristic} за 13 монет",
            callback_data=f"15{characteristic}13",
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            text=f"Отримати 50 одиниць {characteristic} за 45 монет",
            callback_data=f"50{characteristic}45",
        )
    )
    markup.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
    return await message.answer(
        text,
        reply_markup=markup,
    )


async def show_items(player_info: dict, message: types.Message) -> types.Message:
    return await create_markup_for_shop(
        "items", player_info["current_state"], Item, message
    )


async def show_horses(player_info: dict, message: types.Message) -> types.Message:
    return await create_markup_for_shop(
        "horses", player_info["current_state"], Horse, message
    )


async def enter_academy(player_info: dict, message: types.Message) -> types.Message:
    return await create_recover_markup(
        "intelligence",
        f'Ви знаходитесь в академії міста {player_info["current_state"]}'
        f' і у вас {player_info["intelligence"]} інтелекту. Ви хочете провести навчання в академії?',
        message,
    )


async def enter_temple(player_info: dict, message: types.Message):
    return await create_recover_markup(
        "health",
        f'Ви знаходитесь у храмі міста {player_info["current_state"]}'
        f' і у вас {player_info["health"]} здоров\'я. Ви хочете відновити його?',
        message,
    )


async def enter_tavern(player_info: dict, message: types.Message):
    markup = await create_recover_markup(
        "energy",
        f'Ви знаходитесь у таверні міста {player_info["current_state"]}'
        f' і у вас {player_info["energy"]} енергії. Ви хочете відновити її?',
        message,
    )


async def show_dungeon(player_info: dict, message: types.Message):
    client = Client(DB_PASSWORD)
    dungeon = client.get({"name": player_info["current_state"]}, "dungeons")
    text = (
        f'🌇Підземелля - {dungeon["name"]}\n\n📖{dungeon["description"]}\n\n'
        f'Буде отримано шкоди - {dungeon["damage"]}\n\n'
        f'💵Буде отримано нагороди - {dungeon["treasure"]}\n\n'
        f'⌚Час взяття підземелля - {dungeon["base_time"]} с'
    )
    await message.answer(text)


async def enter_dungeon(player_info: dict, message: types.Message):
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


async def show_raid(player_info: dict, message: types.Message):
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


async def show_raid_level(player_info: dict, message: types.Message):
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


async def enter_raid(player_info: dict, message: types.Message):
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
