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

city_objects = [
    {
        'name': 'market',
        'ukr_name': 'Ринок'
    },
    {
        'name': 'academy',
        'ukr_name': 'Ринок'
    },
    {
        'name': 'temple',
        'ukr_name': 'Храм'
    },
    {
        'name': 'tavern',
        'ukr_name': 'Таверна'
    },
    {
        'name': 'menagerie',
        'ukr_name': 'Стойло'
    },
]


# States
class Player(StatesGroup):
    user_id = State()
    telegram_name = State()
    name = State()
    level = State()
    experience = State()
    health = State()
    energy = State()
    strength = State()
    agility = State()
    intuition = State()
    intelligence = State()
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


async def prepare_player_info(data):
    items = 'пусто'
    if data['items']:
        items = ''
        for item in data['items']:
            items += f'{item}, '
    text = f'Ігрове ім\'я: *{data["name"]}*\n🎖Рівень: *{data["level"]}*\n🌟Досвід: *{data["experience"]}*\n❤Здоров\'я: ' \
           f'*{data["health"]}*\nЕнергія: *{data["energy"]}*\n\n💪Сила: *{data["strength"]}*\n⚡Спритність: *{data["agility"]}*\n' \
           f'🎯Інтуїція: *{data["intuition"]}*\n🎓Інтелект: *{data["intelligence"]}*\n💟Клас: *{data["hero_class"]}*\n\n' \
           f'🤝Нація: *{data["nation"]}*\n💰Гроші: *{data["money"]}*\n🎒Речі: *{items}*\n' \
           f'🐺Транспорт: *{data["mount"]["name"] if data["mount"]["name"] else "немає"}*\n' \
           f'\nПоточне місце: *{data["current_state"]}*'
    return text


async def show_city_info(city_name: str, chat_id: str):
    photo_url = f'https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{city_name}.jpg'
    client = Client(DB_PASSWORD, 'Telegramia', 'cities')
    city = client.get({'name': city_name})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    buttons = []
    for city_object in city_objects:
        if city[city_object['name']]:
            buttons.append(types.KeyboardButton(city_object['ukr_name']))
    markup.add(*buttons)
    await bot.send_photo(chat_id, photo_url, f'Ви знаходитесь у місті {city_name}', reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    client = Client(DB_PASSWORD, 'Telegramia', 'players')
    if callback_query.data == 'No':
        client.delete({'user_id': user_id})
        await Player.nation.set()
        markup = await create_keyboard('countries', 'name')
        return await bot.send_message(callback_query.from_user.id, 'Оберіть країну', reply_markup=markup)
    else:
        city_name = client.get({'user_id': user_id})['current_state']
        await show_city_info(city_name, callback_query.from_user.id)


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
    client = Client(DB_PASSWORD, 'Telegramia', 'players')
    user_id = message.from_user.id
    if client.get({'user_id': user_id}) is not None:
        return await message.reply('Ви вже зареєстровані')
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
    telegram_name = message.from_user.username
    client = Client(DB_PASSWORD, 'Telegramia', 'countries')
    country = client.get({'name': nation})
    await state.update_data({'nation': nation})
    await state.update_data({'user_id': user_id})
    await state.update_data({'telegram_name': telegram_name})
    await state.update_data({'level': 1.})
    await state.update_data({'experience': 0.})
    await state.update_data({'money': 100.})
    await state.update_data({'items': []})
    await state.update_data({'mount': {'name': ''}})
    await state.update_data({'health': 100.})
    await state.update_data({'energy': 60.})
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


@dp.message_handler(state=Player.hero_class)
async def answer_repo_name_issue(message: types.Message, state: FSMContext) -> types.Message:
    class_name = message.text
    await state.update_data({'hero_class': class_name})
    client = Client(DB_PASSWORD, 'Telegramia', 'classes')
    class_ = client.get({'name': class_name})
    await state.update_data({'strength': class_['characteristics']['strength']})
    await state.update_data({'agility': class_['characteristics']['agility']})
    await state.update_data({'intuition': class_['characteristics']['intuition']})
    await state.update_data({'intelligence': class_['characteristics']['intelligence']})
    data = await state.get_data()
    await state.finish()
    text = await prepare_player_info(data)
    client = Client(DB_PASSWORD, 'Telegramia', 'players')
    client.insert(data)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('Так', callback_data='Yes'),
               types.InlineKeyboardButton('Ні', callback_data='No'))
    await message.answer(text, parse_mode='Markdown')
    return await message.answer('Вас задовільняє ваш персонаж?', reply_markup=markup)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
