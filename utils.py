def check_money(player: dict, price: float) -> bool:
    player_money = float(player['money'])
    return player_money - price > 0


def check_characteristics(player: dict, value: float, characteristic: str) -> bool:
    player_value = player[characteristic] + value
    return player_value <= player['level'] * 50
