import logging

from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp

from tgbot.keyboards.inline.help_information import help_markup
from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def show_help_text(message: Message) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    return await message.answer("Уся інструкція доступна на сайті", reply_markup=help_markup)
