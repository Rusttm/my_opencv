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
    _col_name = "react"
    _reaction = "tg"

    def __init__(self):
        super().__init__()

    async def get_new_records_from_tg_db(self) -> list:
        return await self.get_filtered_data_from_table_async(table_name=self._table_name, col_name=self._col_name, is_val=self._reaction)

    async def get_records_from_tg_db(self) -> list:
        return await self.get_filtered_data_from_table_async(table_name=self._table_name, col_name=self._col_name, is_val=self._reaction)




def test_table_get():
    connector = DBContGetDataCaptureTgTableAsync()
    captured_list = asyncio.run(connector.get_new_records_from_tg_db())
    for capt in captured_list:
        print(capt)


if __name__ == '__main__':
    test_table_get()
