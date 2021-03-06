from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.utils.markdown import hbold

from tgbot.models.database import Client
from tgbot.misc.system.finish_state import finish_state
from tgbot.keyboards.reply.city import create_markup as city_markup
from tgbot.keyboards.reply.dungeon import create_markup as dungeon_markup
from tgbot.keyboards.reply.raid import create_markup as raid_markup
from tgbot.states.states import CityObject


async def show_city_info(city_name: str, message: Message, state=None) -> Message:
    client: Client = message.bot.get('client')
    await finish_state(state)
    markup: ReplyKeyboardMarkup
    photo_url = ""
    if dungeon := client.get({"name": city_name}, "dungeons"):
        markup = dungeon_markup()
        photo_url = f'https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{dungeon["name"]}.jpg'
    elif raid := client.get({"name": city_name}, "raids"):
        markup = raid_markup()
        photo_url = f"https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{raid['name']}.jpg"
    else:
        photo_url = f"https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_{city_name}.jpg"
        city = client.get({"name": city_name}, "cities")
        markup = city_markup(city)
    # photo_url = 'https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_Брісвель.jpg'
    await CityObject.first()
    return await message.answer_photo(
        photo_url, f"Ви знаходитесь у місті {hbold(city_name)}", reply_markup=markup
    )
