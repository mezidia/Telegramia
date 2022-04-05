from aiogram.types import CallbackQuery

from loader import dp, bot
from utils.db_api.database import Client
from utils.city.info import show_city_info
from utils.characteristics.characterstics import characteristics
from utils.city.recover import apply_recover
from data.config import DB_PASSWORD
from states.player import Player
from keyboards.default.general import create_markup
from keyboards.inline.callback_datas import buy_callback


@dp.callback_query_handler(buy_callback.filter(characteristic="energy"))
async def increase_energy(call: CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    await apply_recover(user_id, call, callback_data)
    

@dp.callback_query_handler(buy_callback.filter(characteristic="health"))
async def increase_health(call: CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    await apply_recover(user_id, call, callback_data)


@dp.callback_query_handler(buy_callback.filter(characteristic="intelligence"))
async def increase_intelligence(call: CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    await apply_recover(user_id, call, callback_data)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    client = Client(DB_PASSWORD)
    callback_data = callback_query.data
    if callback_data == "No":
        client.delete({"user_id": user_id}, "players")
        await Player.nation.set()
        markup = await create_markup("countries", "name")
        return await bot.send_message(
            callback_query.from_user.id, "Оберіть країну", reply_markup=markup
        )
    else:
        player = client.get({"user_id": user_id}, "players")
        client.update({"name": player["hero_class"]}, {"choices": 1}, "classes", "$inc")
        return await show_city_info(
            player["current_state"], callback_query.from_user.id
        )
