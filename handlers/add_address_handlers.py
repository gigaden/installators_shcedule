from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text, StateFilter

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from fsm.user_register_fsm import FSMFillAddresses

from aiogram.types import CallbackQuery, Message
from lexicon.lexicon_ru import LEXICON_ADDRESS, LEXICON_CALENDAR

from keyboards.calendar_keyboard import create_calendar_keyboard

from settings import current_year, current_month

from db.crud import create_new_user, check_user_in_db

router: Router = Router()


# хэндлер будет срабатывать на комманду /address
@router.callback_query(Text(text='/address'))
async def process_address_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_ADDRESS['/address'])
    await state.update_data(addresses_array=list())
    await state.set_state(FSMFillAddresses.fill_address)


# хэндлер будет срабатывать на /cancel в любых состояниях, кроме по умолчанию и отключать машину состояний
@router.message(StateFilter(FSMFillAddresses.fill_address), Command(commands='cancel'))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADDRESS['/cancel'])
    await state.clear()
    await message.answer(text=LEXICON_CALENDAR['title'],
                         reply_markup=create_calendar_keyboard(current_year, current_month))


# хэндлер будет срабатывать в состоянии добавления адреса
@router.message(~Command(commands='saveaddress'), StateFilter(FSMFillAddresses.fill_address))
async def process_add_address(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADDRESS['addresses_added'])
    user_data: dict = await state.get_data()
    print(user_data['addresses_array'])
    user_data['addresses_array'].append(message.text)
    await state.update_data(addresses_array=user_data['addresses_array'])
    await state.set_state(FSMFillAddresses.fill_address)


# хэндлер сработает при нажатии /saveaddress и занесёт данные в бд
@router.message(Command(commands='saveaddress'), StateFilter(FSMFillAddresses.fill_address))
async def process_finish_add_address(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADDRESS['/saveaddress'])
    user_data: dict = await state.get_data()
    print(user_data['addresses_array'])

    await state.clear()
