import importlib
import os
from DBModule.DBConn.DBConnMainClass import DBConnMainClass
import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
import asyncio
import pandas as pd

class DBConnGetFromTableAsync(DBConnMainClass):
    """ connector for work with tables"""
    logger_name = f"{os.path.basename(__file__)}"
    _engine = None
    _engine_async = None
    _async_session = None
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

    # async def create_async_session(self) -> object:
    #     try:
    #         await self.create_async_engine()
    #         self._async_session = sessionmaker(self._engine_async, expire_on_commit=False, class_=AsyncSession)
    #         return self._async_session
    #     except Exception as e:
    #         print(e)
    #         self.logger.warning(f"{__class__.__name__} cant create new async engine session error: {e}")
    #         return None

    async def get_all_tables_list_async(self) -> list:
        """ Inspection on an AsyncEngine is currently not supported.
        Please obtain a connection then use ``conn.run_sync``"""
        await self.create_async_engine()

        def get_all_tables_list(conn):
            inspector = sqlalchemy.inspect(conn)
            return inspector.get_table_names()

        async with self._engine_async.begin() as async_conn:
            table_names = await async_conn.run_sync(get_all_tables_list)
        await self._engine_async.dispose()
        return table_names

    async def check_table_exist_async(self, table_name: str = None):
        tables_list = await self.get_all_tables_list_async()
        return table_name in tables_list

    def get_model_class(self, model_name):
        module_import = importlib.import_module(f"{self.model_module}.{model_name}")
        return getattr(module_import, model_name)

    async def get_all_data_from_table_async(self, model_name: str = None):
        model_main_class = self.get_model_class(model_name)
        await self.create_async_engine()
        res = None
        async_session = sessionmaker(self._engine_async, expire_on_commit=False, class_=AsyncSession)
        try:
            async with async_session() as session:
                res = (await session.execute(select(model_main_class))).scalars().all()
            # list_of_dicts = [dict((key, value) for key, value in row.items()) for row in res]
            # print(f"{list_of_dicts}")
            for x in res:
                print(x.__dict__)
                # print(vars(x))
                # print(x._asdict())
            return res
        except Exception as e:
            err_msg = f"{__class__.__name__} cant read table data, error: {e}"
            print(err_msg)
            self.logger.warning(err_msg)
            return None
        finally:
            await self._engine_async.dispose()



if __name__ == '__main__':
    connector = DBConnGetFromTableAsync()
    print("tables list:", asyncio.run(connector.get_all_tables_list_async()))
    print("'detect_model' in tables list:", asyncio.run(connector.check_table_exist_async("detect_model")))
    print("all records:", asyncio.run(connector.get_all_data_from_table_async("DBModDetect")))