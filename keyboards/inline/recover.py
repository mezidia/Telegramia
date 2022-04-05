from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_markup(characteristic: str):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text=f"Отримати 5 одиниць {characteristic} за 5 монет",
            callback_data=f"5{characteristic}5",
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=f"Отримати 15 одиниць {characteristic} за 13 монет",
            callback_data=f"15{characteristic}13",
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=f"Отримати 50 одиниць {characteristic} за 45 монет",
            callback_data=f"50{characteristic}45",
        )
    )
    return markup
