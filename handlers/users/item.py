from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from states.item import Item
from loader import dp
from handlers.users.echo import echo
from utils.db_api.database import Client
from data.config import DB_PASSWORD
from utils.city.purchase import smart_purchase, do_purchase
from utils.city.checks import check_money
from utils.city.parsers import parse_purchase
from utils.misc import commands
from utils.city.info import show_city_info

# Show items by types


@dp.message_handler(state=Item.item)
async def answer_item_purchase(message: Message, state: FSMContext):
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
        return await commands.handle_commands(message, text)
