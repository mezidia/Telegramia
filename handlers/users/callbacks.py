from aiogram.types import CallbackQuery

from loader import dp
from utils.db_api.database import Client
from utils.city.info import show_city_info
from utils.city.recover import apply_recover
from data.config import DB_PASSWORD
from states.player import Player
from keyboards.default.general import create_markup
from keyboards.inline.callback_datas import hero_callback


@dp.callback_query_handler(text_contains="recover")
async def recover_callback(call: CallbackQuery):
    user_id = call.from_user.id
    await apply_recover(user_id, call, call.data)


@dp.callback_query_handler(hero_callback.filter(choice="yes"))
async def accept_registration(call: CallbackQuery):
    await call.answer("Вітаємо, вас зареєстровано!", show_alert=True, cache_time=60)
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    client = Client(DB_PASSWORD)
    player = client.get({"user_id": user_id}, "players")
    client.update({"name": player["hero_class"]}, {"choices": 1}, "classes", "$inc")
    return await show_city_info(
        player["current_state"], call.from_user.id
    )


@dp.callback_query_handler(hero_callback.filter(choice="no"))
async def reject_registration(call: CallbackQuery):
    await call.answer("Процес реєстрації почнеться знову", show_alert=True, cache_time=60)
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    client = Client(DB_PASSWORD)
    client.delete({"user_id": user_id}, "players")
    await Player.nation.set()
    markup = await create_markup("countries", "name")
    return await call.message.answer("Оберіть країну", reply_markup=markup)
