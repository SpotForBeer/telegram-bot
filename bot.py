# --- ЗАПУСК БОТА И ИНИЦИАЛИЗАЦИЯ ---
import asyncio
import logging
from os import getenv
import sys

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers.start import router as start_router
from handlers.search_handler import router as search_router

from aiogram_dialog import setup_dialogs
from dialogs.venue_dialog import venue_dialog

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(start_router)
dp.include_router(search_router)
dp.include_router(venue_dialog)

async def main():
    bot = Bot(token=getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    setup_dialogs(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())