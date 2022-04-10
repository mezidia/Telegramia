from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot) -> None:
    STARTING_COMMANDS = {
        'en': [
            BotCommand(command='start', description='Start the bot'),
            BotCommand(command='help', description='Show help'),
            BotCommand(command='create', description='Create a new account'),
            BotCommand(command='delete', description='Delete an account'),
            BotCommand(command='me', description='Show your account information'),
            BotCommand(command='where', description='Show your location'),
        ],
        'uk': [
            BotCommand(command='start', description='Початок роботи'),
            BotCommand(command='help', description='Допомога'),
            BotCommand(command='create', description='Створення акаунту'),
            BotCommand(command='delete', description='Видалення акаунту'),
            BotCommand(command='me', description='Інформація про героя'),
            BotCommand(command='where', description='Показати місцезнаходження героя'),
        ],
    }
    for language_code, commands in STARTING_COMMANDS.items():
        await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault(), language_code=language_code)
