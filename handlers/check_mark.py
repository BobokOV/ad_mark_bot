from aiogram import types, Router, F
from aiogram.filters import CommandStart

from keyboards import main_kb as kb
from vk_utils import get_last_5_creative_statuses_string
from config.api_token import API_TOKEN # Импорт API_TOKEN из config

router = Router()

# Обработка старта
@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    Обрабатывает команду /start и отправляет приветственное сообщение.
    """
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=kb)

@router.message(F.text == "Получить результаты согласования креативов из ЕРИР")
async def erir_results_handler(massage: types.Message) -> None:
    text = get_last_5_creative_statuses_string(api_token=API_TOKEN)
    await massage.answer(f"{text}")

# Все остальные сообщения (можно оставить здесь или переместить в main.py, в зависимости от структуры)
@router.message()
async def main_handler(message: types.Message) -> None:
    """
    Хендлер для обработки всех сообщений, кроме обработанных выше
    """
    await message.answer("Эта команда не обрабатывается")