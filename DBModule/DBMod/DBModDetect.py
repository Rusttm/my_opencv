# !!!used SQLAlchemy 2.0.18
from sqlalchemy import create_engine, inspect
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy import Double, BigInteger, Uuid, Boolean
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, insert
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase

from DBModule.DBConn.DBConnAlchemy import DBConnAlchemy
engine = DBConnAlchemy().create_alchemy_con_sync()

class Base(DeclarativeBase):
	pass

class DBModDetect(Base):
	__tablename__ = 'detect_model'
	# __table_args__ = (UniqueConstraint('id', name='unique_key_id'),)
	position_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	created = Column(DateTime, comment='Дата создания')
	category_name = Column(String(1024), comment='Название категории')
	confident = Column(Double, comment='Степень уверенности %%')
	box_x1 = Column(Double, comment='Координата X1 прямоугольника')
	box_y1 = Column(Double, comment='Координата Y1 прямоугольника')
	box_x2 = Column(Double, comment='Координата X2 прямоугольника')
	box_y2 = Column(Double, comment='Координата Y2 прямоугольника')
	box_width = Column(Double, comment='Ширина кадра')
	box_height = Column(Double, comment='Высота кадра')
	description = Column(String(4096), comment='Описание категории')

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()
