# !!!used SQLAlchemy 2.0.18
from sqlalchemy import create_engine, inspect
from sqlalchemy import Integer, String, JSON, DateTime, func, ARRAY, PickleType
from sqlalchemy import Double, BigInteger, Uuid, Boolean, UUID, Column
# from sqlalchemy.dialects.postgresql import JSONB, ARRAY, insert
from sqlalchemy.dialects.sqlite import JSON, DATETIME
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import asyncio
import sqlite3
import aiosqlite

from AiogramPackage.TGAlchemy.TGConnSQL import TGConnSQL

__url = TGConnSQL().get_sql_url()
engine = create_async_engine(__url)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    created: Mapped[DateTime] = Column(DateTime, default=func.now())
    updated: Mapped[DateTime] = Column(DateTime, default=func.now(), onupdate=func.now())


class TGModelProd(Base):
    def __init__(self, obj_dict: dict = None):
        super().__init__()
        if obj_dict:
            for k, v in obj_dict.items():
                setattr(self, k, v)

    __tablename__ = 'product_model'
    position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False,
                                comment='Обязательное поле для всех таблиц, автоповышение')
    # accountId = Column(Uuid, comment='ID учетной записи Обязательное при ответе Только для чтения')
    accountId = Column(String(255), comment='ID учетной записи Обязательное при ответе Только для чтения')

    alcoholic = Column(JSON, comment='Объект, содержащий поля алкогольной продукции. Подробнее тут')
    archived = Column(Boolean, comment='Добавлен ли Товар в архив Обязательное при ответе')
    article = Column(String(255), comment='Артикул')
    # attributes = Column(MutableList.as_mutable(ARRAY(JSON)), comment='Коллекция доп. полей')
    # barcodes = Column(MutableList.as_mutable(ARRAY(JSON)), comment='Штрихкоды Комплекта. Подробнее тут')
    attributes = Column(MutableList.as_mutable(PickleType()), comment='Коллекция доп. полей')
    barcodes = Column(MutableList.as_mutable(PickleType()), comment='Штрихкоды Комплекта. Подробнее тут')
    buyPrice = Column(JSON, comment='Закупочная цена. Подробнее тут')
    code = Column(String(255), comment='Код Товара')
    country = Column(JSON, comment='Метаданные Страны Expand')
    description = Column(String(4096), comment='Описание Товара')
    discountProhibited = Column(Boolean, comment='Признак запрета скидок Обязательное при ответе')
    effectiveVat = Column(BigInteger, comment='Реальный НДС % Только для чтения')
    effectiveVatEnabled = Column(Boolean,
                                        comment='Дополнительный признак для определения разграничения реального НДС = 0 или "без НДС". (effectiveVat = 0, effectiveVatEnabled = False) -> "без НДС", (effectiveVat = 0, effectiveVatEnabled = True) -> 0%. Только для чтения')
    externalCode = Column(String(255), comment='Внешний код Товара Обязательное при ответе')
    files = Column(JSON, comment='Метаданные массива Файлов (Максимальное количество файлов - 100) Expand')
    group = Column(JSON, comment='Метаданные отдела сотрудника Обязательное при ответе Expand')

    # id = Column(Uuid, unique=True, nullable=False, comment='ID Товара Обязательное при ответе Только для чтения')
    id = Column(String(255), unique=True, nullable=False, comment='ID Товара Обязательное при ответе Только для чтения')

    images = Column(JSON,
                           comment='Массив метаданных Изображений (Максимальное количество изображений - 10) Expand')

    isSerialTrackable = Column(Boolean,
                                      comment='Учет по серийным номерам. Данная отметка не сочетается с признаками weighed, alcoholic, ppeType, trackingType, onTap.')
    meta = Column(JSON, comment='Метаданные Товара Обязательное при ответе')
    minPrice = Column(JSON, comment='Минимальная цена. Подробнее тут')
    minimumBalance = Column(BigInteger, comment='Неснижаемый остаток')
    name = Column(String(255), comment='Наименование Товара Обязательное при ответе Необходимо при создании')
    owner = Column(JSON, comment='Метаданные владельца (Сотрудника) Expand')
    # packs = Column(MutableList.as_mutable(ARRAY(JSON)), comment='Упаковки Товара. Подробнее тут')
    packs = Column(MutableList.as_mutable(PickleType()), comment='Упаковки Товара. Подробнее тут')
    partialDisposal = Column(Boolean,
                                    comment='Управление состоянием частичного выбытия маркированного товара. «True» - возможность включена.')
    pathName = Column(String(255),
                             comment='Наименование группы, в которую входит Товар Обязательное при ответе Только для чтения')
    paymentItemType = Column(String(255), comment='Признак предмета расчета. Подробнее тут')
    ppeType = Column(String(255),
                            comment='Код вида номенклатурной классификации медицинских средств индивидуальной защиты (EAN-13). Подробнее тут')
    productFolder = Column(JSON, comment='Метаданные группы Товара Expand')
    # salePrices = Column(MutableList.as_mutable(ARRAY(JSON)), comment='Цены продажи. Подробнее тут')
    salePrices = Column(MutableList.as_mutable(PickleType()), comment='Цены продажи. Подробнее тут')

    shared = Column(Boolean, comment='Общий доступ Обязательное при ответе')
    supplier = Column(JSON, comment='Метаданные контрагента-поставщика Expand')
    # syncId = Column(Uuid, comment='ID синхронизации Только для чтения Заполнение при создании')
    syncId = Column(String(255), comment='ID синхронизации Только для чтения Заполнение при создании')

    taxSystem = Column(String(255), comment='Код системы налогообложения. Подробнее тут')
    # things = Column(MutableList.as_mutable(ARRAY(String)), comment='Серийные номера')
    things = Column(MutableList.as_mutable(PickleType()), comment='Серийные номера')
    tnved = Column(String(255), comment='Код ТН ВЭД')
    trackingType = Column(String(255), comment='Тип маркируемой продукции. Подробнее тут')
    uom = Column(JSON, comment='Единицы измерения Expand')
    # updated = Column(DateTime,
    #                         comment='Момент последнего обновления сущности Обязательное при ответе Только для чтения')
    updated = Column(String(255),
                     comment='Момент последнего обновления сущности Обязательное при ответе Только для чтения')

    useParentVat = Column(Boolean,
                                 comment='Используется ли ставка НДС родительской группы. Если True для единицы ассортимента будет применена ставка, установленная для родительской группы. Обязательное при ответе')
    variantsCount = Column(BigInteger,
                                  comment='Количество модификаций у данного товара Обязательное при ответе Только для чтения')
    vat = Column(BigInteger, comment='НДС %')
    vatEnabled = Column(Boolean,
                               comment='Включен ли НДС для товара. С помощью этого флага для товара можно выставлять НДС = 0 или НДС = "без НДС". (vat = 0, vatEnabled = False) -> vat = "без НДС", (vat = 0, vatEnabled = True) -> vat = 0%.')
    volume = Column(BigInteger, comment='Объем')
    weight = Column(BigInteger, comment='Вес')


async def create_table_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_table_async():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def insert_new_row(prod_dict):
    prog_obj = TGModelProd(prod_dict)
    async with async_session.begin() as s:
        s.add(prog_obj)


def create_new_table_sync():
    Base.metadata.create_all(engine)


def delete_table_sync():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    # create_new_table_sync()
    asyncio.run(create_table_async())
    # asyncio.run(drop_table_async())


