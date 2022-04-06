from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import help_callback
from utils.misc.help import help_text


def create_markup(current_page: int):
    markup = InlineKeyboardMarkup(row_width=3)
    if (current_page - 1) in help_text:
        markup.insert(
            InlineKeyboardButton(
                text="Назад ⬅️",
                callback_data=help_callback.new(method="previous", page=current_page-1),
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text="Закрити ❌",
            callback_data="close",
        )
    )
    if (current_page + 1) in help_text:
        markup.insert(
            InlineKeyboardButton(
                text="Далі ➡️",
                callback_data=help_callback.new(method="next", page=current_page+1),
            )
        )
    return markup
