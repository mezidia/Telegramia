import logging

from aiogram import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp


@dp.message_handler(commands="cancel", state="*")
async def cancel_handler(message: Message, state: FSMContext) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return await message.reply("Процес реєстрації не починався.")
    await state.finish()
    return await message.reply("Реєстрація зупинена.", reply_markup=ReplyKeyboardRemove())
