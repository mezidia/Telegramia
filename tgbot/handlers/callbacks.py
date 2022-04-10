from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.models.database import Client
from tgbot.misc.city import show_city_info
from tgbot.misc.recover import apply_recover
from tgbot.misc.help import help_text
from tgbot.misc.characterstics import characteristics
from tgbot.states.states import Player
from tgbot.config import Config
from tgbot.keyboards.reply.general import create_markup
from tgbot.keyboards.inline.help_information import create_markup as create_help_markup
from tgbot.keyboards.inline.callback_datas import hero_callback, buy_callback


async def recover_callback(call: CallbackQuery):
    user_id = call.from_user.id
    await call.answer()
    await apply_recover(user_id, call, call.data)


async def accept_registration(call: CallbackQuery):
    await call.answer("Вітаємо, вас зареєстровано!", show_alert=True, cache_time=60)
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    config: Config = call.bot.get('config')
    client = Client(config.db.password)
    player = client.get({"user_id": user_id}, "players")
    client.update({"name": player["hero_class"]}, {"choices": 1}, "classes", "$inc")
    return await show_city_info(
        player["current_state"], call.message
    )


async def reject_registration(call: CallbackQuery):
    await call.answer("Процес реєстрації почнеться знову", show_alert=True, cache_time=60)
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    config: Config = call.bot.get('config')
    client = Client(config.db.password)
    client.delete({"user_id": user_id}, "players")
    await Player.nation.set()
    markup = await create_markup("countries", "name", call.message)
    return await call.message.answer("Оберіть країну", reply_markup=markup)


async def manual_page_callback(call: CallbackQuery):
    await call.answer()
    page = int(call.data.split(":")[-1])
    return await call.message.edit_text(help_text[page], reply_markup=create_help_markup(page))


async def close_manual_page(call: CallbackQuery):
    await call.answer()
    await call.message.delete()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(recover_callback, buy_callback.filter(characteristic=characteristics))
    dp.register_callback_query_handler(accept_registration, hero_callback.filter(choice="yes"))
    dp.register_callback_query_handler(reject_registration, hero_callback.filter(choice="no"))
    dp.register_callback_query_handler(manual_page_callback, text_contains="read")
    dp.register_callback_query_handler(close_manual_page, text="close")
