from aiogram.types import Message

from tgbot.handlers.help import show_help_text
from tgbot.handlers.start import show_start_text
from tgbot.handlers.registration import create_player_handler
from tgbot.handlers.player import show_player_handler, send_place_info
from tgbot.handlers.delete import delete_handler


async def handle_commands(message: Message, text: str):
    commands = {
        "/create": create_player_handler,
        "/where": send_place_info,
        "/me": show_player_handler,
        "/start": show_start_text,
        "/help": show_help_text,
        '/delete': delete_handler
    }
    return await commands[text](message)