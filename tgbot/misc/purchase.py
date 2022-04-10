from typing import NoReturn, Union

from tgbot.models.database import Client


def do_purchase(client: Client, player, items, price) -> NoReturn:
    client.update(
        {"user_id": player["user_id"]},
        {
            "items": items,
            "money": player["money"] - price,
        },
        "players",
    )


def smart_purchase(item_name: str, items: list, client: Client) -> Union[dict, bool]:
    item_in_shop = client.get({"name": item_name}, "items")
    type_items = client.get_all("items", {"type": item_in_shop["type"]})
    for item in type_items:
        if item["name"] in items:
            if item_in_shop["bonus"] > item["bonus"]:
                return item
    return False
