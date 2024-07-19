from DBModule.DBMainClass import DBMainClass
import os
import asyncio
import aiofiles
import sqlite3


class DBModGenMainClass(DBMainClass):
    """ generates models from jsonfile"""
    logger_name = f"{os.path.basename(__file__)}"
    config_dir = "config"
    models_dir = "models"
    models_py_dir = "DBMod"

    def __init__(self):
        # print("test class")
        super().__init__()

    async def create_model_py_file_from_json(self, file_name: str = None):
        models_full_dir = os.path.join(self.config_dir, self.models_dir)
        from DBModule.DBConn.DBConnConfigFile import DBConnConfigFile
        json_reader = DBConnConfigFile()
        model_dict = await json_reader.get_data_from_json_async(file_name=file_name, dir_name=models_full_dir)
        # model_dict = self.prepare_model_in_json(file_name=file_name)
        fields_dict = model_dict.get("data", None)
        header = f"# !!!used SQLAlchemy 2.0.18\n" \
                 f"from sqlalchemy import create_engine, inspect\n" \
                 f"from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint\n" \
                 f"from sqlalchemy import Column, Integer, String, JSON, DateTime\n" \
                 f"from sqlalchemy import Double, BigInteger, Uuid, Boolean\n" \
                 f"from sqlalchemy.dialects.postgresql import JSONB, ARRAY, insert\n" \
                 f"from sqlalchemy.ext.mutable import MutableList\n" \
                 f"from sqlalchemy.orm import DeclarativeBase\n\n" \
                 f"from datetime import datetime\n\n" \
                 f"from DBModule.DBConn.DBConnAlchemy import DBConnAlchemy\n" \
                 f"engine = DBConnAlchemy().create_alchemy_con_sync()\n\n" \
                 f"class Base(DeclarativeBase):\n\tpass\n\n" \
                 f"class {model_dict.get('model_class')}(Base):\n" \
                 f"\t__tablename__ = '{model_dict.get('table')}'\n" \
                 f"\t# __table_args__ = (UniqueConstraint('id', name='unique_key_id'),)\n"

        body = ""
        for col_name, col_dict in fields_dict.items():
            ext_dict = col_dict.get("ext_prop", None)
            ext_str = ""
            if ext_dict:
                ext_list = [f'{key}={val}' for key, val in ext_dict.items()]
                ext_str = ", "
                ext_str = ext_str + ", ".join(ext_list)

            temp_str = f"\t{col_name} = Column({col_dict.get('type', None)}" \
                       f"{ext_str}" \
                       f", comment='{col_dict.get('descr', '')}')\n"
            body = body + temp_str

        footer = f"\ndef create_new_table():\n" \
                 f"\tBase.metadata.create_all(engine)\n\n" \
                 f"def delete_table():\n" \
                 f"\tBase.metadata.drop_all(engine)\n\n" \
                 f"if __name__ == '__main__':\n" \
                 f"\tcreate_new_table()\n" \
                 f"\t# delete_table()\n"
        up_up_dir = os.path.dirname(os.path.dirname(__file__))
        models_py_full_dir = os.path.join(up_up_dir, self.models_py_dir, f"{model_dict.get('model_class', 'name')}.py")
        async with aiofiles.open(models_py_full_dir, mode="w") as file1:
            # Writing data to a file
            await file1.write(header + body + footer)
            await file1.flush()
        return True


if __name__ == "__main__":
    connect = DBModGenMainClass()
    connect.logger.info("testing MainClass")
    asyncio.run(connect.create_model_py_file_from_json(file_name="video_capture_tg_model"))

