from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils.db_api.database import Client
from data.config import DB_PASSWORD


@dataclass
class IsPlayer(BoundFilter):
    key = 'is_player'
    is_player: bool
    
    async def check(self, message: types.Message) -> bool:
        client = Client(DB_PASSWORD)
        user_id = message.from_user.id
        if client.get({'user_id': user_id}, 'players') is not None:
            return True
        return False
