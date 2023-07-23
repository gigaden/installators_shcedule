from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text, StateFilter

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from fsm.user_register_fsm import FSMFillForm, FSMFillAddresses

from aiogram.types import CallbackQuery, Message

from keyboards.calendar_keyboard import create_calendar_keyboard

from settings import current_year, current_month

from db.crud import create_new_user, check_user_in_db
from lexicon.lexicon_ru import LEXICON_RU


router: Router = Router()


# хэндлер будет срабатывать на комманду старт вне состояний и предлагать заполнить анкету для регистрации
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# хэндлер будет срабатывать на /cancel в любых состояниях, кроме по умолчанию и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state), ~StateFilter(FSMFillAddresses.fill_address))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel'])
    await state.clear()


# хэндлер будет срабатывать на команду /cancel  в состоянии по умолчанию и сообщать, что
# эта команда доступна только при заполнении анкеты
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['/cancel_default_state'])


# хэндлер сработает на команду /fillform
@router.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    # проверяем есть ли тг айди в бд
    user_in_db = await check_user_in_db(message.from_user.id)
    if user_in_db:
        await message.answer(text=LEXICON_RU['/fillform_already_registered'])
        await state.clear()
        return
    await message.answer(text=LEXICON_RU['/fillform_insert_name'])
    # устанавливаем состояние ожидания ввода фио
    await state.set_state(FSMFillForm.fill_fio)


# сработает при корректном вводе фио и переведёт  в состояние ввода номера авто
@router.message(StateFilter(FSMFillForm.fill_fio), F.text.replace(' ', '').isalpha())
async def process_fio_sent(message: Message, state: FSMContext):
    # сохраняем фио в хранилище по ключу 'fio'
    await state.update_data(fio=message.text)
    await message.answer(text=LEXICON_RU['/fillform_insert_auto_num'])
    await state.set_state(FSMFillForm.fill_car_num)


# сработает при некорректном вводе фио
@router.message(StateFilter(FSMFillForm.fill_fio))
async def wrong_fio(message: Message):
    await message.answer(text=LEXICON_RU['/fillform_insert_wrong_name'])


# сработает при корректном вводе номера авто
@router.message(StateFilter(FSMFillForm.fill_car_num))
async def process_car_num_sent(message: Message, state: FSMContext):
    await state.update_data(car_num=message.text)
    await message.answer(text=LEXICON_RU['/fillform_car_model'])
    await state.set_state(FSMFillForm.fill_car_model)


# сработает при корректном вводе модели авто
@router.message(StateFilter(FSMFillForm.fill_car_model))
async def process_car_num_sent(message: Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    await message.answer(text=LEXICON_RU['/fillform_dogovor_num'])
    await state.set_state(FSMFillForm.fill_dogovor)


# сработает при корректном вводе номера договора
@router.message(StateFilter(FSMFillForm.fill_dogovor))
async def process_dogovor_sent(message: Message, state: FSMContext):
    await state.update_data(dogovor=message.text)
    await message.answer(text=LEXICON_RU['/fillform_filial'])
    await state.set_state(FSMFillForm.fill_filial)


# сработает при корректном вводе филиала
@router.message(StateFilter(FSMFillForm.fill_filial))
async def process_filial_sent(message: Message, state: FSMContext):
    await state.update_data(filial=message.text)
    await state.update_data(tg_id=message.from_user.id)

    user_data: dict = await state.get_data()
    # заносим в бд
    await create_new_user(user_data)
    print(user_data)
    await message.answer(text=f"{user_data['fio']}\n"
                              f"{user_data['car_num']}\n"
                              f"{user_data['car_model']}\n"
                              f"{user_data['dogovor']}\n"
                              f"{user_data['filial']}\n"
                              f"{message.from_user.id}\n"
                              f"{LEXICON_RU['/fillform_finish']}")
    await state.clear()



