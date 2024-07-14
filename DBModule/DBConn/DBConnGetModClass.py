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
from copy import copy


class DBConnGetModClass(DBConnMainClass):
    """ connector for work with tables"""
    logger_name = f"{os.path.basename(__file__)}"
    _model_module = "DBModule.DBMod"
    _config_dir = "config"
    _models_dir = "models"
    _model_key = "model_class"

    def __init__(self):
        super().__init__()

    async def get_model_class_by_table_name(self, table_name) -> object:
        try:
            from DBModule.DBConn.DBConnConfigFile import DBConnConfigFile
            models_full_dir = os.path.join(self._config_dir, self._models_dir)
            table_config = await DBConnConfigFile().get_data_from_json_async(table_name, models_full_dir)
            table_model_class = table_config.get(self._model_key)
            module_import = importlib.import_module(f"{self._model_module}.{table_model_class}")
            model_main_class = getattr(module_import, table_model_class)
            return model_main_class
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create model class, error: {e}")
            return None




if __name__ == '__main__':
    connector = DBConnGetModClass()
    print("cofiguration:", asyncio.run(connector.get_model_class_by_table_name("detect_model")))
