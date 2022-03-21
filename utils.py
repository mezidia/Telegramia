from database import Client

from typing import Tuple
from datetime import datetime, timedelta


def check_money(player: dict, price: float) -> bool:
    player_money = float(player['money'])
    return player_money - price > 0


def check_health(player: dict, damage: float) -> bool:
    player_health = player['health']
    return player_health - damage > 0


def check_characteristics(player: dict, value: float, characteristic: str) -> bool:
    player_value = player[characteristic] + value
    return player_value <= player['level'] * 50


def check_in_dungeon(player: dict, client: Client) -> bool:
    try:
        dungeon = client.get({'name': player['current_state']}, 'dungeons')
        dungeon_members = dungeon['members']
    except TypeError:
        return False
    if player['name'] in dungeon_members:
        start_date = dungeon_members[player['name']]
        now_date = datetime.now()
        delta = now_date - start_date
        dungeon_time = timedelta(seconds=dungeon['base_time'])
        return delta < dungeon_time
    return False


def check_in_raid(player: dict, client: Client) -> bool:
    try:
        raid = client.get({'name': player['current_state']}, 'raids')
        raid_members = raid['members']
    except TypeError:
        return False
    if player['name'] in raid_members:
        player_info = raid_members[player['name']]
        raid_level = client.get({'raid_name': raid['name'], 'level': player_info['level']}, 'raid_levels')
        start_date = player_info['time']
        now_date = datetime.now()
        delta = now_date - start_date
        dungeon_time = timedelta(seconds=raid_level['base_time'])
        return delta < dungeon_time
    return False


def check_energy(player: dict, energy_value: float, travel: bool = True) -> bool:
    """

    :param player:
    :param energy_value:
    :param travel: False, if it is a dungeon or raid invasion
    :return:
    """
    player_energy = player['energy']
    if travel and (mount := player['mount']):
        energy_value -= mount['bonus']
    return player_energy - energy_value >= 0


def parse_purchase(text: str) -> Tuple[str, float]:
    text_list = text.split(' ')
    price = float(text_list[-1])
    item_list = text_list[1:-2]
    item = ' '.join(item_list)
    return item, price


async def finish_state(state):
    try:
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
    except AttributeError:
        pass
