from aiogram.utils.markdown import hitalic, hbold


async def prepare_player_info(data):
    items = "пусто"
    if data["items"]:
        items = ""
        for item in data["items"]:
            items += f"{item}, "
    text = (
        f'Ігрове ім\'я: {hbold(data["name"])}\n'
        f'🎖Рівень: {hitalic(data["level"])}\n'
        f'🌟Досвід: <i>{data["experience"]:2f}</i>\n'
        f'❤Здоров\'я: {hitalic(data["health"])}\n'
        f'Енергія: {hitalic(data["energy"])}\n\n'
        f'💪Сила: {hitalic(data["strength"])}\n'
        f'⚡Спритність: {hitalic(data["agility"])}\n'
        f'🎯Інтуїція: {hitalic(data["intuition"])}\n'
        f'🎓Інтелект: {hitalic(data["intelligence"])}\n'
        f'💟Клас: {hitalic(data["hero_class"])}\n\n'
        f'🤝Нація: {hitalic(data["nation"])}\n'
        f'💰Гроші: {hitalic(data["money"])}\n'
        f'🎒Речі: {hitalic(items)}\n'
        f'🐺Транспорт: {hitalic(data["mount"]["name"] if data["mount"] else "немає")}\n\n'
        f'Поточне місце: {hbold(data["current_state"])}'
    )
    return text
