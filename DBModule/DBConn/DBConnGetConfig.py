from DBModule.DBConn.DBConnConfigFile import DBConnConfigFile
import asyncio
import json
import os
import configparser


class DBConnGetConfig(DBConnConfigFile):
    """ loads actual configuration data from config file"""
    logger_name = f"{os.path.basename(__file__)}"
    config_file_name = "db_config.json"
    config_key = "databases_configurations"
    db_key = "main_database_type"

    def __init__(self):
        super().__init__()

    async def get_config(self) -> dict:
        """ return full dictionary for actual configuration"""
        try:
            __full_conf = await self.get_data_from_json(file_name=self.config_file_name)
            __db_current_name = __full_conf.get(self.db_key)
            if __db_current_name is None:
                raise KeyError(f"requested keyword in json file should be {self.db_key}")
            __current_config = __full_conf.get(self.config_key).get(__db_current_name)
            if __current_config is None: raise KeyError(f"unknown keywords {__db_current_name}")
            # __current_config = __full_conf[self.config_key][__db_current_name]
        except Exception as e:
            err_msg = f"module {__class__.__name__} cant reads actual configuration, error: {e}"
            print(err_msg)
            self.logger.error(err_msg)
            return None
        else:
            return __current_config


if __name__ == '__main__':
    connector = DBConnGetConfig()
    print(asyncio.run(connector.get_config()))

