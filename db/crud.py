from sqlalchemy.sql.functions import count, func

from models import Users, session, Addresses, Days
from sqlalchemy.exc import IntegrityError
from sqlalchemy import extract, select

from datetime import datetime, date

import re


# проверяем есть ли пользователь в бд
async def check_user_in_db(tg_id: int):
    if session.query(Users).filter(Users.tg_id == tg_id).first():
        return True
    return False


# добавляем пользователя в бд
async def create_new_user(user_data: dict):
    new_user: Users = Users(
        tg_id=user_data["tg_id"],
        fio=user_data["fio"],
        car_num=user_data["car_num"],
        car_model=user_data["car_model"],
        dogovor=user_data["dogovor"],
        filial=user_data["filial"],
        filial_address=user_data["filial_address"],
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
            full_address=address[2],
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
    query: list = (
        session.query(Addresses.full_address, Addresses.id)
        .filter(extract("month", Addresses.date) == month)
        .filter(extract("year", Addresses.date) == year)
        .filter(extract("day", Addresses.date) == day)
        .filter(Addresses.users_id == user.id)
        .order_by(Addresses.id)
        .all()
    )
    return query


# получаем только один адрес по выбранному id
def get_address(id_address: int) -> str:
    return (
        session.query(Addresses.full_address)
        .filter(Addresses.id == id_address)
        .first()[0]
    )


# удаляем выбранный адрес из бд
async def del_address(id_address: int, tg_id: int):
    user_id = session.query(Users).filter(Users.tg_id == tg_id).first()
    query = (
        session.query(Addresses)
        .filter(Addresses.id == id_address and Addresses.users_id == user_id)
        .one()
    )
    session.delete(query)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


# изменяем в бд выбранный адрес
async def update_address(
        id_address: int, address: str, coordinates: tuple, full_address: str
):
    query: [Addresses] = (
        session.query(Addresses).filter(Addresses.id == id_address).first()
    )
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
    query: list = (
        session.query(Addresses.coordinates, Addresses.full_address)
        .filter(extract("month", Addresses.date) == month)
        .filter(extract("year", Addresses.date) == year)
        .filter(extract("day", Addresses.date) == day)
        .filter(Addresses.users_id == user_id)
        .order_by(Addresses.id)
        .all()
    )
    all_coordinates: list = [
        tuple(float(re.sub(r"[\(\)]", "", coord)) for coord in coords[0].split(","))
        for coords in query
    ]
    all_full_addresses: str = "; ".join([address[1] for address in query])
    return all_coordinates, all_full_addresses


# заносим пробег за день и адреса в бд
async def add_distance_and_routes(
        tg_id: int, year: int, month: int, day: int, all_addresses: str, distance: float
):
    # проверяем есть ли запись за эту дату
    user = session.query(Users).filter(Users.tg_id == tg_id).first().id
    query = (
        session.query(Days)
        .filter(extract("month", Days.date) == month)
        .filter(extract("year", Days.date) == year)
        .filter(extract("day", Days.date) == day)
        .filter(Days.users_id == user)
        .first()
    )
    if query:
        query.all_addresses = all_addresses
        query.distance = distance
        session.add(query)
    else:
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
    query = (
        session.query(Days)
        .filter(extract("month", Days.date) == month)
        .filter(extract("year", Days.date) == year)
        .filter(Days.users_id == user.id)
        .order_by(Days.date)
        .all()
    )
    return [
        [day.date.strftime("%d.%m.%Y"), day.all_addresses, day.distance]
        for day in query
    ]


# редактируем поле в таблице Users
async def edit_user_field(tg_id: int, field_name: str, new_data: str):
    user: [Users] = get_user(tg_id)
    if field_name != 'score_price' or (field_name == 'score_price' and new_data.isdigit()):
        setattr(user, field_name, new_data)
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


# статистика для суперадмина
async def get_super_statistic():
    users_count = session.query(Users).count()
    query_users_days = select(Users.fio, count(Days.date)).join(Users.days).group_by(Users.fio)
    users_days = session.execute(query_users_days).all()

    return users_count, users_days


# получаем доход за месяц
async def get_scores(tg_id: int, month: int, year: int):
    user = session.query(Users).filter(Users.tg_id == tg_id).first()
    query_sum_scores = session.query(func.sum(Days.scores)).filter(extract("month", Days.date) == month).filter(
        extract("year", Days.date) == year).filter(Days.users_id == user.id).scalar()
    query_count_scores = session.query(func.count(Days.scores)).filter(extract("month", Days.date) == month).filter(
        extract("year", Days.date) == year).filter(Days.users_id == user.id).scalar()

    return query_sum_scores, query_count_scores


#  получаем доход за текущий день
async def get_day_scores(tg_id: int):
    current_date = date.today()
    day: int = current_date.day
    month: int = current_date.month
    year: int = current_date.year

    user = session.query(Users).filter(Users.tg_id == tg_id).first()
    score: int = (
        session.query(Days.scores)
        .filter(extract("month", Days.date) == month)
        .filter(extract("year", Days.date) == year)
        .filter(extract("day", Days.date) == day)
        .filter(Days.users_id == user.id)
        .first()
    )
    return score if score else [0]


#  получаем доход за выбранный день
async def get_selected_day_scores(tg_id: int, year: int, month: int, day: int) -> float:
    user = session.query(Users).filter(Users.tg_id == tg_id).first()
    score: float = (
        session.query(Days.scores)
        .filter(extract("month", Days.date) == month)
        .filter(extract("year", Days.date) == year)
        .filter(extract("day", Days.date) == day)
        .filter(Days.users_id == user.id)
        .first()
    )
    return score


# заносим в бд баллы за день
async def insert_day_score(tg_id: int, year: int, month: int, day: int, scores: float):
    user = session.query(Users).filter(Users.tg_id == tg_id).first()
    query = session.query(Days).filter(extract("month", Days.date) == month).filter(
        extract("year", Days.date) == year).filter(extract("day", Days.date) == day).filter(
        Days.users_id == user.id).first()

    query.scores = scores
    session.add(query)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


# проверяем есть ли запись за эту дату в таблице Days
async def check_days_in_db(
        tg_id: int, year: int, month: int, day: int):
    user = session.query(Users).filter(Users.tg_id == tg_id).first().id
    query = (
        session.query(Days)
        .filter(extract("month", Days.date) == month)
        .filter(extract("year", Days.date) == year)
        .filter(extract("day", Days.date) == day)
        .filter(Days.users_id == user)
        .first()
    )

    return not (query is None)


# получаем стоимость балла у пользователя из бд
async def get_price_scores(tg_id: int):
    price_scores = session.query(Users.score_price).filter(Users.tg_id == tg_id).first()
    return price_scores
