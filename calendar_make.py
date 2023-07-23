import calendar
import locale
from datetime import date

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

print(list(calendar.day_name))
print(list(calendar.day_abbr))
print(list(calendar.month_name))
print(list(calendar.month_abbr))
# Функция monthcalendar(year, month) возвращает матрицу, представляющую календарь на месяц.
# Каждая строка матрицы представляет неделю.
current_date = date.today()
print(calendar.monthcalendar(2023,5))

# Функция month(year, month, w=0, l=0) возвращает календарь на месяц в многострочной строке.
# Аргументами функции являются: year (год), month (месяц), w (ширина столбца даты) и l (количество строк, отводимые на неделю).
print(calendar.month(2023, 5))
for i in calendar.month_abbr[1:]:
    print(i)

# year, month = input().split()
month_dict ={}
j = 0
for m in calendar.month_abbr[1:]:
    month_dict[m] = j
    j +=1
print(month_dict)

year = current_date.year
month = current_date.month
print(list(calendar.day_abbr))
print(*calendar.monthcalendar(year, month), sep='\n')
print(current_date.month)

from settings import current_month

mn = calendar.month_name[month - 1]
print(mn)