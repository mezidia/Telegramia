from aiogram.types import CallbackQuery

from tgbot.config import Config
from tgbot.models.database import Client
from tgbot.misc.system.checks import check_money, check_characteristics
from tgbot.misc.city.city import show_city_info


async def apply_recover(user_id: str, call: CallbackQuery, callback_data: str):
    client: Client = call.bot.get('client')
    _, value, characteristic, price = callback_data.split(":")

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
            player["current_state"], call.message
        )
    return await call.message.answer("У вас недостатньо грошей або ваш рівень замалий")
