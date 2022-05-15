from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, User, CallbackQuery
from aiogram import Bot

from tgbot.config import Config
from tgbot.models.database import Client


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: User):
        user_id = user.id
        bot = Bot.get_current()
        config: Config = bot.get('config')
        client = Client(config.db.password)
        player = client.get({'user_id': user_id}, 'players')
        data['player'] = player

    async def on_pre_process_message(self, message: Message, data: dict):
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, call: CallbackQuery, data: dict):
        await self.setup_chat(data, call.from_user)