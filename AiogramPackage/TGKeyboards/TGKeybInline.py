from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from AiogramPackage.TGMiddleWares.TGMWCallbackData import TGMWCallbackData

def get_callback_btns(
        *,
        btns: dict[str, str],
        # btns: dict,
        sizes: tuple[int] = (2,),):
    keyboard = InlineKeyboardBuilder()
    for text, data in btns.items():
        # version1 with data from aiogram.utils.callback_answer import CallbackAnswer
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
        # version2 with own MiddleWare Callbackanswer
        # keyboard.add(InlineKeyboardButton(text=text, callback_data=TGMWCallbackData(text=data)))

    return keyboard.adjust(*sizes).as_markup()

def get_url_btns(
        *,
        btns: dict[str,str],
        sizes: tuple[int] = (2,),):
    keyboard = InlineKeyboardBuilder()
    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))
        # keyboard.add(InlineKeyboardButton(text=text, url=TGMWCallbackData(url=url)))

    return keyboard.adjust(*sizes).as_markup()

def get_mixed_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,),):
    keyboard = InlineKeyboardBuilder()
    for text, value in btns.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))
    return keyboard.adjust(*sizes).as_markup()

def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="💸Прибыли/Убытки", callback_data=TGMWCallbackData(text="rep_fin_profit_daily"))
    keyboard_builder.button(text="⚖️Баланс", callback_data=TGMWCallbackData(text="rep_fin_balance_"))
    keyboard_builder.button(text="🚬Долги клиентов", callback_data=TGMWCallbackData(text="rep_fin_debt_"))
    keyboard_builder.button(text="🛠️Отгрузки <30%", callback_data=TGMWCallbackData(text="rep_fin_margin_"))
    keyboard_builder.button(text="💰Остатки на счетах", callback_data=TGMWCallbackData(text="rep_fin_account_"))
    keyboard_builder.button(text="📆Итоги на сегодня", callback_data=TGMWCallbackData(text=f"rep_fin_daily_"))
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()
