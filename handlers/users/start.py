from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.misc.help import help_text
from keyboards.inline.help_information import create_markup


@dp.message_handler(CommandStart())
async def show_start_text(message: types.Message) -> types.Message:
    text = "Вітаю у текстовій грі <b>Telegramia</b>. Створіть <i>свого героя</i> за допомогою команди /create. Для того, щоб дізнатись, як грати, прочитайте інструкцію нище."
    await message.answer(text)
    return await message.answer(help_text[0], reply_markup=create_markup(0))
