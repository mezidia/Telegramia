from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def show_start_text(message: types.Message) -> types.Message:
    text = "Вітаю у текстовій грі <b>Telegramia</b>. Створіть <i>свого героя</i> за допомогою команди /create. Дізнайтесь, як грати, через команду /help"
    return await message.answer(text)
