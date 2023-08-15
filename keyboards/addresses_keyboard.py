from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_ADDRESS
from callback_classes.callback_classes import CallBackCancel, CallBackFilialAddress, CallBackSaveAddress


def create_add_addresses_keyboard(tg_id: int):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    cancel: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_ADDRESS['/cancel_add_address'],
        callback_data=CallBackCancel().pack()
    )
    filial_address: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_ADDRESS['/filial_address'],
        callback_data=CallBackFilialAddress(tg_id=tg_id).pack())
    save_address: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_ADDRESS['saveaddress_btn'],
        callback_data=CallBackSaveAddress().pack()
    )
    kb_builder.row(filial_address, save_address, cancel, width=1)
    return kb_builder.as_markup()
