# --- ДИАЛОГ ПРОСМОТРА ЗАВЕДЕНИЙ ---
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const, Format

from locales import Lexicon
from states.setup_state import Processing
from utils.ai_responce_parser import Venue

# --- ОБРАБОТЧИКИ КНОПОК ---
async def on_next(callback: CallbackQuery, button: Button, manager: DialogManager):
    venues = manager.dialog_data.get("venues", [])

    if not venues:
        return

    current_index = manager.dialog_data.get("current_index", 0)
    # КРУГОВОЕ ДВИЖЕНИЕ(находится остаток от деления нашего индекса на количество элементов)
    new_index = (current_index + 1) % len(venues)

    manager.dialog_data["current_index"] = new_index

async def on_prev(callback: CallbackQuery, button: Button, manager: DialogManager):
    venues = manager.dialog_data.get("venues", [])

    if not venues:
        return

    # КРУГОВОЕ ДВИЖЕНИЕ(находится остаток от деления нашего индекса на количество элементов)
    current_index = manager.dialog_data.get("current_index", 0)
    new_index = (current_index - 1) % len(venues)

    manager.dialog_data["current_index"] = new_index

async def get_venue_data(dialog_manager: DialogManager, **kwargs):
    """
    Формирует данные для отображения карточки заведения в диалоге.

    - Инициализирует список заведений и текущий индекс при первом вызове
    - Возвращает текст карточки, счётчик прогресса и флаг наличия данных
    - Зацикливает навигацию по списку заведений

    :param dialog_manager: менеджер состояния диалога
    :return: словарь с данными для окна диалога
    """
    # Инициализация данных диалога при первом входе
    if "venues" not in dialog_manager.dialog_data:
        start_venues = dialog_manager.start_data.get("venues", [])
        dialog_manager.dialog_data["venues"] = start_venues
        dialog_manager.dialog_data["current_index"] = 0

    # Получаем сохранённые данные диалога
    venues_dicts = dialog_manager.dialog_data.get("venues", [])
    current_index = dialog_manager.dialog_data.get("current_index", 0)
    lang = dialog_manager.dialog_data.get("lang", "en")

    # Если список пуст — возвращаем заглушку и скрываем кнопки
    if not venues_dicts:
        return {
            "card_text": Lexicon.VENUE_ERROR[lang]["empty_list"],
            "counter": "0/0",
            "has_data": False  # Скрываем кнопки
        }

    venue_dict = venues_dicts[current_index]

    # Преобразуем словарь в объект и формируем текст карточки
    # Защищаемся от ошибок некорректных данных
    try:
        venue_obj = Venue(**venue_dict)
        card_text = venue_obj.format_card()
    except Exception:
        card_text = Lexicon.VENUE_ERROR[lang]["data_display_error"]

    return {
        "card_text": card_text,
        "counter": f"{current_index + 1}/{len(venues_dicts)}",
        "has_data": True
    }

venues_window = Window(
    Format("{counter}"),
    Format("\n<b>{card_text}</b>"),

    Row(
        Button(Const("⬅️"), id="btn_prev", on_click=on_prev),
        Button(Const("➡️"), id="btn_next", on_click=on_next),
        # Кнопки показываются только если has_data = True
        when="has_data"
    ),

    state=Processing.scrolling,
    getter=get_venue_data
)

venue_dialog = Dialog(venues_window)