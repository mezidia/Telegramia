from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

hero_choice_markup = InlineKeyboardMarkup(row_width=2)
hero_choice_markup.add(
    InlineKeyboardButton("Так", callback_data="Yes"),
    InlineKeyboardButton("Ні", callback_data="No"),
)
