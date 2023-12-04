from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import models
from callback_classes.callback_classes import (
    CallBackEditUser,
    CallBackCloseDay,
    CallBackCancelEditField,
)

from db.crud import get_user


def user_data_keyboard(tg_id: int):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    user: models.Users = get_user(tg_id)
    fio: InlineKeyboardButton = InlineKeyboardButton(
        text=user.fio,
        callback_data=CallBackEditUser(tg_id=tg_id, field_name="fio").pack(),
    )
    car_num: InlineKeyboardButton = InlineKeyboardButton(
        text=user.car_num,
        callback_data=CallBackEditUser(tg_id=tg_id, field_name="car_num").pack(),
    )
    car_model: InlineKeyboardButton = InlineKeyboardButton(
        text=user.car_model,
        callback_data=CallBackEditUser(tg_id=tg_id, field_name="car_model").pack(),
    )
    dogovor: InlineKeyboardButton = InlineKeyboardButton(
        text=user.dogovor,
        callback_data=CallBackEditUser(tg_id=tg_id, field_name="dogovor").pack(),
    )
    filial: InlineKeyboardButton = InlineKeyboardButton(
        text=user.filial,
        callback_data=CallBackEditUser(tg_id=tg_id, field_name="filial").pack(),
    )
    filial_address: InlineKeyboardButton = InlineKeyboardButton(
        text=user.filial_address,
        callback_data=CallBackEditUser(tg_id=tg_id, field_name="filial_address").pack(),
    )
    score_price: InlineKeyboardButton = InlineKeyboardButton(
        text=f"Стоимость балла {user.score_price} руб.",
        callback_data=CallBackEditUser(tg_id=tg_id, field_name="score_price").pack(),
    )

    close: InlineKeyboardButton = InlineKeyboardButton(
        text="Закрыть редактирование", callback_data=CallBackCloseDay().pack()
    )
    kb_builder.row(
        fio, car_num, car_model, dogovor, filial, filial_address, score_price, close, width=1
    )
    return kb_builder.as_markup()


# клавиатура для кнопки отмены в режиме редактирования поля
def cancel_edit_field(tg_id: int):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    cancel: InlineKeyboardButton = InlineKeyboardButton(
        text="Закрыть", callback_data=CallBackCancelEditField().pack()
    )
    kb_builder.row(cancel, width=1)
    return kb_builder.as_markup()
