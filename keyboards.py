from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Получить результаты обработки из erir"),
            KeyboardButton(text="Создать договор")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите кнопку из списка",
    selective=False
)

yn_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите кнопку из списка",
    selective=False
)

type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="СЗ"),
            KeyboardButton(text="ИП"),
            KeyboardButton(text="ООО"),
            KeyboardButton(text="ОАО")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите кнопку из списка",
    selective=False
)

sm_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="instagram"),
            KeyboardButton(text="telegram"),
            KeyboardButton(text="youtube"),
            KeyboardButton(text="twitch"),
            KeyboardButton(text="tiktok"),
            KeyboardButton(text="vk")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите кнопку из списка",
    selective=False
)

konf_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать договор"),
            KeyboardButton(text="Отменить создание договора"),
            KeyboardButton(text="Изменить договор (кнопка не работает!)")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите кнопку из списка",
    selective=False
)
