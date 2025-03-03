from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import requests

from states.document_form import DocumentForm  # Импорт машины состояний

from config.api_GAS_token import token
from config.api_url import api_url

router = Router()

@router.message(Command("create_contract"))
async def create_contract(message: Message, state: FSMContext):
    await state.set_state(DocumentForm.client_name)
    await message.answer("Введите имя заказчика")

@router.message(DocumentForm.client_name)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await state.set_state(DocumentForm.client_documents)
    await message.answer("Введите реквизиты заказчика")

@router.message(DocumentForm.client_documents)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(client_documents=message.text)
    await state.set_state(DocumentForm.performer_name)
    await message.answer("Введите имя исполнителя")

@router.message(DocumentForm.performer_name)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(performer_name=message.text)
    await state.set_state(DocumentForm.performer_documents)
    await message.answer("Введите реквизиты исполнителя")

@router.message(DocumentForm.performer_documents)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(performer_documents=message.text)
    await state.set_state(DocumentForm.date)
    await message.answer("Введите дату")

@router.message(DocumentForm.date)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(DocumentForm.is_marked)

    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Да")
    keyboard.button(text="Нет")
    keyboard.adjust(2)

    markup = keyboard.as_markup(one_time_keyboard=True)

    await message.answer("Нужно ли маркировать публикацию?", reply_markup=markup)

@router.message(DocumentForm.is_marked)
async def create_contract(message: Message, state: FSMContext):
    if message.text == "Да":
        await state.update_data(is_marked="True")
    elif message.text == "Нет":
        await state.update_data(is_marked="False")

    await state.set_state(DocumentForm.link)
    await message.answer("Введите ссылку на блогера")

@router.message(DocumentForm.link)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await state.set_state(DocumentForm.channel_name)
    await message.answer("Введите название канала")

@router.message(DocumentForm.channel_name)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(channel_name=message.text)
    await state.set_state(DocumentForm.cost)
    await message.answer("Введите стоимость публикации (сумму, которую перевели блогеру)")

@router.message(DocumentForm.cost)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(cost=message.text)
    await state.set_state(DocumentForm.client_type)

    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="ИП")
    keyboard.button(text="СЗ")
    keyboard.button(text="ООО")
    keyboard.button(text="ОАО")
    keyboard.adjust(2)

    markup = keyboard.as_markup(one_time_keyboard=True)

    await message.answer("Выберите тип заказчика", reply_markup=markup)


@router.message(DocumentForm.client_type)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(client_type=message.text)
    await state.set_state(DocumentForm.performer_type)

    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="ИП")
    keyboard.button(text="СЗ")
    keyboard.button(text="ООО")
    keyboard.button(text="ОАО")
    keyboard.adjust(2)

    markup = keyboard.as_markup(one_time_keyboard=True)

    await message.answer("Выберите тип исполнителя", reply_markup=markup)

@router.message(DocumentForm.performer_type)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(performer_type=message.text)
    await state.set_state(DocumentForm.social_network)

    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Instagram")
    keyboard.button(text="Telegram")
    keyboard.button(text="YouTube")
    keyboard.button(text="TikTok")
    keyboard.button(text="Twitch")
    keyboard.button(text="ВК")
    keyboard.adjust(2)

    markup = keyboard.as_markup(one_time_keyboard=True)

    await message.answer("Выберите социальную сеть, в которой будет размещена реклама\nВозможно ввести несколько" +
                         " социальных сетей, для этого пишите боту сообщение", reply_markup=markup)

@router.message(DocumentForm.social_network)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(social_network=message.text)
    await state.set_state(DocumentForm.format)
    await message.answer("Введите формат рекламы")

@router.message(DocumentForm.format)
async def create_contract(message: Message, state: FSMContext):
    await state.update_data(format=message.text)
    await state.set_state(DocumentForm.confirmation)

    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Создать договор")
    keyboard.button(text="Отменить создание договора")
    keyboard.button(text="Изменить договор (кнопка не работает!)")
    keyboard.adjust(2)

    markup = keyboard.as_markup(one_time_keyboard=True)

    await message.answer("Подтвердите создание договора", reply_markup=markup)



@router.message(DocumentForm.confirmation)
async def create_contract(message: Message, state: FSMContext):
    if message.text == "Создать договор":
        data = await state.get_data()
        response = requests.post(api_url, data={**data, "token": token}).json()
        text = f"Документ создан!\nОткрыть документ: {response['url']}\nПроверь данные документа. Особенно внимательно проверь подписи. После проверки экспортируй в пдф и отправляй блогеру" if response.get(
            "success") else f"Ошибка: {response.get('error')}"
        await message.answer(text)

    await state.clear()