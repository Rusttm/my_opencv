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

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterFinList, BOTFilterIsGroupAdmin, \
    BOTFilterAdminList
from AiogramPackage.TGKeyboards.TGKeybInline import get_callback_btns
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1_admin, del_kb, reply_kb_lvl2_admin
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
_delay_time = 6000   # sec


admin_private_router = Router()
admin_private_router.message.filter(BOTFilterChatType(["private"]), BOTFilterAdminList())


class SaveFile(StatesGroup):
    event_file = State()


class DownLoadFile(StatesGroup):
    download_file = State()


def clean_text(text: str):
    """ вырезает из текста знаки"""
    return text.translate(str.maketrans("", "", punctuation))


async def reload_admins_list(bot: Bot):
    """ this module loads lists of groups members and restricted words
    some lists should be reloaded by /admin command"""
    _main_key = "bot_config"
    _admin_key = "admin_members"
    _filters_key = "filters_config"
    _fin_key = "fin_members"
    _restricted_key = "restricted_words"
    _config_dir_name = "config"
    _config_file_name = "bot_main_config.json"
    _static_dir = "data_static"
    _module_config: dict = None
    from AiogramPackage.TGConnectors.BOTReadJson import BOTReadJson
    connector = BOTReadJson()
    _module_config = await connector.get_main_config_json_data_async(_config_dir_name, _config_file_name)
    admin_members_dict = _module_config.get(_main_key).get(_admin_key)
    fin_members_dict = _module_config.get(_main_key).get(_fin_key)
    bot.admins_list = list(admin_members_dict.values())
    logging.info(f"reloaded {bot.admins_list=}")
    bot.fins_list = list(fin_members_dict.values())
    logging.info(f"reloaded {bot.fins_list=}")
    restricted_words_list = _module_config.get(_main_key).get(_restricted_key)
    bot.restricted_words = list(restricted_words_list)
    logging.info(f"reloaded {bot.restricted_words=}")
    # logging.info(f" now {bot.chat_group_admins_list=}")
    if not bot.chat_group_admins_list:
        bot.chat_group_admins_list = bot.admins_list
        logging.info(f" and {bot.chat_group_admins_list=}")
    # print(f"{bot.admins_list=}")
    filters_dict = _module_config.get(_main_key).get(_filters_key)
    bot.filters_dict = dict(filters_dict)
    logging.info(f"reloaded {bot.filters_dict=}")


@admin_private_router.message(Command("admin", ignore_case=True))
async def admin_cmd(message: types.Message, bot: Bot):
    """ this handler reloads group admins list"""
    await reload_admins_list(bot=bot)
    await message.delete()


@admin_private_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{message.from_user.first_name}, welcome to admin main menu!",
                         reply_markup=reply_kb_lvl1_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"))

@admin_private_router.message(or_f(Command("addition", ignore_case=True), (F.text.lower().contains("дополнительно"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{message.from_user.first_name}, welcome to admin file menu!",
                         reply_markup=reply_kb_lvl2_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"))

@admin_private_router.message(Command("save", "upload", ignore_case=True))
@admin_private_router.message(StateFilter(None), F.text == "save")
async def start_save_img(message: types.Message, state: FSMContext):
    await state.set_state(SaveFile.event_file)
    await message.answer("Загрузите файл")


@admin_private_router.message(SaveFile.event_file)
async def add_event_img(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    file_id = message.document.file_id
    data_dict = dict()
    data_dict["from_chat_id"] = message.from_user.id
    data_dict["to_chat_id"] = message.chat.id
    data_dict["event_msg"] = "сообщение:" + str(message.text)
    data_dict["event_descr"] = "описание:" + str(message.text)
    data_dict["event_img"] = file_id
    try:
        await db_add_event(session, data_dict)
        file = await bot.get_file(file_id)
        file_path = file.file_path
        # version1
        file_name = "bot_" + str(file_path.split("/")[-1])
        # version2
        # file_name = file_id
        # version3
        up_cur_file_path = os.path.dirname(os.path.dirname(__file__))
        static_file = os.path.join(up_cur_file_path, _static_dir, file_name)
        # print(f"{static_file=}")
        # version1 with binary object
        # my_object = typing.BinaryIO()
        # MyBinariIO = await bot.download(file, my_object)
        # version2
        await bot.download(file, static_file)
    except Exception as e:
        msg = f"Не смог добавить фото и сообщение в базу, ошибка: \n {e}"
        await message.answer(msg)
    else:
        await message.answer(f"Файл загружен, можете скачать его коммандами:\n <b>/download {file_name}</b>\n или \n <b>download_{file_name}</b>")
    finally:
        await state.clear()


@admin_private_router.message(SaveFile.event_file)
async def add_event_img(message: types.Message):
    await message.answer("photo not added, please send me a photo")


# from https://mastergroosha.github.io/aiogram-3-guide/messages/
@admin_private_router.message(Command("download"))
@admin_private_router.message(StateFilter(None), F.text.lower().contains("получить"))
async def download_static_file(message: types.Message, command: CommandObject, state: FSMContext):
    if command.args is None:
        await state.set_state(DownLoadFile.download_file)
        await message.answer("Введите название файла")
        # return
    else:
        # await state.update_data(file_name=command.args)
        # return
        try:
            file_name = command.args
            up_cur_file_path = os.path.dirname(os.path.dirname(__file__))
            static_file = os.path.join(up_cur_file_path, _static_dir, file_name)
            async with aiofiles.open(static_file, 'rb') as image_from_buffer:
                result = await message.answer_photo(
                    BufferedInputFile(file=await image_from_buffer.read(), filename=file_name),
                    caption=f"{file_name}")
        except Exception as e:
            msg = f"Cant load file from destination, Error: \n {e}"
            await message.answer(msg)
        else:
            await state.clear()
            await message.answer(f"Файл {file_name} отправлен!")

@admin_private_router.message(DownLoadFile.download_file)
@admin_private_router.message(F.text.lower().startswith("download_"))
async def save_static_file(message: types.Message, state: FSMContext, bot: Bot):
    """  downloading and sending img from bot static directory"""
    if message.text.startswith("download_"):
        file_name = message.text[9:]
    else:
        try:
            current_state = await state.get_state()
            if current_state == DownLoadFile.download_file:
                data_dict = await state.get_data()
                file_name = data_dict.get("file_name", None)
                if not file_name:
                    file_name = message.text
        except Exception as e:
            msg = f"cant get file_name info, Error \n {e}"
            print(msg)
    # await message.answer(f"Отправляю файл ...")
    tech_msg_1 = await bot.send_message(chat_id=message.chat.id, text=f"Отправляю файл ...")
    try:
        up_cur_file_path = os.path.dirname(os.path.dirname(__file__))
        static_file = os.path.join(up_cur_file_path, _static_dir, file_name)
        async with aiofiles.open(static_file, 'rb') as file_from_buffer:
            result = await message.answer_document(
                BufferedInputFile(file=await file_from_buffer.read(), filename=f"bot_{file_name}"), caption=f"Файл")
    except Exception as e:
        msg = f"Cant load file from destination, Error: \n {e}"
        await message.answer(msg)
    else:
        msg_id = message.message_id
        await bot.delete_messages(chat_id=message.chat.id, message_ids=[msg_id-1, msg_id, tech_msg_1.message_id])
    finally:
        await state.clear()


@admin_private_router.message(CommandStart())
@admin_private_router.message(F.text.lower() == "start")
async def admin_menu_cmd(message: types.Message):
    await message.answer(f"Hi, {html.quote(message.from_user.first_name)}, welcome to 👨🏼‍🔧admin panel\n Please renew data with /admin command",
                         reply_markup=reply_kb_lvl1_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"
                         ))

class SetTime(StatesGroup):
    time_set = State()

@admin_private_router.message(StateFilter('*'), Command("cancel", ignore_case=True))
@admin_private_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_find_instrument(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(f"Ввод ❌<b>Отменен</b>", reply_markup=
    reply_kb_lvl1_admin.as_markup(resize_keyboard=True, input_field_placeholder="Что Вас интересует?"))


@admin_private_router.message(Command("time"))
async def admin_menu_cmd(message: types.Message, state: FSMContext):
    await message.answer(f"If you want to set time delay, enter number or type cancel\n", input_field_placeholder="Введите количество секунд")
    await state.set_state(SetTime.time_set)

@admin_private_router.message(SetTime.time_set)
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

@admin_private_router.message(Command("records"))
@admin_private_router.message(F.text.lower().contains("записи"))
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
                                             caption=f"🎬Запись от {img_data}, длительностью {img_timelaps} секунд.\n"
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
