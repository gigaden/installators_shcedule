import psycopg2
from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey, BigInteger
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, scoped_session

from environs import Env

# Подключение к серверу PostgreSQL на localhost с помощью psycopg2 DBAPI
env = Env()
env.read_env()
engine = create_engine(
    f"postgresql+psycopg2://{env('DB_USER')}:{env('DB_PASS')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
)
session: scoped_session = scoped_session(sessionmaker(bind=engine))
Base: declarative_base = declarative_base()
Base.query = session.query_property()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False)
    fio = Column(String(300), nullable=False)
    car_num = Column(String(50), nullable=False)
    car_model = Column(String(50), nullable=False)
    dogovor = Column(String(50), nullable=False)
    filial = Column(String(80), nullable=False)
    filial_address = Column(String(300), nullable=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    days = relationship("Days")
    addresses = relationship("Addresses")


class Days(Base):
    __tablename__ = "days"
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, nullable=False)
    all_addresses = Column(String, nullable=False)
    distance = Column(Integer, nullable=True, default=0)


class Addresses(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, nullable=False, default=None)
    address = Column(String(300), nullable=False)
    coordinates = Column(String(100), nullable=False)
    full_address = Column(String(300), nullable=False)


Base.metadata.create_all(engine)  # Убрать комментарий, если нужно создать таблицы в БД
