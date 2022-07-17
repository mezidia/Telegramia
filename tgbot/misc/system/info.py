from aiogram.utils.markdown import hitalic


async def prepare_player_info(data):
    items = "пусто"
    if data["items"]:
        items = ""
        for item in data["items"]:
            items += f"{item}, "
    text = (
        f'Ігрове ім\'я: {hitalic(data["name"])}\n🎖Рівень: {hitalic(data["level"])}\n🌟Досвід: {hitalic(data["experience"])}\n❤Здоров\'я: '
        f'{hitalic(data["health"])}\nЕнергія: {hitalic(data["energy"])}\n\n💪Сила: {hitalic(data["strength"])}\n⚡Спритність: {hitalic(data["agility"])}\n'
        f'🎯Інтуїція: {hitalic(data["intuition"])}\n🎓Інтелект: {hitalic(data["intelligence"])}\n💟Клас: {hitalic(data["hero_class"])}\n\n'
        f'🤝Нація: {hitalic(data["nation"])}\n💰Гроші: {hitalic(data["money"])}\n🎒Речі: {hitalic(items)}\n'
        f'🐺Транспорт: {hitalic(data["mount"]["name"] if data["mount"] else "немає")}\n'
        f'\nПоточне місце: {hitalic(data["current_state"])}'
    )
    return text
