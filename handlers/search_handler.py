from dataclasses import asdict

import requests
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode

from locales import Lexicon
from states.setup_state import Processing
from utils.ai_logic import get_recommendations
from utils.ai_responce_parser import parse_ai_response

router = Router()
url = "https://api-u9q2.onrender.com/recommendations/venues"

#Получение критериев, их обработка и переход к диалогу
@router.message(Processing.criteria)
async def process_criteria(message: Message, state: FSMContext, dialog_manager: DialogManager):
    criteria = message.text
    await state.update_data(criteria=criteria)

    user_data = await state.get_data()
    city = user_data.get("city")
    lang = user_data.get("lang", "en")
    criteria = message.text

    status_msg = await message.answer(Lexicon.get(Lexicon.VENUE_ANALIZING, lang))

    data = {
        "city": city,
        "lang": lang,
        "criteria": criteria,
    }

    json_response = requests.post(url, json=data)
    json_response.raise_for_status()

    response_data = json_response.json()

    venues_list = await parse_ai_response(response_data)

    print("[DEBUG] Ответ от API:", json_response.text)  # Сырой JSON
    print("[DEBUG] Распарсенный dict:", response_data)

    await status_msg.delete()

    if not venues_list:
        await message.answer(Lexicon.get(Lexicon.CRITERIA_FAILED, lang))
        return

    venues_dicts = [asdict(v) for v in venues_list]

    await dialog_manager.start(
        state=Processing.scrolling,
        data={"venues": venues_dicts},
        mode=StartMode.RESET_STACK
    )