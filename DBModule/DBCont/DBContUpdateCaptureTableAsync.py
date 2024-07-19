import importlib
import os
from DBModule.DBCont.DBContMainClass import DBContMainClass
import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import asyncio


class DBContUpdateCaptureTableAsync(DBContMainClass):
    """ connector for work with tables"""
    logger_name = f"{os.path.basename(__file__)}"
    _table_name = "video_capture_tg_model"

    def __init__(self):
        super().__init__()

    async def update_data_dict_capture_table_async(self, data_dict: dict) -> bool:
        try:
            from DBModule.DBConn.DBConnPut2TableAsync import DBConnPut2TableAsync
            await DBConnPut2TableAsync().put_data_dict_2table_async(model_data_dict=data_dict,
                                                                    table_name=self._table_name)
            return True
        except Exception as e:
            err_msg = f"{__class__.__name__} cant write data 2 table, error: {e}"
            print(err_msg)
            self.logger.warning(err_msg)
            return False


def test_table_insertion():
    connector = DBContUpdateCaptureTableAsync()
    today = datetime.datetime(year=2021, month=7, day=1, hour=17, minute=15)
    data_dict = dict({"created": today,
                      "closed": today,
                      "category_name": "person",
                      "confident": 56.01,
                      "time": 10.02,
                      "frame_width": 640,
                      "frame_height": 380,
                      "count": 2,
                      "path": "/temp",
                      "description": "test write",
                      "react": "tg",
                      "react_time": datetime.datetime.now()


                      })
    table_name = "video_capture_model"
    print(asyncio.run(connector.put_data_dict_2_capture_table_async(data_dict)))


if __name__ == '__main__':
    test_table_insertion()
