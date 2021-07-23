import logging

from aiogram import Bot, Dispatcher, executor, types

from config import TELEGRAM_TOKEN, DB_PASSWORD
from filters import IsPlayer
from database import Client

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


@dp.message_handler(commands=['create'])
async def create_player_handler(message: types.Message):
    photo_url = 'https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_intro.jpg'
    text = 'Вітаємо у магічному світі *Telegramia*. Цей світ повен пригод, цікавих людей, підступних ворогів, ' \
           'великих держав і ще багато чого іншого...Скоріше починай свою подорож. Для початку обери країну, ' \
           'у яку відправишся, щоб підкорювати цей світ'
    client = Client(DB_PASSWORD, 'Telegramia', 'countries')
    countries = client.get_all()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for country in countries:
        btn = types.KeyboardButton(country['name'])
        buttons.append(btn)
    markup.add(*buttons)
    await message.answer_photo(photo_url, text, parse_mode='Markdown', reply_markup=markup)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
