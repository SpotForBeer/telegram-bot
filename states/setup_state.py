# Классы состояний (FSM)
from aiogram.filters.state import State, StatesGroup

# --- СОСТОЯНИЯ НАЧАЛЬНОГО ОПРОСА ---
class StartPool(StatesGroup):
    language = State()
    location = State()
    manual_location = State()
    auto_location = State()

# --- СОСТОЯНИЯ КРИТЕРИЕВ И РЕЗУЛЬТАТА ---
class Processing(StatesGroup):
    criteria = State()
    scrolling = State()
