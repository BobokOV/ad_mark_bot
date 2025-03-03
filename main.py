import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

from config.bot_token import BOT_TOKEN
from config.api_token import API_TOKEN
from keyboards import main_kb as kb

from vk_utils import get_last_5_creative_statuses_string

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработка старта
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    Обрабатывает команду /start и отправляет приветственное сообщение.
    """
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=kb)

@dp.message(F.text == "Получить результаты согласования креативов из ЕРИР")
async def a_handler (massage: types.Message) -> None:
    text = get_last_5_creative_statuses_string(api_token=API_TOKEN)
    await massage.answer(f"{text}")

# Все остальные сообщения
@dp.message()
async def main_handler(message: types.Message) -> None:
    """
    Хендлер для обработки всех сообщений, кроме обработанных выше
    """
    await message.answer("Эта команда не обрабатывается")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())