from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text, StateFilter

from aiogram.fsm.state import default_state

from aiogram.types import CallbackQuery, Message

from db.crud import check_user_in_db

from lexicon.lexicon_ru import LEXICON_RU, LEXICON_CALENDAR

from keyboards.calendar_keyboard import create_calendar_keyboard, create_edit_day_keyboard

from callback_classes.callback_classes import CallBackMonthForward, CallBackMonthBack, CallBackDay

from settings import current_year, current_month

router: Router = Router()


# хэндлер сработает на команду /calendar и развернёт клавиатуру с календарём
@router.message(Command(commands='calendar'), StateFilter(default_state))
async def process_calendar_command(message: Message):
    if await check_user_in_db(message.from_user.id):
        await message.answer(text=LEXICON_CALENDAR['title'], reply_markup=create_calendar_keyboard(current_year, current_month))
    else:
        await message.answer(text=LEXICON_RU['not_registered_user'])


# хэндлер будет срабатывать на кнопку >>> и выводить следующий месяц
@router.callback_query(CallBackMonthForward.filter())
async def process_next_month(callback: CallbackQuery, callback_data: CallBackMonthForward):
    await callback.message.edit_text(text=LEXICON_CALENDAR['title'],
                                     reply_markup=create_calendar_keyboard(callback_data.year, callback_data.month + 1)
                                     )


# хэндлер будет срабатывать на кнопку <<< и выводить следующий месяц
@router.callback_query(CallBackMonthBack.filter())
async def process_next_month(callback: CallbackQuery, callback_data: CallBackMonthBack):
    await callback.message.edit_text(text=LEXICON_CALENDAR['title'],
                                     reply_markup=create_calendar_keyboard(callback_data.year, callback_data.month - 1)
                                     )


# хэндлер обрабатывает нажатие пользователя на день календаря
@router.callback_query(CallBackDay.filter())
async def process_selected_day(callback: CallbackQuery, callback_data: CallBackDay):
    if callback_data.day == 0:
        await callback.answer(text=LEXICON_CALENDAR['wrong_day'], show_alert=True)
    else:
        await callback.message.edit_text(text='редактирование дня',
                                         reply_markup=create_edit_day_keyboard(callback_data.year, callback_data.month,
                                                                               callback_data.day))
