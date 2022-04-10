from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from tgbot.models.database import Client
from tgbot.config import Config

from typing import Optional


class IsPlayer(BoundFilter):
    key = 'is_player'

    def __init__(self, is_player: Optional[bool] = None):
        self.is_player = is_player
    
    async def check(self, message: Message) -> bool:
        config: Config = message.bot.get('config')
        client = Client(config.db.password)
        user_id = message.from_user.id
        if client.get({'user_id': user_id}, 'players') is not None:
            return True
        return False

