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


async def show_roads(player_info: dict, message: types.Message):
    client = Client(DB_PASSWORD, 'Telegramia', 'roads')
    roads = client.get_all({'from_obj': player_info['current_state']})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for road in roads:
        markup.add(types.KeyboardButton(f'{road["from_obj"]}-{road["to_obj"]}'))
    markup.add(types.KeyboardButton('Назад'))
    await message.answer('Оберіть місце, куди хочете відправитись', reply_markup=markup)


async def create_markup_for_shop(items: list):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in items:
        markup.add(types.KeyboardButton(f'Купити {item["name"]} за {item["price"]}'))
    markup.add(types.KeyboardButton('Назад'))
    return markup


async def create_recover_markup(characteristic: str):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=f'Отримати 5 одиниць {characteristic} за 5 монет',
                                          callback_data=f'5{characteristic}5'))
    markup.add(types.InlineKeyboardButton(text=f'Отримати 15 одиниць {characteristic} за 13 монет',
                                          callback_data=f'10{characteristic}13'))
    markup.add(types.InlineKeyboardButton(text=f'Отримати 50 одиниць {characteristic} за 45 монет',
                                          callback_data=f'50{characteristic}45'))
    markup.add(types.InlineKeyboardButton(text='Назад',
                                          callback_data='back'))
    return markup


async def show_items(player_info: dict, message: types.Message):
    client = Client(DB_PASSWORD, 'Telegramia', 'items')
    items = client.get_all({'city': player_info['current_state']})
    markup = await create_markup_for_shop(items)
    await message.answer('Оберіть предмет, який хочете купити', reply_markup=markup)


async def show_horses(player_info: dict, message: types.Message):
    client = Client(DB_PASSWORD, 'Telegramia', 'horses')
    horses = client.get_all({'city': player_info['current_state']})
    markup = await create_markup_for_shop(horses)
    await message.answer('Оберіть предмет, який хочете купити', reply_markup=markup)


async def enter_academy(player_info: dict, message: types.Message):
    markup = await create_recover_markup('intelligence')
    await message.answer(f'Ви знаходитесь в академії міста {player_info["current_state"]}'
                         f' і у вас {player_info["intelligence"]} інтелекту. Ви хочете провести навчання в академії?',
                         reply_markup=markup)


async def enter_temple(player_info: dict, message: types.Message):
    markup = await create_recover_markup('health')
    await message.answer(f'Ви знаходитесь у храмі міста {player_info["current_state"]}'
                         f' і у вас {player_info["health"]} здоров\'я. Ви хочете відновити його?',
                         reply_markup=markup)


async def enter_tavern(player_info: dict, message: types.Message):
    markup = await create_recover_markup('energy')
    await message.answer(f'Ви знаходитесь у таверні міста {player_info["current_state"]}'
                         f' і у вас {player_info["energy"]} енергії. Ви хочете відновити її?',
                         reply_markup=markup)


city_objects = [
    {
        'name': 'market',
        'ukr_name': 'Ринок',
        'function': show_items
    },
    {
        'name': 'academy',
        'ukr_name': 'Академія',
        'function': enter_academy
    },
    {
        'name': 'temple',
        'ukr_name': 'Храм',
        'function': enter_temple
    },
    {
        'name': 'tavern',
        'ukr_name': 'Таверна',
        'function': enter_tavern
    },
    {
        'name': 'menagerie',
        'ukr_name': 'Стойло',
        'function': show_horses
    },
    {
        'name': 'roads',
        'ukr_name': 'Дороги',
        'function': show_roads
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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=3)
    buttons = []
    for city_object in city_objects:
        try:
            if city[city_object['name']]:
                buttons.append(types.KeyboardButton(city_object['ukr_name']))
        except KeyError:
            pass
    buttons.append(types.KeyboardButton('Дороги'))
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


@dp.message_handler(is_player=True, commands=['where'])
async def send_place_info(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    client = Client(DB_PASSWORD, 'Telegramia', 'players')
    city_name = client.get({'user_id': user_id})['current_state']
    await show_city_info(city_name, chat_id)


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
    await message.answer(country['description'])
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
    client = Client(DB_PASSWORD, 'Telegramia', 'players')
    user_id = message.from_user.id
    chat_id = message.chat.id
    player = client.get({'user_id': user_id})
    if message.text == 'Назад':
        await show_city_info(player['current_state'], chat_id)
        return
    for city_object in city_objects:
        if city_object['ukr_name'] == message.text:
            await city_object['function'](player, message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
