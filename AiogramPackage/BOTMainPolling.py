# from https://docs.aiogram.dev/en/latest/
import asyncio
import datetime
import aiofiles
import aioschedule
import os
from aiogram import Bot, Dispatcher, types
# from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
# from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from AiogramPackage.TGAlchemy.TGModelProdSQLite import create_table_async, drop_table_async, async_session
from AiogramPackage.TGConnectors.BOTMainClass import BOTMainClass
from AiogramPackage.TGHandlers.TGHandlerAdmin import reload_users_groups_list
import logging

from AiogramPackage.TGHandlers.TGHandlerCallback import callback_router
from AiogramPackage.TGHandlers.TGHandlerUser import user_router
from AiogramPackage.TGHandlers.TGHandlerGroup import user_group_router
from AiogramPackage.TGHandlers.TGHandlerAdmin import admin_private_router
from AiogramPackage.TGHandlers.TGHandlerStockers import stokers_private_router
from AiogramPackage.TGCommon.TGBotCommandsList import private_commands
from AiogramPackage.TGMiddleWares.TGMWDatabase import DBMiddleware
from aiogram.types import BufferedInputFile
from AiogramPackage.TGKeyboards.TGKeybInline import get_callback_btns
# from AiogramPackage.TGAlchemy.TGModelService import download_service_events_row_async

# from AiogramPackage.TGConnectors.TGMSConnector import TGMSConnector

logging.basicConfig(level=logging.INFO)
logging.info("logging starts")
bot_class = BOTMainClass()
_config = bot_class.get_main_config_json_data_sync()
logger = bot_class.logger
logger.brand = f"{os.path.basename(__file__)}"
logger.info(f"logger {os.path.basename(__file__)} starts logging")

_detect_data_dir = "data"
_detect_cap_dir = "capture"
_detect_img_dir = "images"
_detect_video_dir = "video"

# version1 set updates list
# ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]

# ver for aiogram 3.3.0
bot = Bot(token=_config.get("bot_config").get("token"), parse_mode=ParseMode.HTML)
# for v3.10
# bot = Bot(token=_config.get("bot_config").get("token"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# version1 work after filter middleware
# admin_group_router.message.middleware(CounterMiddleware())
# version2 update in outer middleware all events before filters
# dp.update.outer_middleware(CounterMiddleware())

# 0 router (handler)
dp.include_router(callback_router)
# 1 router (handler)
dp.include_router(admin_private_router)
dp.include_router(stokers_private_router)
# 2 router (handler)
dp.include_router(user_router)
# 3 router (handler)
dp.include_router(user_group_router)


bot.admins_list = [731370983]
bot.chat_group_admins_list = [731370983]
bot.fins_list = [731370983]
bot.stokers_list = [731370983]
bot.restricted_words = ['idiot']
bot.filters_dict = dict()
time_req_sec = 60  # seconds


async def on_startup(bot):
    print("bot runs")
    await reload_users_groups_list(bot)
    await bot.send_message(chat_id=bot.admins_list[0], text="Бот был перегружен, конфигурационные данные обновлены")
    asyncio.create_task(scheduler())
    # await scheduler()


async def scheduler():
    aioschedule.every(time_req_sec).seconds.do(records_sent)
    # aioschedule.every(time_req_sec).seconds.do(test_task)
    # aioschedule.every().hour.at(":40").do(test_task)
    # aioschedule.every(10).minutes.do(service_sends)

    while True:
        await aioschedule.run_pending()
        # await aioschedule.run_pending()
        await asyncio.sleep(1)


async def records_sent():
    """ loads data from Postgresql database (service table)"""
    # await asyncio.sleep(1)
    try:
        from TGConnectors.TGDBConnector import TGDBConnector
        conn = TGDBConnector()
        records_list = await conn.get_detected_obj_last_delay_async(delay=time_req_sec)

        if not records_list:
            return False
        else:
            prj_dir = os.path.dirname(os.path.dirname(__file__))
            img_dir = os.path.join(prj_dir, _detect_data_dir, _detect_cap_dir, _detect_img_dir)
            recipients_list = bot.admins_list
            # recipients_list = bot.fins_list
            for recipient_id in recipients_list:
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
                        # msg_text = f"at {img_data} detected {img_obj_count} objects"
                        # await bot.send_message(chat_id=recipient_id, text=msg_text)
                        async with aiofiles.open(img_path, mode="rb") as rec_img:
                            await bot.send_photo(chat_id=recipient_id,
                                                 photo=BufferedInputFile(file=await rec_img.read(),
                                                                         filename=f"{img_name}"),
                                                 caption=f"🎬Запись от {img_data}, длительностью {img_timelaps} секунд.\n"
                                                         f"Обнаружено {img_obj_count} {img_obj} ",
                                                 reply_markup=get_callback_btns(btns={
                                                     "🎬Скачать видео": f"download_video_{recipient_id}_{video_name}",
                                                 }),
                                                 request_timeout=100)



                except Exception as e:
                    err_msg = f"Не могу отправить данные о записях в чат {recipient_id}, ошибка:\n{e}"
                    err_msg += f"Найдено {len(records_list)} записей, ошибка:\n{e}"
                    await bot.send_message(chat_id=bot.admins_list[0], text=err_msg)
    except Exception as e:
        await bot.send_message(chat_id=bot.admins_list[0], text=f"Не могу найти обновления, ошибка:\n{e}")
    print(datetime.datetime.now(), "\nChecked DataBase")

async def on_shutdown():
    print("Бот закрылся")


async def test_task():
    print("new task run")
    return


# from https://ru.stackoverflow.com/questions/1144849/%D0%9A%D0%B0%D0%BA-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D1%82%D1%8C-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%83-aiogram-%D0%B8-schedule-%D0%BD%D0%B0-%D0%A2elegram-bot





async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    # version3
    dp.update.middleware(DBMiddleware(session_pool=async_session))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats())
    # version1 wuth list of updates
    # await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    # version2 with all uodates
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    logger.info(f"logger {os.path.basename(__file__)} starts logging")


if __name__ == '__main__':
    asyncio.run(main())
