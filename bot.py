# TODO: create map image
# TODO: make more separate files

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config import TELEGRAM_TOKEN, DB_PASSWORD
from filters import IsPlayer
from database import Client
from utils import (
    check_characteristics,
    check_money,
    check_energy,
    do_purchase,
    level_up,
    parse_purchase,
    parse_road_name,
    finish_state,
    smart_purchase,
)
from states import Player, CityObject, Item, Road, Horse
from object_markups import (
    show_items,
    enter_tavern,
    enter_temple,
    enter_academy,
    show_roads,
    show_horses,
    show_dungeon,
    enter_dungeon,
    show_raid,
    show_raid_level,
    enter_raid,
)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Activate filters
dp.filters_factory.bind(IsPlayer, event_handlers=[dp.message_handlers])

city_objects = [
    {"name": "market", "ukr_name": "Ринок", "function": show_items},
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

characteristics = ["energy", "health", "intelligence"]


async def create_keyboard(collection_name: str, field_name: str):
    client = Client(DB_PASSWORD)
    objects = client.get_all(collection_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for object_ in objects:
        btn = types.KeyboardButton(object_[field_name])
        buttons.append(btn)
    markup.add(*buttons)
    return markup


async def prepare_player_info(data):
    items = "пусто"
    if data["items"]:
        items = ""
        for item in data["items"]:
            items += f"{item}, "
    text = (
        f'Ігрове ім\'я: *{data["name"]}*\n🎖Рівень: *{data["level"]}*\n🌟Досвід: *{data["experience"]}*\n❤Здоров\'я: '
        f'*{data["health"]}*\nЕнергія: *{data["energy"]}*\n\n💪Сила: *{data["strength"]}*\n⚡Спритність: *{data["agility"]}*\n'
        f'🎯Інтуїція: *{data["intuition"]}*\n🎓Інтелект: *{data["intelligence"]}*\n💟Клас: *{data["hero_class"]}*\n\n'
        f'🤝Нація: *{data["nation"]}*\n💰Гроші: *{data["money"]}*\n🎒Речі: *{items}*\n'
        f'🐺Транспорт: *{data["mount"]["name"] if data["mount"] else "немає"}*\n'
        f'\nПоточне місце: *{data["current_state"]}*'
    )
    return text


async def show_city_info(city_name: str, chat_id: str, state=None) -> types.Message:
    client = Client(DB_PASSWORD)
    await finish_state(state)
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=3
    )
    photo_url = ""
    if dungeon := client.get({"name": city_name}, "dungeons"):
        markup.add(types.KeyboardButton("Інформація про підземелля"))
        markup.add(types.KeyboardButton("Увійти у підземелля"))
        markup.add(types.KeyboardButton("Дороги"))
        photo_url = f'https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{dungeon["name"]}.jpg'
    elif raid := client.get({"name": city_name}, "raids"):
        markup.add(types.KeyboardButton("Інформація про рейд"))
        markup.add(types.KeyboardButton("Інформація про наступний рівень рейду"))
        markup.add(types.KeyboardButton("Увійти у рейд"))
        markup.add(types.KeyboardButton("Дороги"))
        photo_url = f"https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{raid['name']}.jpg"
    else:
        photo_url = f"https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{city_name}.jpg"
        city = client.get({"name": city_name}, "cities")
        buttons = []
        for city_object in city_objects:
            try:
                if city[city_object["name"]]:
                    buttons.append(types.KeyboardButton(city_object["ukr_name"]))
            except KeyError:
                pass
        buttons.append(types.KeyboardButton("Дороги"))
        markup.add(*buttons)
    await CityObject.first()
    return await bot.send_photo(
        chat_id, photo_url, f"Ви знаходитесь у місті {city_name}", reply_markup=markup
    )


@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    client = Client(DB_PASSWORD)
    callback_data = callback_query.data
    for characteristic in characteristics:
        if characteristic in callback_data:
            value, price = callback_data.split(characteristic)
            player = client.get({"user_id": user_id}, "players")
            if check_money(player, float(price)) and check_characteristics(
                player, float(value), characteristic
            ):
                client.update(
                    {"user_id": user_id},
                    {
                        characteristic: player[characteristic] + float(value),
                        "money": player["money"] - float(price),
                    },
                    "players",
                )
                player = client.get({"user_id": user_id}, "players")
                await callback_query.answer(
                    f"Покупка здійснена! Ви збільшили {characteristic} на {value} одиниць"
                )
                return await show_city_info(
                    player["current_state"], callback_query.from_user.id
                )
            return await bot.send_message(
                callback_query.from_user.id,
                "У вас недостатньо грошей або ваш рівень замалий",
            )
    if callback_data == "No":
        client.delete({"user_id": user_id}, "players")
        await Player.nation.set()
        markup = await create_keyboard("countries", "name")
        return await bot.send_message(
            callback_query.from_user.id, "Оберіть країну", reply_markup=markup
        )
    else:
        player = client.get({"user_id": user_id}, "players")
        client.update({"name": player["hero_class"]}, {"choices": 1}, "classes", "$inc")
        return await show_city_info(
            player["current_state"], callback_query.from_user.id
        )


# Use state '*' if I need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext) -> types.Message:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return await message.reply("Процес реєстрації не починався.")
    await state.finish()
    return await message.reply("Реєстрація зупинена.")


@dp.message_handler(state=Player.nation)
async def answer_player_nation(
    message: types.Message, state: FSMContext
) -> types.Message:
    nation = message.text
    user_id = message.from_user.id
    telegram_name = message.from_user.username
    client = Client(DB_PASSWORD)
    country = client.get({"name": nation}, "countries")
    client.update({"name": country["name"]}, {"population": 1}, "countries", "$inc")
    await state.update_data({"nation": nation})
    await state.update_data({"user_id": user_id})
    await state.update_data({"telegram_name": telegram_name})
    await state.update_data({"level": 1.0})
    await state.update_data({"experience": 0.0})
    await state.update_data({"money": 100.0})
    await state.update_data({"items": []})
    await state.update_data({"mount": {"name": ""}})
    await state.update_data({"health": 100.0})
    await state.update_data({"energy": 60.0})
    await state.update_data({"current_state": country["capital"]})
    await message.answer(country["description"])
    await Player.name.set()
    return await message.answer("Напиши, як тебе звати")


@dp.message_handler(state=Player.name)
async def answer_player_name(
    message: types.Message, state: FSMContext
) -> types.Message:
    name = message.text
    await state.update_data({"name": name})
    markup = await create_keyboard("classes", "name")
    await Player.hero_class.set()
    return await message.answer("Обери свій клас", reply_markup=markup)


@dp.message_handler(state=Player.hero_class)
async def answer_player_class(
    message: types.Message, state: FSMContext
) -> types.Message:
    class_name = message.text
    await state.update_data({"hero_class": class_name})
    client = Client(DB_PASSWORD)
    class_ = client.get({"name": class_name}, "classes")
    await state.update_data({"strength": class_["characteristics"]["strength"]})
    await state.update_data({"agility": class_["characteristics"]["agility"]})
    await state.update_data({"intuition": class_["characteristics"]["intuition"]})
    await state.update_data({"intelligence": class_["characteristics"]["intelligence"]})
    data = await state.get_data()
    await state.finish()
    text = await prepare_player_info(data)
    client.insert(data, "players")
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Так", callback_data="Yes"),
        types.InlineKeyboardButton("Ні", callback_data="No"),
    )
    await message.answer(text, parse_mode="Markdown")
    return await message.answer("Вас задовільняє ваш персонаж?", reply_markup=markup)


@dp.message_handler(state=CityObject.city_object)
async def answer_city_object(message: types.Message, state: FSMContext):
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
        return await handle_commands(message, text)


@dp.message_handler(state=Item.item)
async def answer_item_purchase(message: types.Message, state: FSMContext):
    text = message.text
    if text == "Назад":
        return await echo(message, state)
    if not text.startswith("/"):
        client = Client(DB_PASSWORD)
        user_id = message.from_user.id
        player = client.get({"user_id": user_id}, "players")
        item, price = parse_purchase(text)
        if check_money(player, price):
            items = player["items"]
            if item in items:
                await message.answer("У вас вже є цей предмет")
            else:
                await state.finish()
                if items:
                    if old_item := smart_purchase(item, items, client):
                        items.append(item)
                        items.remove(old_item["name"])
                        price -= old_item["price"]
                        await message.answer(f"Ви успішно купили {item}")
                        do_purchase(client, player, items, price)
                    else:
                        await message.answer("У вас є кращий предмет такого ж типу")
                else:
                    items.append(item)
                    await message.answer(f"Ви успішно купили {item}")
                    do_purchase(client, player, items, price)
                client.update({"name": item}, {"count": 1}, "items", "$inc")
        else:
            await message.answer("У вас недостатньо грошей")
        return await show_city_info(player["current_state"], message.chat.id, state)
    else:
        return await handle_commands(message, text)


@dp.message_handler(state=Horse.horse)
async def answer_horse_purchase(message: types.Message, state: FSMContext):
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
        return await handle_commands(message, text)


@dp.message_handler(state=Road.road_name)
async def answer_road_choice(message: types.Message, state: FSMContext):
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
        return await handle_commands(message, road_name)


async def handle_commands(message: types.Message, text: str):
    commands = {
        "/create": create_player_handler,
        "/where": send_place_info,
        "/me": show_player_handler,
        "/start": show_start_text,
        "/help": show_help_text,
    }
    return await commands[text](message)


@dp.message_handler(commands=["start"])
async def show_start_text(message: types.Message) -> types.Message:
    text = "Вітаю у текстовій грі <b>Telegramia</b>. Створіть <i>свого героя</i> за допомогою команди /create. Дізнайтесь, як грати, через команду /help"
    return await message.answer(text, parse_mode="HTML")


@dp.message_handler(is_player=True, commands=["help"])
async def show_help_text(message: types.Message) -> types.Message:
    pass


@dp.message_handler(commands=["create"])
async def create_player_handler(message: types.Message) -> types.Message:
    client = Client(DB_PASSWORD)
    user_id = message.from_user.id
    if client.get({"user_id": user_id}, "players") is not None:
        return await message.reply("Ви вже зареєстровані")
    photo_url = (
        "https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_intro.jpg"
    )
    text = (
        "Вітаємо у магічному світі *Telegramia*. Цей світ повен пригод, цікавих людей, підступних ворогів, "
        "великих держав і ще багато чого іншого...Скоріше починай свою подорож. Для початку обери країну, "
        "у яку відправишся, щоб підкорювати цей світ"
    )
    markup = await create_keyboard("countries", "name")
    await Player.nation.set()
    await message.answer_photo(
        photo_url, text, parse_mode="Markdown", reply_markup=markup
    )


@dp.message_handler(is_player=True, commands=["where"])
async def send_place_info(message: types.Message) -> types.Message:
    client = Client(DB_PASSWORD)
    user_id = message.from_user.id
    chat_id = message.chat.id
    city_name = client.get({"user_id": user_id}, "players")
    await show_city_info(city_name["current_state"], chat_id)


@dp.message_handler(is_player=True, commands=["me"])
async def show_player_handler(message: types.Message) -> types.Message:
    client = Client(DB_PASSWORD)
    user_id = message.from_user.id
    player = client.get({"user_id": user_id}, "players")
    text = await prepare_player_info(player)
    await message.answer(text, parse_mode="Markdown")


@dp.message_handler()
async def echo(message: types.Message, state: FSMContext) -> types.Message:
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


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
