# from https://docs.aiogram.dev/en/latest/
import asyncio
import datetime

import aioschedule
import os
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
# from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from AiogramPackage.TGAlchemy.TGModelProdSQLite import create_table_async, drop_table_async, async_session
from AiogramPackage.TGConnectors.BOTMainClass import BOTMainClass
from AiogramPackage.TGHandlers.TGHandlerAdmin import reload_admins_list
import logging

from AiogramPackage.TGHandlers.TGHandlerCallback import callback_router
from AiogramPackage.TGHandlers.TGHandlerUser import user_router
from AiogramPackage.TGHandlers.TGHandlerGroup import user_group_router
from AiogramPackage.TGHandlers.TGHandlerAdmin import admin_private_router
from AiogramPackage.TGCommon.TGBotCommandsList import private_commands
from AiogramPackage.TGMiddleWares.TGMWDatabase import DBMiddleware
# from AiogramPackage.TGAlchemy.TGModelService import download_service_events_row_async

# from AiogramPackage.TGConnectors.TGMSConnector import TGMSConnector

logging.basicConfig(level=logging.INFO)
logging.info("logging starts")
bot_class = BOTMainClass()
_config = bot_class.get_main_config_json_data_sync()
logger = bot_class.logger
logger.brand = f"{os.path.basename(__file__)}"
logger.info(f"logger {os.path.basename(__file__)} starts logging")

# version1 set updates list
# ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]

# bot = Bot(token=_config.get("bot_config").get("token"), parse_mode=ParseMode.HTML)
bot = Bot(token=_config.get("bot_config").get("token"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# version1 work after filter middleware
# admin_group_router.message.middleware(CounterMiddleware())
# version2 update in outer middleware all events before filters
# dp.update.outer_middleware(CounterMiddleware())

# 0 router (handler)
dp.include_router(callback_router)
# 1 router (handler)
dp.include_router(admin_private_router)
# 2 router (handler)
dp.include_router(user_router)
# 3 router (handler)
dp.include_router(user_group_router)

bot.admins_list = [731370983]
bot.chat_group_admins_list = [731370983]
bot.fins_list = [731370983]
bot.restricted_words = ['idiot']
bot.filters_dict = dict()
records_delay = 6000 # seconds


async def on_startup(bot):
    print("bot runs")
    await reload_admins_list(bot)
    await bot.send_message(chat_id=bot.admins_list[0], text="Бот был перегружен, конфигурационные данные обновлены")
    asyncio.create_task(scheduler())


async def on_shutdown():
    print("Бот закрылся")


# from https://ru.stackoverflow.com/questions/1144849/%D0%9A%D0%B0%D0%BA-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D1%82%D1%8C-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%83-aiogram-%D0%B8-schedule-%D0%BD%D0%B0-%D0%A2elegram-bot
async def scheduler():
    aioschedule.every(records_delay).seconds.do(records_sent)
    # aioschedule.every(10).minutes.do(service_sends)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def records_sent():
    """ loads data from Postgresql database (service table)"""
    records_list = list()
    try:
        from TGConnectors.TGDBConnector import TGDBConnector
        conn = TGDBConnector()
        records_list = await conn.get_detected_obj_last_delay_async()

        if not records_list:
            return False
        else:
            recipients_list = bot.admins_list
            # recipients_list = bot.fins_list
            for recipient_id in recipients_list:
                try:
                    for rec in records_list:
                        await bot.send_message(chat_id=recipient_id, text=f"{rec.get("position_id")}")
                except Exception as e:
                    err_msg = f"Не могу отправить данные о записях в чат {recipient_id}, ошибка:\n{e}"
                    err_msg += f"Найдено {len(records_list)} записей, ошибка:\n{e}"
                    await bot.send_message(chat_id=bot.admins_list[0], text=err_msg)
    except Exception as e:
        await bot.send_message(chat_id=bot.admins_list[0], text=f"Не могу найти обновления, ошибка:\n{e}")
    print(datetime.datetime.now(), "\nCheck the DataBase")

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
