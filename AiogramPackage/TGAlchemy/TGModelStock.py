# !!!used SQLAlchemy 2.0.18
from sqlalchemy import create_engine, inspect
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy import Double, BigInteger, Uuid, Boolean, select
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, insert
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, aliased

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import asyncio
from sqlalchemy.types import Unicode

from AiogramPackage.TGAlchemy.TGConnSQL import TGConnSQL

__url = TGConnSQL().get_sql_url()
engine = create_async_engine(__url)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class TGModelStock(Base):
    __tablename__ = 'stockall_model'
    # __table_args__ = (UniqueConstraint('id', name='unique_key_id'),)
    position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False,
                         comment='Обязательное поле для всех таблиц, автоповышение')
    article = Column(String(255), comment='Артикул')
    code = Column(String(255), unique=True, nullable=False, comment='Код Обязательное при ответе')
    externalCode = Column(String(255),
                          comment='Внешний код сущности, по которой выводится остаток Обязательное при ответе')
    folder = Column(JSONB, comment='Группа Товара/Модификации/Cерии. Подробнее тут Обязательное при ответе')
    image = Column(JSONB, comment='Метаданные изображения Товара/Модификации/Серии')
    inTransit = Column(Double, comment='Ожидание Обязательное при ответе')
    meta = Column(JSONB,
                  comment='Метаданные Товара/Модификации/Серии по которой выдается остаток Обязательное при ответе')
    name = Column(String(255), comment='Наименование Обязательное при ответе')
    price = Column(Double, comment='Себестоимость')
    quantity = Column(Double, comment='Доступно Обязательное при ответе')
    reserve = Column(Double, comment='Резерв Обязательное при ответе')
    salePrice = Column(Double, comment='Цена продажи')
    stock = Column(Double, comment='Остаток Обязательное при ответе')
    stockDays = Column(BigInteger, comment='Количество дней на складе Обязательное при ответе')
    uom = Column(JSONB, comment='Единица измерения. Подробнее тут Обязательное при ответе')


async def create_table_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_table_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def insert_new_row(ins_dict):
    pos_obj = TGModelStock(ins_dict)
    async with async_session.begin() as s:
        s.add(pos_obj)


async def get_stock_row(pos_id):
    href_link = str(f"https://api.moysklad.ru/api/remap/1.2/entity/product/{pos_id}?expand=supplier")
    # pos_dict = dict({
    #     "href": f"https://api.moysklad.ru/api/remap/1.2/entity/product/{pos_id}?expand=supplier",
    #     "type": "product",
    #     "uuidHref": f"https://online.moysklad.ru/app/#good/edit?id={pos_id}",
    #     "mediaType": "application/json",
    #     "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata"})

    async with async_session() as session:
        # query = select(TGModelStock).where(TGModelStock.meta.contains(pos_id))
        """ 
        SELECT * FROM public.stockall_model 
        where (meta->'href')::jsonb ? 'https://api.moysklad.ru/api/remap/1.2/entity/product/0ef6dd2b-7f63-11ec-0a80-0e14000c64ed?expand=supplier'
        """

        query = select(TGModelStock).filter(TGModelStock.meta["href"].astext.cast(Unicode) == href_link)
        result = await session.execute(query)
    return result.scalar()


if __name__ == '__main__':
    # create_new_table_sync()
    # asyncio.run(create_table_async())
    # asyncio.run(drop_table_async())
    prod_obj = asyncio.run(get_stock_row(pos_id="684f9da4-5741-11eb-0a80-06ec00afaeba"))
    print(prod_obj.name)
