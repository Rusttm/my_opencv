import datetime
import logging
import os

import aiofiles
from aiogram import types, Router, F, Bot, flags
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.utils.callback_answer import CallbackAnswer, CallbackAnswerMiddleware
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from aiogram.utils.formatting import as_list, as_marked_section, Bold

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterFinList, BOTFilterAdminList
from AiogramPackage.TGAlchemy.TGDbQueriesProd import db_get_prod
# from AiogramPackage.TGConnectors.TGMSConnector import TGMSConnector
from AiogramPackage.TGMiddleWares.TGMWCallbackData import TGMWCallbackData

_static_dir = "data_static"
_reports_img = "plot_img.jpg"
# Bender sticker number
_await_sticker = "CAACAgIAAxkBAAELd3Vl1n8pL3dHXcijRQ6OSUXB4Iu7EwACGwMAAs-71A7CHN2zMqnsdTQE"
_detect_dir = "OCVYolo8"
_detect_data_dir = "data"
_detect_cap_dir = "capture"
_detect_img_dir = "images"
_detect_video_dir = "video"




callback_router = Router()
callback_router.message.filter(BOTFilterChatType(["private"]))
callback_router.callback_query.middleware(CallbackAnswerMiddleware(pre=True, text="🤔 Подождите еще несколько секунд", cache_time=10))

@callback_router.callback_query(F.data.startswith("get_prod_info_"))
async def get_prod_info(callback: types.CallbackQuery, session: AsyncSession):
    prod_id = callback.data[14:]
    prod_description = "Описание недоступно"
    try:
        prod_data = await db_get_prod(prod_id=prod_id, session=session)
        prod_description = prod_data.description
    except Exception as e:
        res_str = f"Can't get description for prod {prod_id}, Error:\n {e}"
        logging.warning(res_str)
    # await callback.answer(f"Описание товара: {prod_description}", show_alert=True)
    await callback.message.answer(f"Описание товара: {prod_description}")
    await callback.answer()

@callback_router.callback_query(F.data.startswith("rep_fin_profit_daily_"), BOTFilterFinList())
async def get_rep_fin_profit_daily(callback: types.CallbackQuery, bot: Bot):
    """ profit report """
    extra_data = callback.data[21:]
    if extra_data:
        temp_msg = await bot.send_sticker(chat_id=int(extra_data), sticker=_await_sticker)
        temp_msg2 = await bot.send_message(chat_id=int(extra_data),
                                           text=f"Отчет готовится, это займет несколько секунд ...")
    try:
        # res_str = await TGMSConnector().get_profit_rep_str_async()
        res_str = "строка с отчетом"
        await callback.message.answer(res_str)
    except Exception as e:
        res_str = f"Can't form daily profit report, Error:\n {e}"
        logging.warning(res_str)
    finally:
        if extra_data:
            await bot.delete_messages(chat_id=extra_data, message_ids=[temp_msg.message_id, temp_msg2.message_id])
    await callback.answer()

@callback_router.callback_query(F.data.startswith("rep_fin_balance_"), BOTFilterFinList())
# @flags.callback_answer(pre=False, cache_time=60)
async def get_rep_bal(callback: types.CallbackQuery, bot: Bot):
    extra_data = callback.data[16:]
    if extra_data:
        temp_msg = await bot.send_sticker(chat_id=int(extra_data), sticker=_await_sticker)
        temp_msg2 = await bot.send_message(chat_id=int(extra_data),
                                           text=f"Отчет готовится, это займет около 1 минуты ...")
    try:
        # res_str = await TGMSConnector().get_bal_rep_str_async()
        res_str = "строка с отчетом"
        await callback.message.answer(res_str)
    except Exception as e:
        res_str = f"Can't form balance report, Error:\n {e}"
        logging.warning(res_str)
    finally:
        if extra_data:
            await bot.delete_messages(chat_id= extra_data, message_ids=[temp_msg.message_id, temp_msg2.message_id])

    await callback.answer()
@callback_router.callback_query(F.data.startswith("rep_fin_debt_"), BOTFilterFinList())
async def get_rep_debt(callback: types.CallbackQuery, bot: Bot):
    extra_data = callback.data[13:]
    if extra_data:
        temp_msg = await bot.send_sticker(chat_id=int(extra_data), sticker=_await_sticker)
        temp_msg2 = await bot.send_message(chat_id=int(extra_data),
                                           text=f"Отчет готовится, это займет несколько секунд ...")
    try:
        # res_str = await TGMSConnector().get_debt_rep_str_async()
        res_str = "строка с отчетом"
        await callback.message.answer(res_str)
    except Exception as e:
        res_str = f"Can't form debt report, Error:\n {e}"
        logging.warning(res_str)
    finally:
        if extra_data:
            await bot.delete_messages(chat_id= extra_data, message_ids=[temp_msg.message_id, temp_msg2.message_id])

    await callback.answer()
@callback_router.callback_query(F.data.startswith("rep_fin_margin_"), BOTFilterFinList())
async def get_rep_margins(callback: types.CallbackQuery, bot: Bot):
    extra_data = callback.data[15:]
    if extra_data:
        temp_msg = await bot.send_sticker(chat_id=int(extra_data), sticker=_await_sticker)
        temp_msg2 = await bot.send_message(chat_id=int(extra_data),
                                           text=f"Отчет готовится, это займет несколько секунд ...")
    try:
        # res_str = await TGMSConnector().get_margins_rep_str_async()
        res_str = "строка с отчетом"
        await callback.message.answer(res_str)
    except Exception as e:
        res_str = f"Can't form margins report, Error:\n {e}"
        logging.warning(res_str)
    finally:
        if extra_data:
            await bot.delete_messages(chat_id= extra_data, message_ids=[temp_msg.message_id, temp_msg2.message_id])


    await callback.answer()

@callback_router.callback_query(F.data.startswith("rep_fin_account_"), BOTFilterFinList())
async def get_rep_account(callback: types.CallbackQuery, bot: Bot):
    extra_data = callback.data[16:]
    if extra_data:
        temp_msg = await bot.send_sticker(chat_id=int(extra_data), sticker=_await_sticker)
        temp_msg2 = await bot.send_message(chat_id=int(extra_data),
                                           text=f"Отчет готовится, это займет несколько секунд ...")
    # temp_msg = await bot.send_message(chat_id=extra_data, text=extra_data)
    try:
        # res_str = await TGMSConnector().get_account_rep_str_async()
        res_str = "строка с отчетом"
        await callback.message.answer(res_str)
    except Exception as e:
        res_str = f"Can't form accounts report, Error:\n {e}"
        logging.warning(res_str)
    finally:
        if extra_data:
            await bot.delete_messages(chat_id= extra_data, message_ids=[temp_msg.message_id, temp_msg2.message_id])

    await callback.answer()


@callback_router.callback_query(F.data.startswith("rep_fin_daily_"), BOTFilterFinList())
@flags.callback_answer(pre=False, cache_time=10)
async def get_rep_daily(callback: types.CallbackQuery, callback_answer: CallbackAnswer, bot: Bot):
    extra_data = callback.data[14:]  # recieve chat_id
    if extra_data:
        temp_msg = await bot.send_sticker(chat_id=int(extra_data), sticker=_await_sticker)
        temp_msg2 = await bot.send_message(chat_id=int(extra_data), text=f"Отчет готовится, это займет около 1 минуты ...")
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    res_str = str(f"Отчет на {today}\n")
    try:
        # res_str += await TGMSConnector().get_summary_rep_str_async()
        res_str = "строка с отчетом"
        await callback.message.answer(res_str)
    except Exception as e:
        res_str = f"Can't form accounts report, Error:\n {e}"
        logging.warning(res_str)
    finally:
        if extra_data:
            await bot.delete_messages(chat_id= extra_data, message_ids=[temp_msg.message_id, temp_msg2.message_id])
    callback_answer.text = str(f"Отчет на {today}\n отправлен")
    await callback.answer()

@callback_router.callback_query(F.data.startswith("download_video_"), BOTFilterAdminList())
@flags.callback_answer(pre=False, cache_time=10)
async def download_video_file(callback: types.CallbackQuery, callback_answer: CallbackAnswer, bot: Bot):
    extra_data = callback.data[15:]
    chat_id = extra_data.split("_")[0]
    print(f"{chat_id=}")
    video_file_name = extra_data[len(chat_id)+1:]
    print(f"{video_file_name=}")
    # recieve chat_id
    if extra_data:
        temp_msg = await bot.send_sticker(chat_id=int(chat_id), sticker=_await_sticker)
        temp_msg2 = await bot.send_message(chat_id=int(chat_id), text=f"Отчет готовится, это займет около 1 минуты ...")
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    res_str = str(f"Отчет на {today}\n")
    try:
        # res_str += await TGMSConnector().get_summary_rep_str_async()
        res_str = f"file {video_file_name=}"

        up_up_cur_file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        video_dir = os.path.join(up_up_cur_file_path, _detect_dir, _detect_data_dir, _detect_cap_dir, _detect_video_dir)
        video_path = os.path.join(video_dir, video_file_name)
        print(f"{video_path=}")
        async with aiofiles.open(video_path, mode="rb") as rec_video:
            await bot.send_video(chat_id=chat_id, video=BufferedInputFile(file=await rec_video.read(),
                                                                     filename=f"{video_file_name}"))

        await callback.message.answer(f"video {video_file_name} send")
    except Exception as e:
        res_str = f"Can't form accounts report, Error:\n {e}"
        logging.warning(res_str)
    finally:
        if extra_data:
            await bot.delete_messages(chat_id= extra_data, message_ids=[temp_msg.message_id, temp_msg2.message_id])
    callback_answer.text = str(f"Отчет на {today}\n отправлен")
    await callback.answer()
