from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


# class MonthForward(BaseFilter):
#     async def __call__(self, callback: CallbackQuery) -> bool:
#         command, month = callback.data.split(" ")
#         return command == 'month_forward' and month.isdigit()
#
#
# class MonthBack(BaseFilter):
#     async def __call__(self, callback: CallbackQuery) -> bool:
#         command, month = callback.data.split(" ")
#         return command == 'month_back' and month.isdigit()