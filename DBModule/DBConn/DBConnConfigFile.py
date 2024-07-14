import pickle

from DBModule.DBConn.DBConnMainClass import DBConnMainClass
import json
import os
import asyncio
import aiofiles
import configparser


class DBConnConfigFile(DBConnMainClass):
    """ configfile connector
    gets data from json file in ./data/db_config.json"""
    logger_name = f"{os.path.basename(__file__)}"
    dir_name = "config"

    def __init__(self):
        super().__init__()

    async def get_json_files_list(self, dir_name: str = None):
        """ gets files .json in self.dir_name"""
        if dir_name is not None:
            self.dir_name = dir_name
        up_up_dir = os.path.dirname(os.path.dirname(__file__))
        files_list = os.listdir(os.path.join(up_up_dir, self.dir_name))
        json_files_list = [file for file in files_list if file.endswith(".json")]
        return json_files_list

    async def get_all_dicts_in_dir(self, dir_name: str = None) -> list:
        """ """
        if dir_name is not None:
            self.dir_name = dir_name
        json_files_list = self.get_json_files_list(dir_name=self.dir_name)
        result = list()
        for file_name in json_files_list:
            result.append(file_name)
        return result

    async def get_data_from_json(self, file_name=None, dir_name=None) -> dict:
        """ takes data from json file """
        if dir_name is not None:
            self.dir_name = dir_name
        if file_name:
            file_name_type = file_name.split(".")[-1]
            if file_name_type != "json":
                file_name += ".json"
        try:
            up_up_dir = os.path.dirname(os.path.dirname(__file__))
            json_file = os.path.join(up_up_dir, self.dir_name, file_name)
            async with aiofiles.open(json_file, mode='r') as jf:
                data = await jf.read()
            return dict(json.loads(data))
        except FileNotFoundError as e:
            self.logger.debug(f"File not found error json file: {e}")
            return None
        except json.decoder.JSONDecodeError as e:
            err_str = f"{__class__.__name__} cant load data from json file {file_name}, error: {e}"
            print(err_str)
            self.logger.debug(err_str)
            return None


if __name__ == '__main__':
    connector = DBConnConfigFile()
    print(asyncio.run(connector.get_json_files_list()))
    print(asyncio.run(connector.get_data_from_json("../config/db_config.json")))
