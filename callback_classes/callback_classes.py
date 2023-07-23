from aiogram.filters.callback_data import CallbackData


# классы для формирования нового месяца
class CallBackMonthForward(CallbackData, prefix='>>>'):
    month: int
    year: int


class CallBackMonthBack(CallbackData, prefix='<<<'):
    month: int
    year: int


class CallBackDay(CallbackData, prefix="selected_date"):
    year: int
    month: int
    day: int
