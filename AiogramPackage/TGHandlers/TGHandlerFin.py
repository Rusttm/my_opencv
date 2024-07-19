""" модерация группы в которой бот является админом"""

import logging
import os
import datetime

import aiofiles
from aiogram import types, Router, F, Bot, flags
from aiogram.filters import CommandStart, Command, or_f, IS_ADMIN
# from aiogram.filters.chat_member_updated import IS_ADMIN, ChatMemberUpdatedFilter, IS_MEMBER
from string import punctuation

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile
from aiogram.utils.callback_answer import CallbackAnswerMiddleware, CallbackAnswer
from aiogram.utils.markdown import hbold

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterFinList, BOTFilterIsGroupAdmin
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1_admin, del_kb
from AiogramPackage.TGKeyboards.TGKeybInline import get_callback_btns
from AiogramPackage.TGConnectors.TGMSConnector import TGMSConnector
from AiogramPackage.TGMiddleWares.TGMWCallbackData import TGMWCallbackData

_static_dir = "data_static"
_reports_img = "plot_img.jpg"
_await_sticker = "CAACAgIAAxkBAAELd3Vl1n8pL3dHXcijRQ6OSUXB4Iu7EwACGwMAAs-71A7CHN2zMqnsdTQE"

fin_group_router = Router()
fin_group_router.message.filter(BOTFilterChatType(["private"]), BOTFilterFinList())


def clean_text(text: str):
    """ вырезает из текста знаки"""
    return text.translate(str.maketrans("", "", punctuation))


class PrepaReport(StatesGroup):
    requested = State()


@fin_group_router.message(CommandStart())
@fin_group_router.message(F.text.lower() == "start")
async def admin_menu_cmd(message: types.Message):
    await message.answer(
        f"Здравствуйте, {message.from_user.first_name}, добро пожаловать в 🧮финансовый блок нашего бота",
        reply_markup=reply_kb_lvl1_admin.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Что Вас интересует?"
        ))


@fin_group_router.message(Command("report", "rep", ignore_case=True))
@fin_group_router.message(F.text.lower().contains("отчет"))
async def menu_cmd(message: types.Message, bot: Bot):

    up_cur_file_path = os.path.dirname(os.path.dirname(__file__))
    static_file = os.path.join(up_cur_file_path, _static_dir, _reports_img)
    async with aiofiles.open(static_file, "rb") as plot_img:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=BufferedInputFile(file=await plot_img.read(), filename="График"),
                             caption=f"Здравствуйте, {hbold(message.from_user.first_name)}, добро пожаловать в 📉<b>отчеты</b>!",
                             reply_markup=get_callback_btns(btns={
                                 "💸Прибыли/Убытки": f"rep_fin_profit_daily_{message.chat.id}",
                                 "⚖️Баланс": f"rep_fin_balance_{message.chat.id}",
                                 "🚬Долги клиентов": f"rep_fin_debt_{message.chat.id}",
                                 "🛠️Отгрузки <30%": f"rep_fin_margin_{message.chat.id}",
                                 "💰Остатки на счетах": f"rep_fin_account_{message.chat.id}",
                                 "📆Итоги на сегодня": f"rep_fin_daily_{message.chat.id}"
                             }),
                             request_timeout=100)

    logging.info("requested reports")


@fin_group_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{message.from_user.first_name}, welcome to admin main menu!",
                         reply_markup=reply_kb_lvl1_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"))


@fin_group_router.message(F.text.lower().startswith("итог"))
async def send_summary_rep_daily(message: types.Message, state: FSMContext, bot: Bot):
    """ send summary daily report"""
    temp_msg = await message.answer("Запрошен большой итоговый отчет, формируется, подождите ...⏱️")
    # from https://zelenka.guru/threads/3538801/
    temp_sticker = await message.reply_sticker(sticker=_await_sticker)
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    res_msg = str(f"Отчет на {today}\n")
    try:
        res_msg += await TGMSConnector().get_summary_rep_str_async()
    except Exception as e:
        msg = f"Can't form summary daily report, Error:\n {e}"
        logging.warning(msg)
        await message.answer(msg)
    else:
        await bot.delete_messages(chat_id=message.chat.id, message_ids=[temp_msg.message_id, temp_sticker.message_id])
        await message.answer(res_msg)
