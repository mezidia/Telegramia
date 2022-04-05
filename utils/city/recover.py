from aiogram.types import CallbackQuery

from utils.db_api.database import Client
from utils.city.checks import check_money, check_characteristics
from utils.city.info import show_city_info
from data.config import DB_PASSWORD


async def apply_recover(user_id: str, call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)

    client = Client(DB_PASSWORD)
    value = callback_data.get("quantity")
    price = callback_data.get("price")
    characteristic = callback_data.get("characteristic")

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
        await call.message.answer(
            f"Покупка здійснена! Ви збільшили {characteristic} на {value} одиниць"
        )
        return await show_city_info(
            player["current_state"], user_id
        )
    return await call.message.answer("У вас недостатньо грошей або ваш рівень замалий")
