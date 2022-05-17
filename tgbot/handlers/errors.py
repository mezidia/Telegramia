from aiogram.utils.exceptions import (TelegramAPIError,
                                      MessageNotModified,
                                      CantParseEntities)
from aiogram import Dispatcher

import logging


async def errors_handler(update, exception):
    if isinstance(exception, MessageNotModified):
        logging.exception('Message is not modified')
        return True

    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    # must be the last
    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    logging.exception(f'Update: {update} \n{exception}')


def register_error(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
