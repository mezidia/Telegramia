from aiogram import types

from database import Client
from config import DB_PASSWORD
from states import Item, Road, Horse


async def show_roads(player_info: dict, message: types.Message):
    client = Client(DB_PASSWORD)
    roads = client.get_all('roads', {'from_obj': player_info['current_state']})
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for road in roads:
        markup.add(types.KeyboardButton(f'{road["name"]}'))
    markup.add(types.KeyboardButton('Назад'))
    await Road.first()
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
                                          callback_data=f'15{characteristic}13'))
    markup.add(types.InlineKeyboardButton(text=f'Отримати 50 одиниць {characteristic} за 45 монет',
                                          callback_data=f'50{characteristic}45'))
    markup.add(types.InlineKeyboardButton(text='Назад',
                                          callback_data='back'))
    return markup


async def show_items(player_info: dict, message: types.Message):
    client = Client(DB_PASSWORD)
    items = client.get_all('items', {'city': player_info['current_state']})
    markup = await create_markup_for_shop(items)
    await Item.first()
    return await message.answer('Оберіть предмет, який хочете купити', reply_markup=markup)


async def show_horses(player_info: dict, message: types.Message):
    client = Client(DB_PASSWORD)
    horses = client.get_all('horses', {'city': player_info['current_state']})
    markup = await create_markup_for_shop(horses)
    await Horse.first()
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


async def show_dungeon(player_info: dict, message: types.Message):
    client = Client(DB_PASSWORD)
    dungeon = client.get({'name': player_info['current_state']}, 'dungeons')
    text = f'🌇Підземелля - {dungeon["name"]}\n\n📖{dungeon["description"]}\n\n' \
           f'Буде отримано шкоди - {dungeon["damage"]}\n\n' \
           f'💵Буде отримано нагороди - {dungeon["treasure"]}'
    await message.answer(text)


async def enter_dungeon(player_info: dict, message: types.Message):
    # TODO: do here logic
    await message.answer(f'Hello {player_info["name"]}')
