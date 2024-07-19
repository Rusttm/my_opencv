from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    res_list = []
    for row in items:
        if type(row) == list:
            temp_list = [KeyboardButton(text=item) for item in row]
            res_list.append(temp_list)
        else:
            res_list.append(KeyboardButton(text=row))
    return ReplyKeyboardMarkup(keyboard=res_list, resize_keyboard=True, input_field_placeholder="Введите комманду")


del_kb = ReplyKeyboardRemove()
