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


    def create_sync_engine(self):
        try:
            from DBModule.DBConn.DBConnAlchemy import DBConnAlchemy
            self._engine = DBConnAlchemy().create_alchemy_con_sync()
            return True
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create new engine error: {e}")
            return False

    async def create_async_engine(self):
        try:
            from DBModule.DBConn.DBConnAlchemy import DBConnAlchemy
            self._engine_async = await DBConnAlchemy().create_alchemy_con_async()
            return True
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create new engine error: {e}")
            return False

    async def create_async_session(self) -> object:
        try:
            await self.create_async_engine()
            self._async_session = sessionmaker(self._engine_async, expire_on_commit=False, class_=AsyncSession)
            return self._async_session
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create new async engine session error: {e}")
            return None

    async def get_all_tables_list_async(self) -> list:
        """ Inspection on an AsyncEngine is currently not supported.
        Please obtain a connection then use ``conn.run_sync``"""
        await self.create_async_engine()

        def get_all_tables_list(conn):
            inspector = sqlalchemy.inspect(conn)
            return inspector.get_table_names()

        async with self._engine_async.begin() as async_conn:
            table_names = await async_conn.run_sync(get_all_tables_list)

        return table_names

    async def check_table_exist_async(self, table_name: str = None):
        tables_list = await self.get_all_tables_list_async()
        return table_name in tables_list

    async def put_data_dict_2table_async(self, model_data_dict: dict = None, model_name: str = None):
        inserted_rows_num = 0
        try:
            module_import = importlib.import_module(f"{self.model_module}.{model_name}")
            model_main_class = getattr(module_import, model_name)
            await self.create_async_engine()
            model_new_obj = model_main_class(**model_data_dict)
            Session = sessionmaker(bind=self._engine)
            session = Session()
            # check is presence position?
            session.add(model_new_obj)
            inserted_rows_num += 1
            session.commit()

        except Exception as e:
            err_str = f"{__class__.__name__} balance table insertion interrupt, error {e}"
            print(err_str)
            self.logger.error(err_str)

        return dict({"inserted": inserted_rows_num, "updated": 0})


def test_table_insertion():
    connector = DBConnPut2TableAsync()
    # print(connector.create_engine())
    print("tables list:", asyncio.run(connector.get_all_tables_list_async()))
    print("'detect_model' in tables list:", asyncio.run(connector.check_table_exist_async("detect_model")))
    today = datetime.datetime.now()
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
    model_class_name = "DBModDetect"
    connector.put_data_dict_2table_async(model_data_dict=data_dict, model_name=model_class_name)

    # how to create class from classname
    module = importlib.import_module("DBModule.DBMod.DBModDetect")
    model_class = getattr(module, model_class_name)
    new_model_obj = model_class(**data_dict)
    print(new_model_obj.description)


if __name__ == '__main__':
    connector = DBConnPut2TableAsync()
    print("tables list:", asyncio.run(connector.get_all_tables_list_async()))
    print("'detect_model' in tables list:", asyncio.run(connector.check_table_exist_async("detect_model")))
