from aiogram.filters.state import StatesGroup, State


# создаём класс для машины состояний регистрации пользователя
class FSMFillForm(StatesGroup):
    fill_fio = State()
    fill_car_num = State()
    fill_car_model = State()
    fill_dogovor = State()
    fill_filial = State()
    fill_filial_addresses = State()


class FSMFillAddresses(StatesGroup):
    fill_date = State()
    fill_address = State()


# класс для редактирования данных пользователя
class FSMEditUser(StatesGroup):
    edit = State()
