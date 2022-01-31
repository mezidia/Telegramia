from typing import Tuple


def check_money(player: dict, price: float) -> bool:
    player_money = float(player['money'])
    return player_money - price > 0


def check_characteristics(player: dict, value: float, characteristic: str) -> bool:
    player_value = player[characteristic] + value
    return player_value <= player['level'] * 50


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
