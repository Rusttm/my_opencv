import asyncio

from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from AiogramPackage.TGAlchemy.TGModelStock import TGModelStock as SQLModel
from AiogramPackage.TGAlchemy.TGModelStock import async_session
from sqlalchemy.types import Unicode

async def db_add_row(session: AsyncSession, data_dict: dict):
    obj = SQLModel(obj_dict=data_dict)
    session.add(obj)
    await session.commit()


async def db_get_all_rows(session: AsyncSession):
    query = select(SQLModel)
    result = await session.execute(query)
    for elem in result.scalars().all():
        print(elem.name)

    return result.scalars().all()


async def db_get_row(session: AsyncSession, model_id: str):
    query = select(SQLModel).where(SQLModel.id == model_id)
    result = await session.execute(query)
    return result.scalar()

async def db_get_prod_sum(session: AsyncSession, prod_id: str):
    href_link = str(f"https://api.moysklad.ru/api/remap/1.2/entity/product/{prod_id}?expand=supplier")
    query = select(SQLModel).filter(SQLModel.meta["href"].astext.cast(Unicode) == href_link)
    result = await session.execute(query)
    return result.scalar()

async def db_update_row(session: AsyncSession, model_id: str, data_dict: dict):
    prep_values = [f"{key}={value}" for key, value in data_dict.items()]
    query = update(SQLModel).where(SQLModel.id == model_id).values(data_dict)
    await session.execute(query)
    await session.commit()


async def db_delete_row(session: AsyncSession, row_id: str):
    query = delete(SQLModel).where(SQLModel.id == row_id)
    await session.execute(query)
    await session.commit()

if __name__ == "__main__":
    # connector = SQLModel
#     data_dict = dict({"from_chat_id": 123456, "to_chat_id": 34653456, "event_msg": "test", "event_descr": "eventer testing"})
    print(asyncio.run(db_get_prod_sum(session=async_session, prod_id="07583f34-a80d-11eb-0a80-084000094ab6")))
