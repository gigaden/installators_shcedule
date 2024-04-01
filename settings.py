from datetime import date

# По умолчанию календарь формируется используя текущую дату
current_date = date.today()
current_month = current_date.month
current_year = current_date.year

# стоимость 1 км пути в рублях в зависимости от месяца(лето/зима)
GAZ_TAX = 11.28 if current_month in (11, 12, 1, 2, 3) else 10.25
SCORE_PRICE = 102  # стоимость балла по умолчанию, юзер сможет потом изменить