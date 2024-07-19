# !!!used SQLAlchemy 2.0.18
from sqlalchemy import Integer, String, JSON, DateTime, func, ARRAY, PickleType, Text
from sqlalchemy import Double, BigInteger, Uuid, Boolean, UUID, Column, TEXT
# from sqlalchemy.dialects.postgresql import JSONB, ARRAY, insert
from sqlalchemy.dialects.sqlite import JSON, DATETIME
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import asyncio
import datetime

from AiogramPackage.TGAlchemy.TGConnSQL import TGConnSQL

__url = TGConnSQL().get_sql_url()
engine = create_async_engine(__url, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class TGModelEvent(Base):
    """ this model for event record in telegram"""
    def __init__(self, obj_dict: dict = None):
        super().__init__()
        if obj_dict:
            for key, value in obj_dict.items():
                setattr(self, key, value)
    __tablename__ = 'event_model'
    position_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    from_chat_id: Mapped[int] = mapped_column(Integer, comment='Номер чата написавшего', nullable=False)
    to_chat_id: Mapped[int] = mapped_column(Integer, comment='Номер текущего чата')
    event_msg: Mapped[str] = mapped_column(Text)
    event_descr: Mapped[str] = mapped_column(Text)
    event_img: Mapped[str] = mapped_column(String(255))


async def create_table_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_table_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def insert_new_row(event_dict=None):
    if not event_dict:
        event_dict = dict({"event_msg": "test",
                           "event_descr": "test descr",
                           "from_chat_id": 12345,
                           "to_chat_id": 54321,
                           "event_img": "test"})
    prog_obj = TGModelEvent(
        from_chat_id=event_dict.get("from_chat_id"),
        to_chat_id=event_dict.get("to_chat_id"),
        event_msg=event_dict.get("event_msg"),
        event_descr=event_dict.get("event_descr"),
        event_img=event_dict.get("event_img")
    )
    async with async_session.begin() as s:
        s.add(prog_obj)


if __name__ == '__main__':
    # create_new_table_sync()
    # asyncio.run(create_table_async())
    # asyncio.run(drop_table_async())
    asyncio.run(insert_new_row())


