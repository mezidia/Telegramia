from aiogram.types import Message

from utils.db_api.database import Client
from utils.misc.state import finish_state
from keyboards.default import dungeon as dungeon_markup, raid as raid_markup, city as city_markup
from data.config import DB_PASSWORD
from states.city import CityObject
from loader import bot


async def show_city_info(city_name: str, chat_id: str, state=None) -> Message:
    client = Client(DB_PASSWORD)
    await finish_state(state)
    markup: object
    photo_url = ""
    if dungeon := client.get({"name": city_name}, "dungeons"):
        markup = dungeon_markup.create_markup()
        photo_url = f'https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{dungeon["name"]}.jpg'
    elif raid := client.get({"name": city_name}, "raids"):
        markup = raid_markup.create_markup()
        photo_url = f"https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{raid['name']}.jpg"
    else:
        photo_url = f"https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{city_name}.jpg"
        city = client.get({"name": city_name}, "cities")
        markup = city_markup.create_markup(city)
    # photo_url = 'https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_Брісвель.jpg'
    await CityObject.first()
    return await bot.send_photo(
        chat_id, photo_url, f"Ви знаходитесь у місті {city_name}", reply_markup=markup
    )
