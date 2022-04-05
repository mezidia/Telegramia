from aiogram import executor

import middlewares, handlers

from loader import dp, bot, storage
from utils.set_bot_commands import set_default_commands
# TODO: create map image
# TODO: change images sizes
# TODO: make async methods
# TODO: write in handlers custom filters

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
