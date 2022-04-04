async def prepare_player_info(data):
    items = "пусто"
    if data["items"]:
        items = ""
        for item in data["items"]:
            items += f"{item}, "
    text = (
        f'Ігрове ім\'я: <i>{data["name"]}</i>\n🎖Рівень: <i>{data["level"]}</i>\n🌟Досвід: <i>{data["experience"]}</i>\n❤Здоров\'я: '
        f'<i>{data["health"]}</i>\nЕнергія: <i>{data["energy"]}</i>\n\n💪Сила: <i>{data["strength"]}</i>\n⚡Спритність: <i>{data["agility"]}</i>\n'
        f'🎯Інтуїція: <i>{data["intuition"]}</i>\n🎓Інтелект: <i>{data["intelligence"]}</i>\n💟Клас: <i>{data["hero_class"]}</i>\n\n'
        f'🤝Нація: <i>{data["nation"]}</i>\n💰Гроші: <i>{data["money"]}</i>\n🎒Речі: <i>{items}</i>\n'
        f'🐺Транспорт: <i>{data["mount"]["name"] if data["mount"] else "немає"}</i>\n'
        f'\nПоточне місце: <i>{data["current_state"]}</i>'
    )
    return text
