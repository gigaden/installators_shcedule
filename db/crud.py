from models import Users, session, Addresses
from sqlalchemy.exc import IntegrityError

from datetime import datetime


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


# получаем адреса за выбранную дату
def get_addresses(tg_id: int, year: int, month: int, day: int) -> list:
    user_id = session.query(Users).filter(Users.tg_id == tg_id).first()
    query: list = session.query(Addresses.full_address).filter(
        Addresses.date == datetime(year, month, day) and Addresses.users_id == user_id).all()
    return [address[0] for address in query]


result = get_addresses(322908715, 2023, 8, 1)
print(result)
