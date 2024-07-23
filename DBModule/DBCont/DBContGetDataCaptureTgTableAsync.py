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
    _date_col_name = "inserted_at"
    _delay = 600  # in seconds

    def __init__(self):
        super().__init__()

    async def get_last_records_from_tg_db(self, delay: int = None) -> list:
        """ return records at last 10 minutes"""
        if delay is None:
            delay = self._delay
        res_list = list()
        last_delay = datetime.datetime.now() - datetime.timedelta(seconds=delay)
        request = await self.get_filtered_data_from_table_async(table_name=self._table_name, col_name=self._date_col_name, from_val=last_delay)
        res_list.extend(request)
        print(f"have got {len(res_list)} records for last {delay}sec")
        return res_list
    async def get_all_records_from_tg_db(self) -> list:
        # return await self.get_filtered_data_from_table_async(table_name=self._table_name, col_name=self._col_name,
        #                                                      is_val=self._reaction)

        return await self.get_all_data_from_table_async(table_name=self._table_name)




def test_table_get():
    connector = DBContGetDataCaptureTgTableAsync()
    captured_list = asyncio.run(connector.get_last_records_from_tg_db(delay=60))
    for capt in captured_list:
        print(capt)


if __name__ == '__main__':
    test_table_get()
