from .is_player import IsPlayer
from loader import dp


if __name__ == '__main__':
    dp.filters_factory.bind(IsPlayer, event_handlers=[dp.message_handlers])
