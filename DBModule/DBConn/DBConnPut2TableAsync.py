import importlib
import os
from DBModule.DBConn.DBConnMainClass import DBConnMainClass
import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import asyncio


class DBConnPut2TableAsync(DBConnMainClass):
    """ connector for work with tables"""
    logger_name = f"{os.path.basename(__file__)}"
    _engine = None
    _engine_async = None
    _async_session = None
    __url = None
    model_module = "DBModule.DBMod"

    def __init__(self):
        super().__init__()

    async def create_async_engine(self):
        try:
            from DBModule.DBConn.DBConnAlchemy import DBConnAlchemy
            self._engine_async = await DBConnAlchemy().create_alchemy_con_async()
            return True
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create new engine error: {e}")
            return False

    async def put_data_dict_2table_async(self, model_data_dict: dict = None, table_name: str = None):
        inserted_rows_num = 0
        try:
            from DBModule.DBConn.DBConnGetModClass import DBConnGetModClass
            model_main_class = await DBConnGetModClass().get_model_class_by_table_name(table_name=table_name)
            await self.create_async_engine()
            model_new_obj = model_main_class(**model_data_dict)
            async_session = sessionmaker(self._engine_async, expire_on_commit=False, class_=AsyncSession)
            try:
                async with async_session() as session:
                    async with session.begin():
                        # session.add_all(model_new_obj)
                        session.add(model_new_obj)
                return True
            except Exception as e:
                err_msg = f"{__class__.__name__} cant write data 2 table, error: {e}"
                print(err_msg)
                self.logger.warning(err_msg)
                return None
            finally:
                await self._engine_async.dispose()

        except Exception as e:
            err_str = f"{__class__.__name__} balance table insertion interrupt, error {e}"
            print(err_str)
            self.logger.error(err_str)

        return dict({"inserted": inserted_rows_num, "updated": 0})


def test_table_insertion():
    connector = DBConnPut2TableAsync()
    today = datetime.datetime(year=2023, month=7, day=1, hour=17, minute=15)
    data_dict = dict({"created": today,
                      "category_name": "person",
                      "confident": 56.01,
                      "box_x1": 10.02,
                      "box_y1": 15.03,
                      "box_x2": 20.04,
                      "box_y2": 25.05,
                      "frame_width": 640,
                      "frame_height": 380,
                      "path": "/temp",
                      "description": "test write"
                      })
    table_name = "detect_model"
    print(asyncio.run(connector.put_data_dict_2table_async(model_data_dict=data_dict, table_name=table_name)))


if __name__ == '__main__':
    test_table_insertion()
