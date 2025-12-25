from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_auto_location_keyboard(lang):
    texts = {
        "ru": "📍 Отправить мою локацию",
        "en": "📍 Send my location",
        "ua": "📍 Надіслати мою локацію"
    }
    text = texts.get(lang, texts["en"])

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text, request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return kb