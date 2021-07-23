from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from database import Client
from config import DB_PASSWORD


class IsPlayer(BoundFilter):
    key = 'is_player'

    def __init__(self, is_player):
        self.is_player = is_player

    async def check(self, message: types.Message) -> bool:
        client = Client(DB_PASSWORD, 'Telegramia', 'players')
        user_id = message.from_user.id
        if client.get({'user_id': user_id}) is not None:
            return True
        return False
