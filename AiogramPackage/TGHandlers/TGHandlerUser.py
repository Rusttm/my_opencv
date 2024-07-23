import logging
import os

import aiofiles
import aiogram.exceptions
from aiogram import types, Router, F, Bot, html
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.filters.callback_data import CallbackQueryFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from aiogram.utils.formatting import as_list, as_marked_section, Bold

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType
# from AiogramPackage.TGKeyboards import TGKeybReplyMarkup as my_reply_kb
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1, reply_kb_lvl2, del_kb
from AiogramPackage.TGKeyboards.TGKeybReplyList import make_row_keyboard
from AiogramPackage.TGKeyboards.TGKeybInline import get_callback_btns, get_url_btns, get_mixed_btns
from AiogramPackage.TGAlchemy.TGModelProd import TGModelProd
from AiogramPackage.TGAlchemy.TGModelStock import get_stock_row

_static_dir = "data_static"
_instrument_img = "instrument_img.jpg"
_spares_img = "spares_img.jpg"

user_router = Router()
user_router.message.filter(BOTFilterChatType(["private"]))


@user_router.message(CommandStart())
@user_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
@user_router.message(F.text.lower() == "start")
async def start_cmd(message: types.Message):
    # version1
    # await message.answer(f"{message.from_user.first_name}, welcome to bot!", reply_markup=my_reply_kb.my_reply_kb)
    # version2
    await message.answer(f"Здравствуйте, {hbold(message.from_user.first_name)}, добро пожаловать в наш 🥸бот",
                         reply_markup=reply_kb_lvl2.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует"
                         ))

@user_router.message(Command("hide_menu", ignore_case=True))
async def menu_cmd(message: types.Message):
    # ver1
    await message.answer(f"{message.from_user.first_name}, can't hide main menu!", reply_markup=del_kb)


@user_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{html.quote(message.from_user.first_name)}, welcome to main menu!", reply_markup=reply_kb_lvl1)

@user_router.message(F.text.lower().contains("контакты"))
async def company_info_cmd(message: types.Message):
    msg = str('<b>телеграм</b>: @rustammazhatov\n'
              '<b>Email</b>: rustammazhatov@gmail.com\n')
    await message.answer(f"Здравствуйте, {hbold(html.quote(message.from_user.first_name))}, мои контактные данные:\n{msg}")

@user_router.message(F.text.lower().contains("доступ"))
async def company_info_cmd(message: types.Message, bot: Bot):
    msg = str(f"New user <b>{message.chat.id}</b> wants to get info\n")
    admin_id = bot.admins_list[0]
    await bot.send_message(chat_id=admin_id, text=msg)

    await message.answer(f"Здравствуйте, {hbold(html.quote(message.from_user.first_name))}, Вас добавят в группу")
