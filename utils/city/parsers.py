from typing import Tuple


def parse_purchase(text: str) -> Tuple[str, float]:
    text_list = text.split(" ")
    price = float(text_list[-1])
    item_list = text_list[1:-2]
    item = " ".join(item_list)
    return item, price


def parse_road_name(text: str) -> str:
    text_list = text.split("-")
    road_name = text_list[0].strip()
    return road_name
