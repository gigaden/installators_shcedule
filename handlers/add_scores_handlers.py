from aiogram import Router
from aiogram.filters import Command, CommandStart, Text, StateFilter

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from fsm.user_register_fsm import FSMFillAddresses, FSMFillScores

from aiogram.types import CallbackQuery, Message
from lexicon.lexicon_ru import LEXICON_ADDRESS, LEXICON_CALENDAR

from keyboards.calendar_keyboard import (
    create_calendar_keyboard,
    create_edit_day_keyboard,
)
from keyboards.addresses_keyboard import create_add_addresses_keyboard, add_scores_keyboard

from settings import current_year, current_month

from db.crud import add_address, get_filial_address, insert_day_score, check_days_in_db, get_selected_day_scores
from utils.check_address import check_address, prepare_address
from utils.get_coordinates import get_coordinates

from callback_classes.callback_classes import (
    CallBackAddress,
    CallBackCancel,
    CallBackFilialAddress,
    CallBackSaveAddress,
    CallBackAddScores,
)
from datetime import datetime

router: Router = Router()


# хэндлер будет срабатывать на /cancel в любых состояниях, кроме по умолчанию и отключать машину состояний
@router.callback_query(
    StateFilter(FSMFillScores.fill_scores), CallBackCancel.filter()
)
async def process_cancel_command_state(
        callback: CallbackQuery, state: FSMContext
):
    await callback.message.answer(text=LEXICON_ADDRESS["/cancel"])
    await state.clear()
    await callback.message.answer(
        text=LEXICON_CALENDAR["title"],
        reply_markup=create_calendar_keyboard(current_year, current_month),
    )


# хэндлер будет срабатывать на комманду добавить баллы
@router.callback_query(CallBackAddScores.filter())
async def process_add_scores_command(
        callback: CallbackQuery, state: FSMContext, callback_data: CallBackAddScores
):
    year, month, day = callback_data.year, callback_data.month, callback_data.day
    days_in_db: bool = await check_days_in_db(callback.from_user.id, year, month, day)
    if days_in_db:
        selected_date: datetime = datetime(year, month, day)
        selected_day_scores: (float,) = await get_selected_day_scores(callback.from_user.id, year, month, day)
        await state.update_data(current_date=selected_date)
        await callback.message.edit_text(
            text=f"За этот день добавлено: {selected_day_scores[0]} баллов.\n"
                 f"{LEXICON_ADDRESS['/add_scores']}",
            reply_markup=add_scores_keyboard(callback.from_user.id),
        )
        await state.set_state(FSMFillScores.fill_scores)
    else:
        await callback.message.answer(
            text=f"Сначало завершите день, а потом добавьте баллы.\n"
                 f"Выбран {callback_data.day:02d}.{callback_data.month:02d}.{callback_data.year}",
            reply_markup=create_edit_day_keyboard(
                callback_data.year, callback_data.month, callback_data.day
            ),
        )


# хэндлер отловит баллы в состоянии добавления баллов и занесёт их в бд
@router.message(StateFilter(FSMFillScores.fill_scores))
async def process_add_scores(message: Message, state: FSMContext):
    scores: str = message.text
    if scores.replace(".", "").replace(",", "").isdigit():
        user_date: dict = await state.get_data()
        year, month, day = user_date["current_date"].year, user_date["current_date"].month, user_date[
            "current_date"].day
        await message.answer(
            text=f"{LEXICON_ADDRESS['scores_added']}\n"
                 f"Выбран {user_date['current_date'].day:02d}.{user_date['current_date'].month:02d}.{user_date['current_date'].year}",
            reply_markup=create_edit_day_keyboard(
                year, month, day
            ),
        )
        await insert_day_score(message.from_user.id, year, month, day, float(scores.replace(",", ".")))
        await state.clear()
    else:
        await message.answer(text=LEXICON_ADDRESS["wrong_scores"],
                             reply_markup=add_scores_keyboard(message.from_user.id))
        await state.set_state(FSMFillScores.fill_scores)
