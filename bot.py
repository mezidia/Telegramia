import logging

from aiogram import Bot, Dispatcher, executor, types

from config import TELEGRAM_TOKEN
from filters import IsPlayer

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Activate filters
dp.filters_factory.bind(IsPlayer, event_handlers=[dp.message_handlers])


@dp.message_handler(is_player=True, commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
