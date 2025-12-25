import json
from typing import List
from dataclasses import dataclass

@dataclass
class Venue:
    """
    Модель заведения для отображения в диалогах.

    Хранит основные данные о заведении и предоставляет методы
    для человекочитаемого представления и форматирования карточки.
    """
    name: str
    cuisine: str
    why_visit: str
    address_hint: str = "Район не указан"  # значение по умолчанию

    def __str__(self):
        return f"{self.name} ({self.cuisine}) — {self.why_visit}"

    def format_card(self) -> str:
        why = self.why_visit[:177] + "..." if len(self.why_visit) > 180 else self.why_visit
        return (
            f"<b>{self.name}</b>\n"
            f"<i>{self.cuisine}</i>\n"
            f"💡 {why}\n"
            f"📍 <i>{self.address_hint}</i>"
        )

async def parse_ai_response(data: dict) -> List[Venue]:
    """
    Разбирает уже распарсенный JSON-ответ от AI и преобразует его в список объектов Venue.
    В случае любой ошибки возвращает пустой список.
    :param data: dict из response.json()
    :return: список объектов Venue
    """
    try:
        venues_data = data.get("venues", [])

        if not isinstance(venues_data, list):
            print(f"[DEBUG] venues не список: {type(venues_data)}")  # Временно для лога
            return []

        venues = []

        for v in venues_data:
            if isinstance(v, dict):
                try:
                    venue = Venue(**v)
                    venues.append(venue)
                except Exception as e:
                    print(f"[DEBUG] Ошибка создания Venue из {v}: {e}")
                    continue
            else:
                print(f"[DEBUG] Элемент не dict: {v}")

        print(f"[DEBUG] Успешно спарсено {len(venues)} заведений")  # Увидишь в консоли
        return venues

    except Exception as e:
        print(f"[DEBUG] Критическая ошибка в парсере: {e}")
        return []