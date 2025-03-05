from aiogram import types, Router, F
from aiogram.filters import CommandStart

from keyboards import main_kb as kb
from config.api_token import API_TOKEN

from vk_utils import ORDHTTPClient

router = Router()

# Обработка старта
@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    Обрабатывает команду /start и отправляет приветственное сообщение.
    """
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=kb)

@router.message(F.text == "Получить результаты обработки из erir")
async def erir_results_handler(massage: types.Message) -> None:
    async with ORDHTTPClient(base_url="https://api.ord.vk.com",
                             api_token=API_TOKEN) as ord_client:
        text = await ord_client.get_erid_statuses()
    await massage.answer(text + "\n\nПриведены те креативы, контрагенты, площадки и договоры, которые находятся в "
                                "обработке. Если у вас есть креатив и он не появился в этом сообщении, вы можете "
                                "отправлять его блогеру\nКреатив обозначается своим токеном")

# Все остальные сообщения (можно оставить здесь или переместить в main.py, в зависимости от структуры)
@router.message()
async def main_handler(message: types.Message) -> None:
    """
    Хендлер для обработки всех сообщений, кроме обработанных выше
    """
    await message.answer("Эта команда не обрабатывается")