from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import calendar
import locale

from callback_classes.callback_classes import CallBackMonthForward, CallBackMonthBack, CallBackDay, CallBackAddress, \
    CallBackShowAddresses, CallBackCloseDay, CallBackEditDay, CallBackDelAddress, CallBackUpdateAddress, \
    CallBackFinishDay
from lexicon.lexicon_ru import LEXICON_CALENDAR

from db.crud import get_addresses

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


# функция создаёт раскладку клавиатуры с календарём
def create_calendar_keyboard(year: int, month: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list = []

    # проверяем выход за границы года и месяца
    if month > 12:
        month -= 12
        year += 1
    elif month < 1:
        month += 12
        year -= 1

    for w in calendar.monthcalendar(year, month):
        for d in w:
            buttons.append(
                InlineKeyboardButton(text=d if d != 0 else ' ',
                                     callback_data=CallBackDay(year=year, month=month, day=d).pack()))

    day_abbr = [InlineKeyboardButton(text=i, callback_data=i) for i in calendar.day_abbr]
    kb_builder.row(InlineKeyboardButton(text='<<<', callback_data=CallBackMonthBack(year=year, month=month).pack()),
                   InlineKeyboardButton(text=calendar.month_abbr[month] + " " + str(year), callback_data=month),
                   InlineKeyboardButton(text='>>>', callback_data=CallBackMonthForward(year=year, month=month).pack())
                   )
    kb_builder.row(*day_abbr, width=7)
    kb_builder.row(*buttons, width=7)

    return kb_builder.as_markup()


# формируем клавиатуру при нажатии на кнопку дня из календаря
def create_edit_day_keyboard(year: int, month: int, day: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    address: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_CALENDAR['add_address_btn'],
                                                         callback_data=CallBackAddress(year=year, month=month,
                                                                                       day=day).pack())
    close: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_CALENDAR['close_address_btn'],
                                                       callback_data=CallBackCloseDay().pack())
    addresses: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_CALENDAR['show_addresses'],
                                                           callback_data=CallBackShowAddresses(year=year, month=month,
                                                                                               day=day).pack())
    finish_day: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_CALENDAR['finish_day'],
                                                            callback_data=CallBackFinishDay(year=year, month=month,
                                                                                            day=day).pack())
    kb_builder.row(address, close, addresses, finish_day, width=1)

    return kb_builder.as_markup()


# клавиатура для редактирования одного выбранного дня
def create_edit_selected_day_keyboard(tg_id: int, id_address: int, year: int, month: int, day: int):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    close_button: InlineKeyboardButton = \
        InlineKeyboardButton(text=LEXICON_CALENDAR['close_address_btn'],
                             callback_data=CallBackShowAddresses(year=year,
                                                                 month=month,
                                                                 day=day).pack())
    update_button: InlineKeyboardButton = \
        InlineKeyboardButton(text=LEXICON_CALENDAR['update'],
                             callback_data=CallBackUpdateAddress(tg_id=tg_id, id_address=id_address, year=year,
                                                                 month=month, day=day).pack())
    del_button: InlineKeyboardButton = \
        InlineKeyboardButton(text=f"{LEXICON_CALENDAR['del']}",
                             callback_data=CallBackDelAddress(tg_id=tg_id, id_address=id_address, year=year,
                                                              month=month, day=day).pack())
    kb_builder.row(update_button, del_button, close_button, width=1)
    return kb_builder.as_markup()


# формируем клавиатуру для показа всех адресов за выбранный день
def create_addresses_day_keyboard(tg_id: int, year: int, month: int, day: int) -> InlineKeyboardMarkup:
    addresses: list = get_addresses(tg_id, year, month, day)
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    addresses_button = [
        InlineKeyboardButton(text=f"{address[0][-50:]}", callback_data=CallBackEditDay(
            tg_id=tg_id, year=year, month=month, day=day, id_address=address[1]).pack()) for address in addresses]
    close_button = InlineKeyboardButton(text=LEXICON_CALENDAR['close_address_btn'],
                                        callback_data=CallBackDay(year=year, month=month, day=day).pack())
    kb_builder.row(*addresses_button, width=1)
    kb_builder.row(close_button)
    return kb_builder.as_markup()


# создаём кнопку "закрыть" при радактировании одного адреса
def process_close_edit_address_btn(tg_id: int, year: int, month: int, day: int):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    close_button: InlineKeyboardButton = \
        InlineKeyboardButton(text=LEXICON_CALENDAR['close_address_btn'],
                             callback_data=CallBackShowAddresses(year=year,
                                                                 month=month,
                                                                 day=day).pack())
    kb_builder.row(close_button)
    return kb_builder.as_markup()
