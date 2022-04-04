from aiogram.types import Message

from handlers.users.help import show_help_text
from handlers.users.start import show_start_text
from handlers.users.registration import create_player_handler
from handlers.users.player import show_player_handler, send_place_info


async def handle_commands(message: Message, text: str):
    commands = {
        "/create": create_player_handler,
        "/where": send_place_info,
        "/me": show_player_handler,
        "/start": show_start_text,
        "/help": show_help_text,
    }
    return await commands[text](message)