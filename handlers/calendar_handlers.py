import os
from aiogram import Router
from aiogram.filters import Command, StateFilter

from aiogram.fsm.state import default_state
from fsm.edit_address_fsm import FSMEditAddress
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message, FSInputFile

from db.crud import check_user_in_db, get_address, del_address, update_address

from lexicon.lexicon_ru import LEXICON_RU, LEXICON_CALENDAR

from keyboards.calendar_keyboard import create_calendar_keyboard, create_edit_day_keyboard, \
    create_addresses_day_keyboard, create_edit_selected_day_keyboard, process_close_edit_address_btn

from callback_classes.callback_classes import CallBackMonthForward, CallBackMonthBack, CallBackDay, \
    CallBackShowAddresses, CallBackCloseDay, CallBackEditDay, CallBackDelAddress, CallBackUpdateAddress, \
    CallBackFinishDay, CallBackMakeReport

from settings import current_year, current_month

from utils.check_address import check_address, prepare_address
from utils.get_coordinates import get_coordinates
from utils.finish_day import finish_day
from utils.make_month_report import make_month_report

router: Router = Router()


# хэндлер сработает на команду /calendar и развернёт клавиатуру с календарём
@router.message(Command(commands='calendar'), StateFilter(default_state))
async def process_calendar_command(message: Message):
    if await check_user_in_db(message.from_user.id):
        await message.answer(text=LEXICON_CALENDAR['title'],
                             reply_markup=create_calendar_keyboard(current_year, current_month))
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
        await callback.message.edit_text(
            text=f"Выбран {callback_data.day:02d}.{callback_data.month:02d}.{callback_data.year}",
            reply_markup=create_edit_day_keyboard(callback_data.year, callback_data.month,
                                                  callback_data.day))


# хэндлер отрабатывает при нажатии на кнопку "адреса за день" и выводит адреса за выбранную дату
@router.callback_query(CallBackShowAddresses.filter())
async def process_address_command(callback: CallbackQuery, callback_data: CallBackShowAddresses):
    await callback.message.edit_text(text=f'Адреса за {callback_data.day}'
                                          f'/{callback_data.month}'
                                          f'/{callback_data.year}\n'
                                          f'Нажмите на адрес, чтобы удалить, или изменить',
                                     reply_markup=create_addresses_day_keyboard(callback.from_user.id,
                                                                                callback_data.year,
                                                                                callback_data.month,
                                                                                callback_data.day))


# хэндлер отрабатывает при нажатии на кнопку "Закрыть" и возвращает календарь
@router.callback_query(CallBackCloseDay.filter())
async def process_close_day(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_CALENDAR['title'],
                                     reply_markup=create_calendar_keyboard(current_year, current_month))


# хэндлер отрабатывает на редактирование выбранного дня при нажатии на кнопку с адресом
@router.callback_query(CallBackEditDay.filter())
async def process_edit_day(callback: CallbackQuery, callback_data: CallBackEditDay, state: FSMContext):
    address = get_address(callback_data.id_address)
    await state.set_state(FSMEditAddress.edit_address)
    await callback.message.edit_text(text=f"Адрес для редактирования:\n"
                                          f"{address}",
                                     reply_markup=create_edit_selected_day_keyboard(callback.from_user.id,
                                                                                    callback_data.id_address,
                                                                                    callback_data.year,
                                                                                    callback_data.month,
                                                                                    callback_data.day
                                                                                    ))


# хэндлер в состоянии редактирования дня ловит адрес из сообщения, проверяет его и изменяет в бд
@router.callback_query(CallBackUpdateAddress.filter())
async def process_update_address(callback: CallbackQuery, callback_data: CallBackDelAddress, state: FSMContext):
    await state.update_data(id_address=callback_data.id_address)
    await state.update_data(tg_id=callback.from_user.id)
    await state.update_data(year=callback_data.year)
    await state.update_data(month=callback_data.month)
    await state.update_data(day=callback_data.day)
    await callback.message.edit_text(text="Введите новый адрес и нажмите отправить\n"
                                          "для выхода нажмите 'Закрыть'",
                                     reply_markup=process_close_edit_address_btn(callback.from_user.id,
                                                                                 callback_data.year,
                                                                                 callback_data.month,
                                                                                 callback_data.day))
    await state.set_state(FSMEditAddress.edit_address)


# ловим текст с новым адресом для изменения выбранного
@router.message(StateFilter(FSMEditAddress.edit_address))
async def process_change_address(message: Message, state: FSMContext):
    new_full_address: str = message.text
    new_address: str = prepare_address(new_full_address)
    new_coordinates: tuple = get_coordinates(new_address)
    user_data: dict = await state.get_data()
    if check_address(new_address) and new_coordinates:
        await update_address(user_data['id_address'], new_address, new_coordinates, new_full_address)
    await message.answer(text=f'Адреса за {user_data["day"]}'
                              f'/{user_data["month"]}'
                              f'/{user_data["year"]}\n'
                              f'Нажмите на адрес, чтобы удалить, или изменить',
                         reply_markup=create_addresses_day_keyboard(user_data['tg_id'], user_data['year'],
                                                                    user_data['month'],
                                                                    user_data['day']))
    await state.clear()


# хэндлер сработае при нажатии на кнопку "удалить адрес"
@router.callback_query(CallBackDelAddress.filter(), StateFilter(FSMEditAddress.edit_address))
async def process_del_address(callback: CallbackQuery, callback_data: CallBackDelAddress):
    await del_address(callback_data.id_address, callback.from_user.id)
    await callback.message.edit_text(text=f'Адреса за {callback_data.day}'
                                          f'/{callback_data.month}'
                                          f'/{callback_data.year}\n'
                                          f'Нажмите на адрес, чтобы удалить, или изменить',
                                     reply_markup=create_addresses_day_keyboard(callback.from_user.id,
                                                                                callback_data.year,
                                                                                callback_data.month,
                                                                                callback_data.day))


# сработает при нажатии кнопки "Завершить день", рассчитает и занесёт в БД маршрут за день
@router.callback_query(CallBackFinishDay.filter())
async def process_finish_day(callback: CallbackQuery, callback_data: CallBackFinishDay):
    if await finish_day(callback.from_user.id, callback_data.year, callback_data.month,
                        callback_data.day):
        await callback.message.edit_text(text=f'{LEXICON_CALENDAR["finish_day_done"]}',
                                         reply_markup=create_calendar_keyboard(current_year, current_month))
    else:
        await callback.message.edit_text(text=f'{LEXICON_CALENDAR["not_enough_addresses"]}',
                                         reply_markup=create_edit_day_keyboard(callback_data.year, callback_data.month,
                                                                               callback_data.day))


# сработает при нажатии кнопки сформировать отчёт
@router.callback_query(CallBackMakeReport.filter())
async def process_make_report(callback: CallbackQuery, callback_data: CallBackMakeReport):
    # создаём отчёт за выбранный месяц и получаем путь к файлу
    file_address: str = await make_month_report(callback.from_user.id, callback_data.year, callback_data.month)
    fs_input: FSInputFile = FSInputFile(path=file_address)

    # отправляем его пользователю
    await callback.message.edit_text(text=LEXICON_CALENDAR['month_report_done'])
    await callback.message.answer_document(document=fs_input)
    await callback.message.answer(text=LEXICON_CALENDAR['title'],
                                  reply_markup=create_calendar_keyboard(current_year, current_month))

    # файл отправлен, можно его удалить из папки
    os.remove(file_address)
