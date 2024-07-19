import asyncio

from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from AiogramPackage.TGAlchemy.TGModelEvent import TGModelEvent

async def db_add_event(session: AsyncSession, data_dict: dict):
    obj = TGModelEvent(
        from_chat_id=data_dict.get("from_chat_id"),
        to_chat_id=data_dict.get("to_chat_id"),
        event_msg=data_dict.get("event_msg"),
        event_descr=data_dict.get("event_descr"),
        event_img=data_dict.get("event_img")
    )
    session.add(obj)
    await session.commit()

async def db_get_events(session: AsyncSession):
    query = select(TGModelEvent)
    result = await session.execute(query)
    return result.scalars().all()

async def db_get_event(session: AsyncSession, position_id: int):
    query = select(TGModelEvent).where(TGModelEvent.position_id == position_id)
    result = await session.execute(query)
    return result.scalar()

async def db_update_event(session: AsyncSession, position_id: int, data_dict: dict):
    query = update(TGModelEvent).where(TGModelEvent.position_id == position_id).values(
        from_chat_id=data_dict.get("from_chat_id"),
        to_chat_id=data_dict.get("to_chat_id"),
        event_msg=data_dict.get("event_msg"),
        event_descr=data_dict.get("event_descr"),
        event_img=data_dict.get("event_img")
    )
    result = await session.execute(query)
    await session.commit()

async def db_delete_event(session: AsyncSession, position_id: int):
    query = delete(TGModelEvent).where(TGModelEvent.position_id == position_id)
    await session.execute(query)
    await session.commit()

# if __name__ == "__main__":
#     connector = TGModelEvent()
#     data_dict = dict({"from_chat_id": 123456, "to_chat_id": 34653456, "event_msg": "test", "event_descr": "eventer testing"})
#     asyncio.run(db_add_event(session=AsyncSession(), data=data_dict))