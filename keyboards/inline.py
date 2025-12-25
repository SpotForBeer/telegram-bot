from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_ua")
    )
    builder.adjust(3) #Количество кнопок в одном ряду
    return builder.as_markup()

def get_location_keyboard(lang):
    texts = {
        "en": ("📍 My location", "⌨️ Enter city"),
        "ru": ("📍 Моя локация", "⌨️ Ввести город"),
        "ua": ("📍 Моя локація", "⌨️ Ввести місто")
    }
    text = texts.get(lang, texts["en"])

    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=text[0], callback_data="auto"),
        InlineKeyboardButton(text=text[1], callback_data="manual")
    )
    builder.adjust(2) #Количество кнопок в одном ряду

    return builder.as_markup()

