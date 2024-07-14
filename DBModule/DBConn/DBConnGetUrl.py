from DBModule.DBConn.DBConnGetConfig import DBConnGetConfig
import asyncio
import os
import configparser


class DBConnGetUrl(DBConnGetConfig):
    """ loads actual configuration data from config file"""
    logger_name = f"{os.path.basename(__file__)}"
    library_key = "library"
    sqlite_key = "sqlite"

    def __init__(self):
        super().__init__()

    def get_alchemy_url(self) -> str:
        """ return full url for sqlalchemy request"""
        _url = ""
        __db_config = self.get_config()
        _db_lib = __db_config.get(self.library_key)
        if _db_lib == self.sqlite_key:
            _dir_name = __db_config.get("db_dir")
            _file_name = __db_config.get("db_file")
            _up_dir = os.path.dirname(os.path.dirname(__file__))
            _file_path = os.path.join(_up_dir, _dir_name, _file_name)
            _url = f"{_db_lib}:///{_file_path}"
        return _url

    async def get_alchemy_async_url(self) -> str:
        """ return full url for sqlalchemy request"""
        _async_url = ""
        __db_config = await self.get_config_async()
        _db_lib = __db_config.get(self.library_key)
        if _db_lib == self.sqlite_key:
            _async_lib = __db_config.get("library_async")
            _dir_name = __db_config.get("db_dir")
            _file_name = __db_config.get("db_file")
            _up_dir = os.path.dirname(os.path.dirname(__file__))
            _file_path = os.path.join(_up_dir, _dir_name, _file_name)
            _async_url = f"{_async_lib}:///{_file_path}"
        return _async_url

if __name__ == '__main__':
    connector = DBConnGetUrl()
    print(asyncio.run(connector.get_alchemy_async_url()))
    print(connector.get_alchemy_url())
