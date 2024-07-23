from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

reply_kb_lvl1 = ReplyKeyboardBuilder()

# start keyboard for everyone
reply_kb_lvl1.add(
    KeyboardButton(text="🤝Контакты"))
# start keyboard shape
reply_kb_lvl1.adjust(1, 1)

# second keyboard for everyone
reply_kb_lvl2 = ReplyKeyboardBuilder()
reply_kb_lvl2.add(
    KeyboardButton(text="🫴Запросить доступ"),
    KeyboardButton(text="🚧Under construction"))
reply_kb_lvl2.adjust(2, 1)

# start keyboard for admin
reply_kb_lvl1_admin = ReplyKeyboardBuilder()
# adds reports to common keyboard
reply_kb_lvl1_admin.attach(reply_kb_lvl1)
reply_kb_lvl1_admin.row(KeyboardButton(text="📹Запросить записи камер"))
reply_kb_lvl1_admin.row(KeyboardButton(text="🗃️Дополнительно"))
del_kb = ReplyKeyboardRemove()

# second keyboard for admin
reply_kb_lvl2_admin = ReplyKeyboardBuilder()
reply_kb_lvl2_admin.row(
    KeyboardButton(text="📥Записать файл"),
    KeyboardButton(text="💾Получить файл"),
    KeyboardButton(text="📃Меню"))
reply_kb_lvl2_admin.adjust(2, 1)

# start keyboard for stockers
reply_kb_lvl1_stock = ReplyKeyboardBuilder()
# adds reports to common keyboard
reply_kb_lvl1_stock.attach(reply_kb_lvl1)
reply_kb_lvl1_stock.row(KeyboardButton(text="📹Запросить записи камер"))


# inline kbd constructor
def get_my_kb(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2, 2),
):
    keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))
    return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)
