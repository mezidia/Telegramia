from aiogram.types import CallbackQuery

from loader import dp, bot
from utils.db_api.database import Client
from utils.city.checks import check_money, check_characteristics
from utils.city.info import show_city_info
from utils.characteristics.characterstics import characteristics
from data.config import DB_PASSWORD
from states.player import Player
from keyboards.default.general import create_markup

@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: CallbackQuery):
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
