# !!!used SQLAlchemy 2.0.18
from sqlalchemy import create_engine, inspect
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy import Double, BigInteger, Uuid, Boolean
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, insert
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase

from datetime import datetime

from DBModule.DBConn.DBConnAlchemy import DBConnAlchemy
engine = DBConnAlchemy().create_alchemy_con_sync()

class Base(DeclarativeBase):
	pass

class DBModCapture(Base):
	__tablename__ = 'video_capture_model'
	# __table_args__ = (UniqueConstraint('id', name='unique_key_id'),)
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	inserted_at = Column(DateTime, default=datetime.now(), comment='Дата внесения в базу')
	created = Column(DateTime, comment='Дата создания')
	closed = Column(DateTime, comment='Дата закрытия')
	category_name = Column(String(1024), comment='Название категории')
	confident = Column(Double, comment='Степень уверенности %%')
	time = Column(Double, comment='Длительность в секундах')
	frame_width = Column(Integer, comment='Ширина кадра')
	frame_height = Column(Integer, comment='Высота кадра')
	count = Column(Double, comment='Количество объектов')
	path = Column(String(4096), comment='Название файла')
	description = Column(String(4096), comment='Описание категории')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()
