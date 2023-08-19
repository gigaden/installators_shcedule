# Телеграм-бот для выездных сотрудников Ростелеком

---
## Миссия бота:
Облегчить жизнь выездных специалистов, автоматизировав вычисление расстояний, пробега, затраченного топлива и формирование отчёта.
___

## Как работает:
- Сотрудник регистрируется через тг бот.
- Вносит адреса.
- Нажимает кнопку "Сформировать отчёт".
- Бот отправляет отчёт за месяц в формате .doc

## В основе бота лежит:
(все зависимости в requirements.txt)
- Python 3.11 - отец нашего бота.
- Aiogram 3.0.0b7 - мама нашего бота.
- PostgreSql - для хранения данных.
- Geopy 2.3.0 - помогает найти нужный адрес и рассчитать расстояние, вместе с:
    - Геокодер API Яндекса, для поиска координат.
    - API openrouteservice.org, для вычисления расстояний.
- SQLAlchemy 2.0.15 - для связи с БД.
- Docxtpl 0.16.7 - для формирования отчёта .docx.

## Установка и настройка
- Клонируйте репозиторий
- Отредактируйте файл ".env.example", сохранив его затем как ".env". Внутри файла необходимо вписать данные для доступа к БД, а также ключи для доступа к боту и гео-сервисам.
- В файле "settings.py" вы можете изменить стоимость 1 км в рублях в константе GAZ_TAX.
- В "templates/" расположен шаблон для формирования отчёта "month_report_template.docx", не рекомендуется его менять без особой нужды.

## Запуск бота
- В файле "models.py", где описаны модели таблиц БД, раскомментируйте нижнюю строчку, если таблицы в БД не созданы.
- Запустите файл "models.py".
- Запустите файл "bot.py"

## Ограничения ГЕО-систем
- бесплатный ключ openrouteservice.org ограничивает доступ к API на вычисление маршрута:
    - 2000 запросов в сутки.
    - 40 запросов в минуту.
- бесплатный ключ Геокодера Яндекса ограничивает доступ к API на вычисление координат:
    - 1000 запросов в сутки

