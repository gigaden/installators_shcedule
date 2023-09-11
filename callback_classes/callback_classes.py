from aiogram.filters.callback_data import CallbackData


# классы для формирования нового месяца
class CallBackMonthForward(CallbackData, prefix=">>>"):
    month: int
    year: int


class CallBackMonthBack(CallbackData, prefix="<<<"):
    month: int
    year: int


class CallBackDay(CallbackData, prefix="selected_date"):
    year: int
    month: int
    day: int


class CallBackAddress(CallbackData, prefix="address"):
    year: int
    month: int
    day: int


class CallBackShowAddresses(CallbackData, prefix="show_addresses"):
    year: int
    month: int
    day: int


class CallBackCloseDay(CallbackData, prefix="close_day_btn"):
    ...


class CallBackEditDay(CallbackData, prefix="edit_day"):
    tg_id: int
    year: int
    month: int
    day: int
    id_address: int


class CallBackDelAddress(CallbackData, prefix="del_address"):
    tg_id: int
    id_address: int
    year: int
    month: int
    day: int


class CallBackUpdateAddress(CallbackData, prefix="update_address"):
    tg_id: int
    id_address: int
    year: int
    month: int
    day: int


class CallBackFinishDay(CallbackData, prefix="finish_day"):
    year: int
    month: int
    day: int


# класс для кнопки отмена в состоянии внесения адреса
class CallBackCancel(CallbackData, prefix="cancel"):
    ...


# класс для кнопки получения адреса филиала
class CallBackFilialAddress(CallbackData, prefix="filial_address"):
    tg_id: int


# для передачи данных при нажатии сохранения адресов
class CallBackSaveAddress(CallbackData, prefix="saveaddress"):
    ...


# для передачи данных по кнопке отчёта за месяц
class CallBackMakeReport(CallbackData, prefix="make_report"):
    year: int
    month: int


# для фильтрации фио юзера
class CallBackEditUser(CallbackData, prefix="edit_user"):
    tg_id: int
    field_name: str


# для фильтрации кнопки отмены редактирования поля юзера
class CallBackCancelEditField(CallbackData, prefix="cancel_edit_field"):
    ...


# для отображения статистики для админов
class CallBackStatistic(CallbackData, prefix="statistic"):
    year: int
    month: int
