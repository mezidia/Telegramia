from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from keyboards.inline.help_information import create_markup
from utils.misc.help import help_text


@dp.message_handler(CommandHelp())
async def show_help_text(message: Message) -> Message:
    return await message.answer(help_text[0], reply_markup=create_markup(0))
