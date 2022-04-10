from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp

from tgbot.keyboards.inline.help_information import help_markup


async def show_help_text(message: Message) -> Message:
    return await message.answer("Уся інструкція доступна на сайті", reply_markup=help_markup)


def register_help_text(dp: Dispatcher):
    dp.register_message_handler(show_help_text, CommandHelp())
