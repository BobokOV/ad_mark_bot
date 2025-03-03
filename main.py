import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import logging

from config.bot_token import BOT_TOKEN
from handlers import doc_creation, check_mark # Импорт обработчиков

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher(storage=MemoryStorage())

    # 🔹 Регистрация роутеров (handler-ов)
    dp.include_router(doc_creation.router) # Регистрация роутера для старых команд
    dp.include_router(check_mark.router) # Регистрация роутера для создания документов

    # 🔹 Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.info("Bot started")
    asyncio.run(main())