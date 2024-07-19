# !!!used SQLAlchemy 2.0.18
import asyncio

from sqlalchemy import create_engine, inspect
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy import Double, BigInteger, Uuid, Boolean, select
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, DATE
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from AiogramPackage.TGAlchemy.TGConnSQL import TGConnSQL
__url = TGConnSQL().get_sql_url()
engine = create_async_engine(__url)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
	pass

class TGModelProd(Base):
	__tablename__ = 'product_model'
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	accountId = Column(Uuid, comment='ID учетной записи Обязательное при ответе Только для чтения')
	alcoholic = Column(JSONB, comment='Объект, содержащий поля алкогольной продукции. Подробнее тут')
	archived = Column(Boolean, comment='Добавлен ли Товар в архив Обязательное при ответе')
	article = Column(String(255), comment='Артикул')
	attributes = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Коллекция доп. полей')
	barcodes = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Штрихкоды Комплекта. Подробнее тут')
	buyPrice = Column(JSONB, comment='Закупочная цена. Подробнее тут')
	code = Column(String(255), comment='Код Товара')
	country = Column(JSONB, comment='Метаданные Страны Expand')
	description = Column(String(4096), comment='Описание Товара')
	discountProhibited = Column(Boolean, comment='Признак запрета скидок Обязательное при ответе')
	effectiveVat = Column(BigInteger, comment='Реальный НДС % Только для чтения')
	effectiveVatEnabled = Column(Boolean, comment='Дополнительный признак для определения разграничения реального НДС = 0 или "без НДС". (effectiveVat = 0, effectiveVatEnabled = false) -> "без НДС", (effectiveVat = 0, effectiveVatEnabled = true) -> 0%. Только для чтения')
	externalCode = Column(String(255), comment='Внешний код Товара Обязательное при ответе')
	files = Column(JSONB, comment='Метаданные массива Файлов (Максимальное количество файлов - 100) Expand')
	group = Column(JSONB, comment='Метаданные отдела сотрудника Обязательное при ответе Expand')
	id = Column(Uuid, unique=True, nullable=False, comment='ID Товара Обязательное при ответе Только для чтения')
	images = Column(JSONB, comment='Массив метаданных Изображений (Максимальное количество изображений - 10) Expand')
	isSerialTrackable = Column(Boolean, comment='Учет по серийным номерам. Данная отметка не сочетается с признаками weighed, alcoholic, ppeType, trackingType, onTap.')
	meta = Column(JSONB, comment='Метаданные Товара Обязательное при ответе')
	minPrice = Column(JSONB, comment='Минимальная цена. Подробнее тут')
	minimumBalance = Column(BigInteger, comment='Неснижаемый остаток')
	name = Column(String(255), comment='Наименование Товара Обязательное при ответе Необходимо при создании')
	owner = Column(JSONB, comment='Метаданные владельца (Сотрудника) Expand')
	packs = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Упаковки Товара. Подробнее тут')
	partialDisposal = Column(Boolean, comment='Управление состоянием частичного выбытия маркированного товара. «true» - возможность включена.')
	pathName = Column(String, comment='Наименование группы, в которую входит Товар Обязательное при ответе Только для чтения')
	paymentItemType = Column(String(255), comment='Признак предмета расчета. Подробнее тут')
	ppeType = Column(String(255), comment='Код вида номенклатурной классификации медицинских средств индивидуальной защиты (EAN-13). Подробнее тут')
	productFolder = Column(JSONB, comment='Метаданные группы Товара Expand')
	salePrices = Column(MutableList.as_mutable(ARRAY(JSONB)), comment='Цены продажи. Подробнее тут')
	shared = Column(Boolean, comment='Общий доступ Обязательное при ответе')
	supplier = Column(JSONB, comment='Метаданные контрагента-поставщика Expand')
	syncId = Column(Uuid, comment='ID синхронизации Только для чтения Заполнение при создании')
	taxSystem = Column(String(255), comment='Код системы налогообложения. Подробнее тут')
	things = Column(MutableList.as_mutable(ARRAY(String)), comment='Серийные номера')
	tnved = Column(String(255), comment='Код ТН ВЭД')
	trackingType = Column(String(255), comment='Тип маркируемой продукции. Подробнее тут')
	uom = Column(JSONB, comment='Единицы измерения Expand')
	# updated = Column(DateTime, comment='Момент последнего обновления сущности Обязательное при ответе Только для чтения')
	updated = Column(DATE,
					 comment='Момент последнего обновления сущности Обязательное при ответе Только для чтения')

	useParentVat = Column(Boolean, comment='Используется ли ставка НДС родительской группы. Если true для единицы ассортимента будет применена ставка, установленная для родительской группы. Обязательное при ответе')
	variantsCount = Column(BigInteger, comment='Количество модификаций у данного товара Обязательное при ответе Только для чтения')
	vat = Column(BigInteger, comment='НДС %')
	vatEnabled = Column(Boolean, comment='Включен ли НДС для товара. С помощью этого флага для товара можно выставлять НДС = 0 или НДС = "без НДС". (vat = 0, vatEnabled = false) -> vat = "без НДС", (vat = 0, vatEnabled = true) -> vat = 0%.')
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

async def get_prod_row(prod_id):
	async with async_session() as session:
		query = select(TGModelProd).where(TGModelProd.id == prod_id)
		result = await session.execute(query)
	return result.scalar()


if __name__ == '__main__':
    # create_new_table_sync()
    # asyncio.run(create_table_async())
    # asyncio.run(drop_table_async())
	prod_obj = asyncio.run(get_prod_row(prod_id="07583f34-a80d-11eb-0a80-084000094ab6"))
	print(prod_obj.name)