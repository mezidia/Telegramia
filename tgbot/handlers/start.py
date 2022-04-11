from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart

from tgbot.misc.help import help_text
from tgbot.keyboards.inline.help_information import create_markup


async def show_start_text(message: types.Message) -> types.Message:
    text = "Вітаю у текстовій грі <b>Telegramia</b>. Створіть <i>свого героя</i> за допомогою команди /create. Для " \
           "того, щоб дізнатись, як грати, прочитайте інструкцію нище. "
    await message.answer(text)
    return await message.answer(help_text[0], reply_markup=create_markup(0))


def register_start(dp: Dispatcher):
    dp.register_message_handler(show_start_text, CommandStart(), state="*")
