from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text, StateFilter

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from fsm.user_register_fsm import FSMFillAddresses

from aiogram.types import CallbackQuery, Message
from lexicon.lexicon_ru import LEXICON_ADDRESS, LEXICON_CALENDAR

from keyboards.calendar_keyboard import create_calendar_keyboard
from keyboards.addresses_keyboard import create_add_addresses_keyboard

from settings import current_year, current_month

from db.crud import add_address, get_filial_address
from utils.check_address import check_address, prepare_address
from utils.get_coordinates import get_coordinates

from callback_classes.callback_classes import CallBackAddress, CallBackCancel, CallBackFilialAddress, \
    CallBackSaveAddress
from datetime import datetime

router: Router = Router()


# хэндлер будет срабатывать на комманду /address
@router.callback_query(CallBackAddress.filter())
async def process_address_command(callback: CallbackQuery, state: FSMContext, callback_data: CallBackAddress):
    year, month, day = callback_data.year, callback_data.month, callback_data.day
    selected_date: datetime = datetime(year, month, day)
    await state.update_data(addresses_array=[selected_date])
    await callback.message.edit_text(text=LEXICON_ADDRESS['/address'],
                                     reply_markup=create_add_addresses_keyboard(callback.from_user.id))
    await state.set_state(FSMFillAddresses.fill_address)


# хэндлер будет срабатывать на /cancel в любых состояниях, кроме по умолчанию и отключать машину состояний
@router.callback_query(StateFilter(FSMFillAddresses.fill_address), CallBackCancel.filter())
async def process_cancel_command_state(callback: CallbackQuery, state: FSMContext, callback_data: CallBackAddress):
    await callback.message.answer(text=LEXICON_ADDRESS['/cancel'])
    await state.clear()
    await callback.message.answer(text=LEXICON_CALENDAR['title'],
                                  reply_markup=create_calendar_keyboard(current_year, current_month))


@router.callback_query(CallBackFilialAddress.filter(), StateFilter(FSMFillAddresses.fill_address))
async def process_send_filial_address(callback: CallbackQuery, state: FSMContext, callback_data: CallBackFilialAddress):
    filial_address: str = await get_filial_address(callback_data.tg_id)
    address: str = prepare_address(filial_address)
    coordinates: tuple = get_coordinates(address)
    if check_address(address) and coordinates:
        await callback.message.answer(
            text=f"{LEXICON_ADDRESS['addresses_added']} \nкоординаты адреса {coordinates}",
            reply_markup=create_add_addresses_keyboard(callback.from_user.id))
        full_address: str = filial_address
        user_data: dict = await state.get_data()
        user_data['addresses_array'].append((address, coordinates, full_address))
        await state.update_data(addresses_array=user_data['addresses_array'])
    else:
        await callback.message.answer(text=LEXICON_ADDRESS['wrong_address'])
    await state.set_state(FSMFillAddresses.fill_address)


# хэндлер будет срабатывать в состоянии добавления адреса
@router.message(StateFilter(FSMFillAddresses.fill_address))
async def process_add_address(message: Message, state: FSMContext):
    address: str = prepare_address(message.text)
    coordinates: tuple = get_coordinates(address)
    if check_address(address) and coordinates:
        await message.answer(
            text=f"{LEXICON_ADDRESS['addresses_added']} \nкоординаты адреса {coordinates}",
            reply_markup=create_add_addresses_keyboard(message.from_user.id))
        full_address: str = message.text
        user_data: dict = await state.get_data()
        user_data['addresses_array'].append((address, coordinates, full_address))
        await state.update_data(addresses_array=user_data['addresses_array'])
    else:
        await message.answer(text=LEXICON_ADDRESS['wrong_address'])
    await state.set_state(FSMFillAddresses.fill_address)


# хэндлер сработает при нажатии /saveaddress и занесёт данные в бд
@router.callback_query(CallBackSaveAddress.filter(), StateFilter(FSMFillAddresses.fill_address))
async def process_finish_add_address(callback: CallbackQuery, state: FSMContext, callback_data: CallBackSaveAddress):
    user_data: dict = await state.get_data()
    if len(user_data['addresses_array']) > 1:
        await callback.message.answer(text=LEXICON_ADDRESS['/saveaddress'])
        await add_address(callback.from_user.id, user_data['addresses_array'])
        await state.clear()
        await callback.message.answer(text=LEXICON_CALENDAR['title'],
                                      reply_markup=create_calendar_keyboard(current_year, current_month))
    else:
        await callback.message.answer(text=LEXICON_ADDRESS['no_address_added'],
                                      reply_markup=create_add_addresses_keyboard(callback.from_user.id))
        await state.set_state(FSMFillAddresses.fill_address)
