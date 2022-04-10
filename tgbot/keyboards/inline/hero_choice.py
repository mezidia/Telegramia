from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.inline.callback_datas import hero_callback

hero_choice_markup = InlineKeyboardMarkup(row_width=2)
hero_choice_markup.add(
    InlineKeyboardButton("Так", callback_data=hero_callback.new(choice="yes")),
    InlineKeyboardButton("Ні", callback_data=hero_callback.new(choice="no")),
)
