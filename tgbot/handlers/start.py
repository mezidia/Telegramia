from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart

from tgbot.misc.system.help import help_text
from tgbot.keyboards.inline.help_information import create_markup
from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def show_start_text(message: Message) -> Message:
    text = "Вітаю у текстовій грі <b>Telegramia</b>. Створіть <i>свого героя</i> за допомогою команди /create. Для " \
           "того, щоб дізнатись, як грати, прочитайте інструкцію нище. "
    await message.answer(text)
    return await message.answer(help_text[0], reply_markup=create_markup(0))
