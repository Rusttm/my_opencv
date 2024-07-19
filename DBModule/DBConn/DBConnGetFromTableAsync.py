import importlib
import os
from DBModule.DBConn.DBConnMainClass import DBConnMainClass
import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
import asyncio
from copy import copy


class DBConnGetFromTableAsync(DBConnMainClass):
    """ connector for work with tables"""
    logger_name = f"{os.path.basename(__file__)}"
    _engine = None
    _engine_async = None
    _async_session = None
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

    async def get_all_data_from_table_async(self, table_name: str = None) -> list:
        from DBModule.DBConn.DBConnGetModClass import DBConnGetModClass
        model_main_class = await DBConnGetModClass().get_model_class_by_table_name(table_name=table_name)
        await self.create_async_engine()
        res_list = list()
        async_session = sessionmaker(self._engine_async, expire_on_commit=False, class_=AsyncSession)
        try:
            async with async_session() as session:
                res = (await session.execute(select(model_main_class))).scalars().all()
            for row in res:
                obj_dict = copy(row.__dict__)
                del obj_dict["_sa_instance_state"]
                res_list.append(obj_dict)
            return res_list
        except Exception as e:
            err_msg = f"{__class__.__name__} cant read table data, error: {e}"
            print(err_msg)
            self.logger.warning(err_msg)
            return None
        finally:
            await self._engine_async.dispose()

    async def get_filtered_data_from_table_async(self, table_name: str = None,
                                                 from_val=None,
                                                 to_val=None,
                                                 col_name: str = None) -> list:
        if col_name is None:
            return await self.get_all_data_from_table_async(table_name=table_name)

        from DBModule.DBConn.DBConnGetModClass import DBConnGetModClass
        model_main_class = await DBConnGetModClass().get_model_class_by_table_name(table_name=table_name)
        # form request

        await self.create_async_engine()
        res_list = list()
        async_session = sessionmaker(self._engine_async, expire_on_commit=False, class_=AsyncSession)
        try:
            async with async_session() as session:
                filtered_request = select(model_main_class)
                if from_val:
                    filtered_request = filtered_request.filter(getattr(model_main_class, col_name) >= from_val)
                if to_val:
                    filtered_request = filtered_request.filter(getattr(model_main_class, col_name) <= to_val)

                res = (await session.execute(filtered_request)).scalars().all()
            for row in res:
                obj_dict = copy(row.__dict__)
                del obj_dict["_sa_instance_state"]
                res_list.append(obj_dict)
            return res_list
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
    # print("all records:", asyncio.run(connector.get_all_data_from_table_async("detect_model")))
    start_date = datetime.datetime(year=2024, month=7, day=18, hour=14, minute=27)
    end_date = datetime.datetime(year=2024, month=7, day=19, hour=14, minute=27)
    # filtered_data = asyncio.run(connector.get_filtered_data_from_table_async("detect_model", col_name="confident", from_val=59.0, to_val=59.0))
    filtered_data = asyncio.run(connector.get_filtered_data_from_table_async("detect_model", col_name="inserted_at", from_val=start_date))
    for val in filtered_data:
        print(val)
