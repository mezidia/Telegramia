from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from utils.db_api.database import Client
from data.config import DB_PASSWORD


class IsPlayer(BoundFilter):
    key = 'is_player'

    def __init__(self, is_player: bool):
        self.is_player = is_player
    
    async def check(self, message: Message) -> bool:
        client = Client(DB_PASSWORD)
        user_id = message.from_user.id
        if client.get({'user_id': user_id}, 'players') is not None:
            return True
        return False
