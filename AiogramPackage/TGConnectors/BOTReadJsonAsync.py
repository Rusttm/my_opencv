import json
import os
import re
import aiofiles
import asyncio


class BOTReadJsonAsync(object):
    """read and return data from json file
    configurator initialised"""
    logger_name = f"{os.path.basename(__file__)}"
    _config_dir_name = "config"
    _config_file_name = "bot_main_config.json"
    _config_data: dict = None

    def __init__(self):
        super().__init__()
        # self._config_data = self.get_config_json_data_sync(self._conf_dir_name, self._config_file_name)

    def get_json_data_sync(self, dir_name, file_name) -> dict:
        """ extract data from json file return dict """
        data = dict()
        try:
            up_file_dir = os.path.dirname(os.path.dirname(__file__))
            if not re.search('json', file_name):
                file_name += '.json'
            CONF_FILE_PATH = os.path.join(up_file_dir, dir_name, file_name)
            with open(CONF_FILE_PATH, 'r') as json_file:
                json_data = json_file.read()
            data = json.loads(json_data)
            # self.logger.debug(f"{__class__.__name__} got data from json file")
        except Exception as e:
            msg = f"{__class__.__name__} can't read json file {file_name}!, Error:\n{e}"
            print(msg)
            # self.logger.error(f"{__class__.__name__} can't read json file!{e}")
        return data

    async def get_json_data_async(self, dir_name, file_name) -> dict:
        """ extract data from json file return dict """
        data = dict()
        try:
            up_file_dir = os.path.dirname(os.path.dirname(__file__))
            if not re.search('json', file_name):
                file_name += '.json'
            CONF_FILE_PATH = os.path.join(up_file_dir, dir_name, file_name)
            async with aiofiles.open(CONF_FILE_PATH, 'r') as json_file:
                json_data = await json_file.read()
            data = json.loads(json_data)
            # self.logger.debug(f"{__class__.__name__} got data from json file")
        except Exception as e:
            msg = f"{__class__.__name__} can't read json file {file_name}!, Error:\n{e}"
            print(msg)
        return data

    def get_main_config_json_data_sync(self, config_dir_name=None, config_file_name=None) -> dict:
        if not config_file_name:
            config_file_name = self._config_file_name
        if not config_dir_name:
            config_dir_name = self._config_dir_name
        self._config_data = self.get_json_data_sync(dir_name=config_dir_name, file_name=config_file_name)
        return self._config_data

    async def get_main_config_json_data_async(self, config_dir_name=None, config_file_name=None) -> dict:
        if not config_file_name:
            config_file_name = self._config_file_name
        if not config_dir_name:
            config_dir_name = self._config_dir_name
        self._config_data = await self.get_json_data_async(dir_name=config_dir_name, file_name=config_file_name)
        return self._config_data

if __name__ == '__main__':
    # connector = MSReadJsonAsync()
    # print(connector.get_config_json_data_sync(file_name='url_money.json'))
    # connector2 = GSReadJsonAsync(dir_name="data", file_name="spread_sheet_metadata.json")
    # print(asyncio.run(connector2.get_json_data_async()))
    connector3 = BOTReadJsonAsync()
    print(asyncio.run(connector3.get_main_config_json_data_async()))
    # print(connector3.get_config_json_data_sync())
