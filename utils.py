from typing import Tuple


def check_money(player: dict, price: float) -> bool:
    player_money = float(player['money'])
    return player_money - price > 0


def check_characteristics(player: dict, value: float, characteristic: str) -> bool:
    player_value = player[characteristic] + value
    return player_value <= player['level'] * 50


def parse_purchase(text: str) -> Tuple[str, float]:
    text_list = text.split(' ')
    price = float(text_list[-1])
    item_list = text_list[1:-2]
    item = ' '.join(item_list)
    return item, price

