from DBModule.DBConn.DBConnGetUrl import DBConnGetUrl
import asyncio
import os
from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


class DBConnAl(DBConnGetUrl):
    """ loads actual configuration data from config file"""
    logger_name = f"{os.path.basename(__file__)}"
    library_key = "library"
    sqlite_key = "sqlite"

    def __init__(self):
        super().__init__()

    async def create_alchemy_con_async(self):
        """ return full url for sqlalchemy request"""
        async_url = await self.get_alchemy_async_url()
        engine = create_async_engine(async_url)
        return async_url

    def create_alchemy_con_sync(self):
        """ return full url for sqlalchemy request"""
        _url = asyncio.run(self.get_alchemy_url())
        engine = create_engine(_url)
        return engine


if __name__ == '__main__':
    connector = DBConnAl()
    print(asyncio.run(connector.create_alchemy_con_async()))
