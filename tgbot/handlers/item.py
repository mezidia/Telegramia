import logging

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from tgbot.states.states import Item
from tgbot.handlers.echo import echo
from tgbot.models.database import Client
from tgbot.misc.purchase import smart_purchase, do_purchase
from tgbot.misc.checks import check_money
from tgbot.misc.parsers import parse_purchase
from tgbot.misc.city_objects import show_item_types, show_items
from tgbot.misc.commands import handle_commands
from tgbot.misc.city import show_city_info
from tgbot.config import Config
from tgbot.misc.types import types
from loader import dp


@dp.message_handler(state=Item.type)
async def answer_item_type(message: Message, state: FSMContext):
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    text = message.text
    if text == "Назад":
        return await echo(message, state)
    try:
        type_ = types[text]
    except KeyError:
        await message.answer("Невірний тип предмету")
        return await show_item_types({}, message)
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
    user_id = message.from_user.id
    player = client.get({"user_id": user_id}, "players")
    return await show_items(player, message, type_)


@dp.message_handler(state=Item.item)
async def answer_item_purchase(message: Message, state: FSMContext):
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    text = message.text
    if text == "Назад":
        return await echo(message, state)
    config: Config = message.bot.get('config')
    client = Client(config.db.password)
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
    return await show_city_info(player["current_state"], message, state)
