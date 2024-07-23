""" роутер приват чат с админом """

import logging
import os
import typing

import aiofiles
from aiogram import types, Router, F, Bot, html
from aiogram.filters import CommandStart, Command, or_f, IS_ADMIN, StateFilter, CommandObject

# from aiogram.filters.chat_member_updated import IS_ADMIN, ChatMemberUpdatedFilter, IS_MEMBER
from string import punctuation

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.deep_linking import create_start_link
from aiogram.methods.delete_message import DeleteMessage

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterStokersList
from AiogramPackage.TGKeyboards.TGKeybInline import get_callback_btns
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1_admin, reply_kb_lvl1_stock, del_kb, reply_kb_lvl2_admin
from AiogramPackage.TGAlchemy.TGDbQueriesEvent import db_add_event
from AiogramPackage.TGAlchemy.TGModelEvent import TGModelEvent

import datetime

_static_dir = "data_static"
_pkg_dir = "AiogramPackage"
_detect_data_dir = "data"
_detect_cap_dir = "capture"
_detect_img_dir = "images"
_detect_video_dir = "video"
_reports_img = "plot_img.jpg"
_await_sticker = "CAACAgIAAxkBAAELd3Vl1n8pL3dHXcijRQ6OSUXB4Iu7EwACGwMAAs-71A7CHN2zMqnsdTQE"
_delay_time = 600   # sec


stokers_private_router = Router()
stokers_private_router.message.filter(BOTFilterChatType(["private"]), BOTFilterStokersList())




def clean_text(text: str):
    """ вырезает из текста знаки"""
    return text.translate(str.maketrans("", "", punctuation))

class SetTime(StatesGroup):
    time_set = State()


@stokers_private_router.message(CommandStart())
@stokers_private_router.message(F.text.lower() == "start")
async def admin_menu_cmd(message: types.Message):
    await message.answer(f"Hi, {html.quote(message.from_user.first_name)}, welcome to 👨🏼‍🔧stokers panel",
                         reply_markup=reply_kb_lvl1_stock.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"
                         ))
@stokers_private_router.message(StateFilter('*'), Command("cancel", ignore_case=True))
@stokers_private_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_find_instrument(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(f"Ввод ❌<b>Отменен</b>", reply_markup=
    reply_kb_lvl1_admin.as_markup(resize_keyboard=True, input_field_placeholder="Что Вас интересует?"))


@stokers_private_router.message(Command("time"))
async def admin_menu_cmd(message: types.Message, state: FSMContext):
    await message.answer(f"If you want to set time delay, enter number or type cancel\n", input_field_placeholder="Введите количество секунд")
    await state.set_state(SetTime.time_set)

@stokers_private_router.message(SetTime.time_set)
async def admin_menu_cmd(message: types.Message, state: FSMContext):
    await message.answer(f"If you want to set time delay, enter number or type cancel\n", input_field_placeholder="Введите количество секунд")
    global _delay_time
    seconds_num = _delay_time
    try:
        seconds_num = int(message.text)
    except:
        await message.answer(f"your enter {message.text} cant convert to integer.\n"
                             f" please make request again")
    else:
        _delay_time = seconds_num
        await message.answer(f"your change time delay to {seconds_num} second")
    finally:
        await state.clear()

@stokers_private_router.message(Command("records"))
@stokers_private_router.message(F.text.lower().contains("записи"))
async def send_msgs_with_cam_photos(message: types.Message, bot: Bot):
    """ main handler for records requests """
    try:
        from AiogramPackage.TGConnectors.TGDBConnector import TGDBConnector
        conn = TGDBConnector()
        records_list = await conn.get_detected_obj_last_delay_async(delay=_delay_time)

        if not records_list:
            await message.answer(f"on this time ({datetime.datetime.now().strftime("%H:%M")}) there are no new records")
        else:
            prj_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            img_dir = os.path.join(prj_dir, _detect_data_dir, _detect_cap_dir, _detect_img_dir)
            try:
                for rec in records_list:
                    img_name = rec.get("image_file")
                    video_name = rec.get("video_file")
                    img_data = rec.get("inserted_at").strftime("%H:%M")
                    img_timelaps = int(rec.get("time"))
                    img_obj = rec.get("category_name")
                    img_obj_count = int(rec.get("count"))
                    img_path = os.path.join(img_dir, img_name)
                    # await message.answer(f"image file:{img_path=}")
                    async with aiofiles.open(img_path, mode="rb") as rec_img:
                        await bot.send_photo(chat_id=message.chat.id,
                                             photo=BufferedInputFile(file=await rec_img.read(),
                                                                     filename=f"{img_name}"),
                                             caption=f"🎬Запись {video_name} от {img_data}, "
                                                     f"длительностью {img_timelaps} секунд.\n"
                                                     f"Обнаружено {img_obj_count} {img_obj} ",
                                             reply_markup=get_callback_btns(btns={
                                                 "🎬Скачать видео": f"download_video_{message.chat.id}_{video_name}",
                                             }),
                                             request_timeout=100)

            except Exception as e:
                err_msg = f"Не могу отправить данные об обновлениях в чат {message.chat.id}, ошибка:\n{e}"
                err_msg += f"Найдено {len(records_list)} записей, ошибка:\n{e}"
                await message.answer(err_msg)
    except Exception as e:
        await message.answer(f"Не могу найти записи камер, ошибка:\n{e}")
    print(datetime.datetime.now(), "\nCheck the DataBase")
