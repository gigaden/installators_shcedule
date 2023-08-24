from aiogram.filters.state import StatesGroup, State


# класс для создания состояния при редактировании выбранного дня
class FSMEditAddress(StatesGroup):
    edit_address = State()
