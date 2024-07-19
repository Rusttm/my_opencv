from DBModule.DBCont.DBContGetDataCaptureTgTableAsync import DBContGetDataCaptureTgTableAsync
import os
import logging
import asyncio

class TGDBConnector(DBContGetDataCaptureTgTableAsync):
    logger_name = f"{os.path.basename(__file__)}"
    _delay = 6000 # seconds

    def __init__(self):
        super().__init__()

    async def get_detected_obj_last_delay_async(self):
        res_str = list()
        try:
            detected_objs_list = await self.get_last_records_from_tg_db(delay=self._delay)
        except Exception as e:
            res_str = f"{__class__.__name__} Cant get last records in db, Ошибка: \n {e}"
            self.logger.warning(res_str)
            logging.warning(res_str)
        else:
            res_str.extend(detected_objs_list)
        return res_str


if __name__ == '__main__':
    connector = TGDBConnector()
    print(asyncio.run(connector.get_detected_obj_last_delay_async()))
