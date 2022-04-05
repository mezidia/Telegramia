from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import buy_callback


def create_markup(characteristic: str):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text=f"Отримати 5 одиниць {characteristic} за 5 монет",
            callback_data=buy_callback.new(quantity=5, characteristic=characteristic, price=5),
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=f"Отримати 15 одиниць {characteristic} за 13 монет",
            callback_data=buy_callback.new(quantity=15, characteristic=characteristic, price=13),
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=f"Отримати 50 одиниць {characteristic} за 45 монет",
            callback_data=buy_callback.new(quantity=50, characteristic=characteristic, price=45),
        )
    )
    return markup
