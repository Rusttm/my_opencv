from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

my_reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
            KeyboardButton(text="О боте"),
        ],
        [
            KeyboardButton(text="Реквизиты Компании"),
            KeyboardButton(text="Платежные реквизиты"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что Вас интересует"
)

del_kb = ReplyKeyboardRemove()