import importlib
import os
from DBModule.DBCont.DBContMainClass import DBContMainClass
from DBModule.DBConn.DBConnGetFromTableAsync import DBConnGetFromTableAsync
import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import asyncio


class DBContGetDataCaptureTgTableAsync(DBContMainClass, DBConnGetFromTableAsync):
    """ connector for work with tables"""
    logger_name = f"{os.path.basename(__file__)}"
    _table_name = "video_capture_tg_model"

    def __init__(self):
        super().__init__()



def test_table_get():
    connector = DBContGetDataCaptureTgTableAsync()
    table_name = "video_capture_model"
    print(asyncio.run(connector.get_all_data_from_table_async(table_name=table_name)))


if __name__ == '__main__':
    test_table_get()
