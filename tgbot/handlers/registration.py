from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hitalic

from tgbot.models.database import Client
from tgbot.misc.system.info import prepare_player_info
from tgbot.keyboards.reply.general import create_markup, delete_markup
from tgbot.keyboards.inline.hero_choice import hero_choice_markup
from tgbot.states.states import Player
from loader import dp


@dp.message_handler(Command('create'), state="*")
async def create_player_handler(message: Message, player: dict) -> Message:
    if player is not None:
        return await message.reply("Ви вже зареєстровані")
    photo_url = (
        "https://raw.githubusercontent.com/mezgoodle/images/master/telegramia_intro.jpg"
    )
    text = (
        f"Вітаємо у магічному світі {hitalic('Telegramia')}. Цей світ повен пригод, цікавих людей, підступних ворогів, "
        "великих держав і ще багато чого іншого...Скоріше починай свою подорож. Для початку обери країну, "
        "у яку відправишся, щоб підкорювати цей світ"
    )
    markup = await create_markup("countries", "name", message)
    await Player.nation.set()
    await message.answer_photo(
        photo_url, text, reply_markup=markup
    )


@dp.message_handler(state=Player.nation)
async def answer_player_nation(message: Message, state: FSMContext) -> Message:
    nation = message.text
    user_id = message.from_user.id
    telegram_name = message.from_user.username
    client: Client = message.bot.get('client')
    country = client.get({"name": nation}, "countries")
    client.update({"name": country["name"]}, {"population": 1}, "countries", "$inc")
    await state.update_data({"nation": nation})
    await state.update_data({"user_id": user_id})
    await state.update_data({"telegram_name": telegram_name})
    await state.update_data({"level": 1.0})
    await state.update_data({"experience": 0.0})
    await state.update_data({"money": 100.0})
    await state.update_data({"items": []})
    await state.update_data({"mount": {}})
    await state.update_data({"health": 100.0})
    await state.update_data({"energy": 60.0})
    await state.update_data({"current_state": country["capital"]})
    await message.answer(country["description"])
    await Player.name.set()
    markup = await delete_markup()
    return await message.answer("Напиши, як тебе звати", reply_markup=markup)


@dp.message_handler(state=Player.name)
async def answer_player_name(message: Message, state: FSMContext) -> Message:
    name = message.text
    await state.update_data({"name": name})
    markup = await create_markup("classes", "name", message)
    await Player.hero_class.set()
    return await message.answer("Обери свій клас", reply_markup=markup)


@dp.message_handler(state=Player.hero_class)
async def answer_player_class(message: Message, state: FSMContext) -> Message:
    class_name = message.text
    await state.update_data({"hero_class": class_name})
    client: Client = message.bot.get('client')
    class_ = client.get({"name": class_name}, "classes")
    await state.update_data({"strength": class_["characteristics"]["strength"]})
    await state.update_data({"agility": class_["characteristics"]["agility"]})
    await state.update_data({"intuition": class_["characteristics"]["intuition"]})
    await state.update_data({"intelligence": class_["characteristics"]["intelligence"]})
    data = await state.get_data()
    await state.finish()
    text = await prepare_player_info(data)
    client.insert(data, "players")
    await message.answer(text)
    return await message.answer("Вас задовільняє ваш персонаж?", reply_markup=hero_choice_markup)
