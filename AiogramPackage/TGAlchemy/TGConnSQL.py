import asyncio

from AiogramPackage.TGConnectors.BOTMainClass import BOTMainClass
import os
class TGConnSQL(BOTMainClass):
    logger_name = f"{os.path.basename(__file__)}"
    _main_key = "bot_config"
    _sql_key = "sql_config"
    # _type_sql_key = "sqlite_config"
    _type_sql_key = "pgsql_config"
    _config_dir_name = "config"
    _config_file_name = "bot_main_config.json"
    _db_dir_name = "data_sql"
    # _db_file_name = "sql.db"
    _module_config: dict = None
    __url: str = None
    def __init__(self):
        super().__init__()

    def get_sql_url(self):
        try:
            self._module_config = self.get_main_config_json_data_sync(self._config_dir_name, self._config_file_name)
            sql_config_dict = self._module_config.get(self._main_key).get(self._sql_key).get(self._type_sql_key)
            init_modules = sql_config_dict.get("init_modules", '')
            host = sql_config_dict.get('url', '')
            port = sql_config_dict.get('port', '')
            database = sql_config_dict.get('db_name', '')
            user = sql_config_dict.get('user', '')
            password = sql_config_dict.get('user_pass', '')
            self.logger.debug(f"{__class__.__name__} read data from config")
            if self._type_sql_key == "sqlite_config":
                up_file_dir = os.path.dirname(os.path.dirname(__file__))
                db_path = os.path.join(up_file_dir, self._db_dir_name, database)
                self.__url = f"{init_modules}:///{db_path}"
            else:
                self.__url = f"{init_modules}://{user}:{password}@{host}:{port}/{database}"
            # self.__url_no_db = f"postgresql://{user}:{password}@{host},{port}/"
        except Exception as e:
            print(f"configuration data not loaded {e}")
            self.logger.error(f"{__class__.__name__} can't create connector in SQLAlchemy! {e}")
        return self.__url

if __name__ == "__main__":
    connector = TGConnSQL()
    print(connector.get_sql_url())