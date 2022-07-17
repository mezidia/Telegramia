from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.markdown import hbold, hitalic

from tgbot.misc.system.help import help_text
from tgbot.keyboards.inline.help_information import create_markup
from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def show_start_text(message: Message) -> Message:
    text = f"Вітаю у текстовій грі {hbold('Telegramia')}. Створіть {hitalic('свого героя')} за допомогою команди" \
           f" /create. Для " \
           "того, щоб дізнатись, як грати, прочитайте інструкцію нище. "
    await message.answer(text)
    return await message.answer(help_text[0], reply_markup=create_markup(0))
