# handler for inline keybords callbacks

import datetime
import logging
import os
import aiofiles
from aiogram import types, Router, F, Bot, flags
from aiogram.types import BufferedInputFile
from aiogram.utils.callback_answer import CallbackAnswer, CallbackAnswerMiddleware
from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterFinList, BOTFilterAdminList


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
callback_router.callback_query.middleware(
    CallbackAnswerMiddleware(pre=True, text="🤔 Подождите еще несколько секунд", cache_time=10))


@callback_router.callback_query(F.data.startswith("download_video_"), BOTFilterAdminList())
@flags.callback_answer(pre=False, cache_time=10)
async def download_video_file(callback: types.CallbackQuery, callback_answer: CallbackAnswer, bot: Bot):
    extra_data = callback.data[15:]
    chat_id = extra_data.split("_")[0]
    video_file_name = extra_data[len(chat_id) + 1:]
    # recieve chat_id
    if extra_data:
        temp_msg = await bot.send_sticker(chat_id=int(chat_id), sticker=_await_sticker)
        temp_msg2 = await bot.send_message(chat_id=int(chat_id), text=f"Отчет готовится, это займет около 1 минуты ...")
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        up_up_cur_file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        video_dir = os.path.join(up_up_cur_file_path, _detect_dir, _detect_data_dir, _detect_cap_dir, _detect_video_dir)
        video_path = os.path.join(video_dir, video_file_name)
        async with aiofiles.open(video_path, mode="rb") as rec_video:
            await bot.send_video(chat_id=chat_id, video=BufferedInputFile(file=await rec_video.read(),
                                                                          filename=f"{video_file_name}"))
    except Exception as e:
        res_str = f"Can't form accounts report, Error:\n {e}"
        logging.warning(res_str)
    finally:
        if extra_data:
            await bot.delete_messages(chat_id=extra_data, message_ids=[temp_msg.message_id, temp_msg2.message_id])
    callback_answer.text = str(f"Отчет на {today}\n отправлен")
    await callback.answer()
