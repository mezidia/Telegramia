import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config import TELEGRAM_TOKEN, DB_PASSWORD
from filters import IsPlayer
from database import Client

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Activate filters
dp.filters_factory.bind(IsPlayer, event_handlers=[dp.message_handlers])


# States
class Player(StatesGroup):
    user_id = State()
    name = State()
    level = State()
    experience = State()
    health = State()
    mana = State()
    strength = State()
    agility = State()
    intuition = State()
    hero_class = State()
    nation = State()
    money = State()
    items = State()
    mount = State()
    current_state = State()


async def create_keyboard(collection_name: str, field_name: str):
    client = Client(DB_PASSWORD, 'Telegramia', collection_name)
    objects = client.get_all()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for object_ in objects:
        btn = types.KeyboardButton(object_[field_name])
        buttons.append(btn)
    markup.add(*buttons)
    return markup


# Use state '*' if I need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext) -> types.Message:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return await message.reply('Процес реєстрації не починався.')
    await state.finish()
    return await message.reply('Реєстрація зупинена.')


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
    markup = await create_keyboard('countries', 'name')
    await Player.nation.set()
    await message.answer_photo(photo_url, text, parse_mode='Markdown', reply_markup=markup)


@dp.message_handler(state=Player.nation)
async def answer_repo_name_issue(message: types.Message, state: FSMContext) -> types.Message:
    nation = message.text
    user_id = message.from_user.id
    client = Client(DB_PASSWORD, 'Telegramia', 'countries')
    country = client.get({'name': nation})
    await state.update_data({'nation': nation})
    await state.update_data({'user_id': user_id})
    await state.update_data({'level': 1.})
    await state.update_data({'experience': 0.})
    await state.update_data({'money': 100.})
    await state.update_data({'items': []})
    await state.update_data({'mount': {}})
    await state.update_data({'current_state': country['capital']})
    await Player.name.set()
    return await message.answer('Напиши, як тебе звати')


@dp.message_handler(state=Player.name)
async def answer_repo_name_issue(message: types.Message, state: FSMContext) -> types.Message:
    name = message.text
    await state.update_data({'name': name})
    markup = await create_keyboard('classes', 'name')
    await Player.hero_class.set()
    return await message.answer('Обери свій клас', reply_markup=markup)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
