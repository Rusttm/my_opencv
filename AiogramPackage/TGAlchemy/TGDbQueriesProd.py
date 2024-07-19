import asyncio

from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from AiogramPackage.TGAlchemy.TGModelProd import TGModelProd



async def db_add_prod(session: AsyncSession, data_dict: dict):
    obj = TGModelProd(obj_dict=data_dict)
    session.add(obj)
    await session.commit()


async def db_get_prods(session: AsyncSession):
    query = select(TGModelProd)
    result = await session.execute(query)
    for elem in result.scalars().all():
        print(elem.name)
    return result.scalars().all()


async def db_get_prod(session: AsyncSession, prod_id: str):
    query = select(TGModelProd).where(TGModelProd.id == prod_id)
    result = await session.execute(query)
    return result.scalar()


async def db_update_prod(session: AsyncSession, prod_id: str, data_dict: dict):
    prep_values = [f"{key}={value}" for key, value in data_dict.items()]
    query = update(TGModelProd).where(TGModelProd.id == prod_id).values(data_dict)
    result = await session.execute(query)
    await session.commit()


async def db_delete_prod(session: AsyncSession, prod_id: str):
    query = delete(TGModelProd).where(TGModelProd.id == prod_id)
    await session.execute(query)
    await session.commit()

# if __name__ == "__main__":
    connector = TGModelProd()
#     data_dict = dict({"from_chat_id": 123456, "to_chat_id": 34653456, "event_msg": "test", "event_descr": "eventer testing"})
    print(asyncio.run(db_get_prod(session=AsyncSession(), prod_id="07583f34-a80d-11eb-0a80-084000094ab6")))
