from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.builtin import Text

from loader import dp


# Use state '*' if I need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: Message, state: FSMContext) -> Message:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return await message.reply("Процес реєстрації не починався.")
    await state.finish()
    return await message.reply("Реєстрація зупинена.", reply_markup=ReplyKeyboardRemove())
