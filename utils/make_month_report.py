from docxtpl import DocxTemplate
from db.crud import take_addresses_objects, get_user
import locale
import calendar
from datetime import date
from settings import GAZ_TAX

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


async def make_month_report(tg_id: int, year: int, month: int) -> str:
    tpl = DocxTemplate('templates/month_report_template.docx')

    # получаем объекты Addresses, Users
    days_objects = take_addresses_objects(tg_id, year, month)
    total_distance = sum([day[2] for day in days_objects])
    user = get_user(tg_id)

    months = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
              'Ноябрь',
              'Декабрь']
    current_date = date.today()

    # формируем контекст для отправки в шаблон
    context = {
        'days': days_objects,
        'gaz_tax': GAZ_TAX,
        'total_distance': total_distance,
        'user': user,
        'month': months[month],
        'year': year,
        'date': [current_date.day, calendar.month_name[current_date.month], current_date.year]
    }

    # рендерим в шаблон и сохраняем
    tpl.render(context)
    file_address: str = f'templates/output/{user.fio.split(" ")[0]}_{month}_{year}.docx'
    tpl.save(file_address)
    return file_address


