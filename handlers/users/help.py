from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from keyboards.inline.help_information import help_markup


@dp.message_handler(CommandHelp())
async def show_help_text(message: Message) -> Message:
    return await message.answer("Уся інструкція доступна на сайті", reply_markup=help_markup)
