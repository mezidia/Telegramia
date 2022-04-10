import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.filters.is_player import IsPlayer
from tgbot.handlers.errors import register_error
from tgbot.handlers.cancel import register_cancel
from tgbot.handlers.echo import register_echo
from tgbot.handlers.callbacks import register_callbacks
from tgbot.handlers.city import register_city_object
from tgbot.handlers.help import register_help_text
from tgbot.handlers.horse import register_answer_horse
from tgbot.handlers.item import register_item_answers
from tgbot.handlers.player import register_player
from tgbot.handlers.registration import register_registration
from tgbot.handlers.road import register_road
from tgbot.handlers.start import register_start
from tgbot.handlers.delete import register_delete_handler
from tgbot.services.setting_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    # TODO: set antispamm middleware
    pass


def register_all_filters(dp):
    dp.filters_factory.bind(IsPlayer)


def register_all_handlers(dp):
    handlers = [
        register_cancel,
        register_registration,
        register_start,
        register_help_text,
        register_delete_handler,
        register_road,
        register_answer_horse,
        register_player,
        register_item_answers,
        register_callbacks,
        register_city_object,
        register_echo,
        register_error,
    ]
    for handler in handlers:
        handler(dp)


async def set_all_default_commands(bot: Bot):
    await set_default_commands(bot)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config()

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    await set_default_commands(bot)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        # await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
