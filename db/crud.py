from models import Users, session, Addresses, Days
from sqlalchemy.exc import IntegrityError
from sqlalchemy import extract

from datetime import datetime

import re


# проверяем есть ли пользователь в бд
async def check_user_in_db(tg_id: int):
    if session.query(Users).filter(Users.tg_id == tg_id).first():
        return True
    return False


# добавляем пользователя в бд
async def create_new_user(user_data: dict):
    new_user: Users = Users(
        tg_id=user_data['tg_id'], fio=user_data['fio'], car_num=user_data['car_num'],
        car_model=user_data['car_model'], dogovor=user_data['dogovor'], filial=user_data['filial'],
        filial_address=user_data['filial_address']
    )
    session.add(new_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


# получаем объект пользователя из бд
def get_user(tg_id: int):
    return session.query(Users).filter(Users.tg_id == tg_id).first()


# добавляем адрес в бд
async def add_address(tg_id: int, addresses_array: list):
    users = session.query(Users).filter(Users.tg_id == tg_id).first().id
    current_date = addresses_array[0]
    addresses: list = []
    for address in addresses_array[1:]:
        new_address: Addresses = Addresses(
            users_id=users,
            date=current_date,
            address=address[0],
            coordinates=address[1],
            full_address=address[2]
        )
        addresses.append(new_address)
    for address_obj in addresses:
        session.add(address_obj)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


# получаем адрес филиала пользователя
async def get_filial_address(tg_id: int):
    return session.query(Users).filter(Users.tg_id == tg_id).first().filial_address


# получаем адреса и их id за выбранную дату
def get_addresses(tg_id: int, year: int, month: int, day: int) -> list:
    user = session.query(Users).filter(Users.tg_id == tg_id).first()
    query: list = session.query(Addresses.full_address, Addresses.id).filter(
        extract('month', Addresses.date) == month).filter(extract('year', Addresses.date) == year).filter(
        extract('day', Addresses.date) == day).filter(
        Addresses.users_id == user.id).order_by(Addresses.id).all()
    return query


# получаем только один адрес по выбранному id
def get_address(id_address: int) -> str:
    return session.query(Addresses.full_address).filter(Addresses.id == id_address).first()[0]


# удаляем выбранный адрес из бд
async def del_address(id_address: int, tg_id: int):
    user_id = session.query(Users).filter(Users.tg_id == tg_id).first()
    query = session.query(Addresses).filter(Addresses.id == id_address and Addresses.users_id == user_id).one()
    session.delete(query)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


# изменяем в бд выбранный адрес
async def update_address(id_address: int, address: str, coordinates: tuple, full_address: str):
    query: [Addresses] = session.query(Addresses).filter(Addresses.id == id_address).first()
    query.address = address
    query.coordinates = coordinates
    query.full_address = full_address
    session.add(query)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


# получаем список координат за выбранный день
async def take_all_routs_for_day(tg_id: int, year: int, month: int, day: int):
    user_id = session.query(Users).filter(Users.tg_id == tg_id).first().id
    query: list = session.query(Addresses.coordinates, Addresses.full_address).filter(
        extract('month', Addresses.date) == month).filter(extract('year', Addresses.date) == year).filter(
        extract('day', Addresses.date) == day).filter(
        Addresses.users_id == user_id).order_by(Addresses.id).all()
    all_coordinates: list = [tuple(float(re.sub(r'[\(\)]', '', coord)) for coord in coords[0].split(',')) for coords in
                             query]
    all_full_addresses: str = '; '.join([address[1] for address in query])
    return all_coordinates, all_full_addresses


# заносим пробег за день и адреса в бд
async def add_distance_and_routes(tg_id: int, year: int, month: int, day: int, all_addresses: str, distance: float):
    # проверяем есть ли запись за эту дату
    query = session.query(Days).filter(Days.date == datetime(year, month, day)).first()
    if query:
        query.all_addresses = all_addresses
        query.distance = distance
        session.add(query)
    else:
        user = session.query(Users).filter(Users.tg_id == tg_id).first().id
        date = datetime(year, month, day)
        new_day = Days(
            users_id=user, date=date, all_addresses=all_addresses, distance=distance
        )
        session.add(new_day)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


# получаем объекты Addresses за выбранный месяц и возвращаем список дат, адресов, расстояний
def take_addresses_objects(tg_id: int, year: int, month: int) -> list:
    user = session.query(Users).filter(Users.tg_id == tg_id).first()
    query = session.query(Days).filter(
        extract('month', Days.date) == month).filter(extract('year', Days.date) == year).filter(
        Days.users_id == user.id).order_by(
        Days.date).all()
    return [[day.date.strftime('%d.%m.%Y'), day.all_addresses, day.distance] for day in query]
