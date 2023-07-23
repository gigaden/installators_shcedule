from models import Users, session
from sqlalchemy.exc import IntegrityError


# добавляем пользователя в бд
async def create_new_user(user_data: dict):
    new_user: Users = Users(
        tg_id=user_data['tg_id'], fio=user_data['fio'], car_num=user_data['car_num'],
        car_model=user_data['car_model'], dogovor=user_data['dogovor'], filial=user_data['filial']
    )
    session.add(new_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()


# проверяем есть ли пользователь в бд
async def check_user_in_db(tg_id: int):
    if session.query(Users).filter(Users.tg_id == tg_id).first():
        return True
    return False
