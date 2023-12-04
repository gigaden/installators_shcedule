from datetime import date

# По умолчанию календарь формируется используя текущую дату
current_date = date.today()
current_month = current_date.month
current_year = current_date.year

GAZ_TAX = 10.71 if 10 < current_month < 3 else 9.73  # стоимость 1 км пути в рублях в зависимости от месяца(лето/зима)
SCORE_PRICE = 102  # стоимость балла по умолчанию, юзер сможет потом изменить
