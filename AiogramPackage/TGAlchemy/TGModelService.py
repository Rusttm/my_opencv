# !!!used SQLAlchemy 2.0.18
import datetime

from sqlalchemy import create_engine, inspect
# from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy import BigInteger, Boolean
from sqlalchemy.dialects.postgresql import JSONB
# from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import asyncio
from sqlalchemy.types import Unicode
from sqlalchemy import select, update, desc, or_

from AiogramPackage.TGAlchemy.TGConnSQL import TGConnSQL

__url = TGConnSQL().get_sql_url()
engine = create_async_engine(__url)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class TGModelService(Base):
    __tablename__ = 'pgsql_service_model'
    position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False,
                         comment='Обязательное поле для всех таблиц, автоповышение')
    event_active = Column(Boolean, nullable=False, default=False,
                          comment='требуется ли реакция на сообщение? активно ли оно?')
    event_level = Column(BigInteger, nullable=False, default=10,
                         comment='уровень события: как в логере 0-notset, 10-debug, 20-info, 30-warning, 40-error, 50-critical')
    event_time = Column(DateTime, comment='время события ')
    event_name = Column(String(255), comment='короткое название события')
    event_from = Column(String(255), comment='источник события')
    event_table = Column(String(255), comment='в какой таблице произошло событие?')
    event_to = Column(String(255), nullable=False, default='Telegram', comment='для кого предназначено событие?')
    event_req = Column(String(255), comment='что требуется сделать?')
    event_descr = Column(String(4096), comment='подробное описание события')
    event_reaction = Column(String(4096), comment='ответ -что сделано на событие')
    event_reaction_time = Column(DateTime, comment='время, когда на событие среагировали')
    event_msg = Column(JSONB, comment='сообщение для SocketClient, отправленное событием в виде словаря')
    event_period_start = Column(DateTime, comment='для указания времени обновления С')
    event_period_end = Column(DateTime, comment='для указания времени обновления ПО')


async def create_table_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_table_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def update_row_async(position_id):
    now_time = datetime.datetime.now()
    values_dict = dict({"event_reaction": "sent_telegram", "event_reaction_time": now_time})
    async with async_session.begin() as session:
        query = update(TGModelService).where(TGModelService.position_id == position_id).values(values_dict)
        result = await session.execute(query)
    return result


async def get_service_all_rows_async():
    async with async_session() as session:
        query = select(TGModelService)
        result = await session.execute(query)
    return result.scalars().all()


async def get_service_filtered_rows_async():
    async with async_session() as session:
        query = select(TGModelService).filter(TGModelService.event_to.contains("Telegram")).where(TGModelService.event_reaction_time.is_(None)).order_by(desc(TGModelService.position_id))
        result = await session.execute(query)
    return result.scalars().all()


async def download_service_events_row_async() -> str :
    res_str = str("Таблицы:\n")
    try:
        new_event_list = await get_service_filtered_rows_async()
        if new_event_list:
            for new_event in new_event_list:
                event_id = new_event.position_id
                event_descr = new_event.event_descr
                res_str += f"{new_event.event_table}:{new_event.event_time}\n"
                await update_row_async(event_id)
                print(new_event.position_id)
        return res_str
    except Exception as e:
        return f"Не могу найти обновления в базе, ошибка:\n{e}"


if __name__ == '__main__':
    # create_new_table_sync()
    # asyncio.run(create_table_async())
    # asyncio.run(drop_table_async())
    event_list = asyncio.run(get_service_filtered_rows_async())
    for event in event_list:
        print(event.position_id)
    # asyncio.run(update_row_async(position_id=29052))
    # print(asyncio.run(download_service_events_row_async()))
