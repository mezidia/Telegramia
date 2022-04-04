from aiogram.types import BotCommand


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Get the manual of the game"),
            BotCommand("where", "Show information about the place"),
            BotCommand("me", "Show information about the player"),
        ]
    )
