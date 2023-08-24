from aiogram import Router
from aiogram.filters import Command, StateFilter

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from fsm.user_register_fsm import FSMEditUser

from aiogram.types import CallbackQuery, Message

from keyboards.user_data_keyboard import user_data_keyboard, cancel_edit_field

from lexicon.lexicon_ru import LEXICON_EDIT_USER, LEXICON_RU
from callback_classes.callback_classes import CallBackEditUser, CallBackCancelEditField
from db.crud import edit_user_field, check_user_in_db

router: Router = Router()


# хэндлер будет срабатывать на /edit и отрабатывать редактирование данных пользователя
@router.message(Command(commands="edit"), StateFilter(default_state))
async def process_edit_user_data(message: Message):
    if await check_user_in_db(message.from_user.id):
        await message.answer(
            text=LEXICON_EDIT_USER["edit"],
            reply_markup=user_data_keyboard(message.from_user.id),
        )
    else:
        await message.answer(text=LEXICON_RU["not_registered_user"])


# ловим нажатие на кнопку с полем для редактирования
@router.callback_query(CallBackEditUser.filter())
async def process_edit_user_field(
    callback: CallbackQuery, callback_data: CallBackEditUser, state: FSMContext
):
    await state.set_state(FSMEditUser.edit)
    await state.update_data(field_name=callback_data.field_name)
    await callback.message.edit_text(
        text=LEXICON_EDIT_USER[callback_data.field_name],
        reply_markup=cancel_edit_field(callback.from_user.id),
    )


# ловим текст в состоянии редактирования поля юзера
@router.message(StateFilter(FSMEditUser.edit))
async def process_update_user_field(message: Message, state: FSMContext):
    users_field = await state.get_data()
    await edit_user_field(message.from_user.id, users_field["field_name"], message.text)
    await message.answer(
        text=LEXICON_EDIT_USER["edit"],
        reply_markup=user_data_keyboard(message.from_user.id),
    )
    await state.clear()


# ловим кнопку отмены в режиме редактирования поля юзера
@router.callback_query(CallBackCancelEditField.filter())
async def process_cancel_edit_field(
    callback: CallbackQuery, callback_data: CallBackCancelEditField, state: FSMContext
):
    await state.clear()
    await callback.message.edit_text(
        text=LEXICON_EDIT_USER["edit"],
        reply_markup=user_data_keyboard(callback.from_user.id),
    )
