from typing import Tuple
from math import modf

from tgbot.models.database import Client


def apply_items(player_info: dict, client: Client) -> dict:
    player_chars = {
        "strength": player_info["strength"],
        "agility": player_info["agility"],
        "intuition": player_info["intuition"],
        "intelligence": player_info["intelligence"],
    }
    for item in player_info["items"]:
        shop_item = client.get({"name": item}, "items")
        char = shop_item["characteristic"]
        player_chars[char] += shop_item["bonus"]
    return player_chars


def level_up(exp: float) -> Tuple[float, float]:
    if exp > 100:
        exp /= 100
        return modf(exp)
    return exp, 0
