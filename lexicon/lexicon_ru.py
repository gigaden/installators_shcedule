LEXICON_RU = {
    '/start': 'Для использования бота вам нужно зарегистрироваться\n\n'
              'Чтобы это сделать отправьте комманду /fillform',
    '/help': 'Полноценная '
             '<a href="https://github.com/gigaden/installators_shcedule/blob/main/manual_for_installators.pdf">'
             'инструкция с картинками лежит тут</a>.\n\n'
             '<u><b>Если вы не зарегистрированы</b>, для начала работы:</u>\n\n'
             '<i>- Отправьте команду /start, или нажмите кнопку</i>.\n'
             '<i>- Для регистрации отправьте команду /fillform.</i>\n'
             '<i>- Поэтапно введите о чём вас просит бот.</i>\n'
             '<u>- Внимательно вводите данные, они будут выгружены в шапку отчёта.</u>\n'
             '<i>- После регистрации откройте календарь через кнопку меню, или отправьте /calendar.</i>\n\n'
             '<b><u>Работа с календарём</u></b>\n\n'
             '<i>- Выберите нужный день</i>\n'
             '<i>Откроется меню, где вы сможете добавить новый адрес, посмотреть добавленные адреса за день.</i>\n'
             '<i>- "Завершить день" - при нажатии будет расчитан маршрут по всем адресам за день и они будут записаны'
             ' в базу данных.</i>\n'
             '<i><b>Нажимайте "завершить день", когда вы больше не собираетесь вносить изменений в текущий день,'
             ' если после этого вы внесли какие-то правки в адрес, или добавили новый,'
             ' то нажмите "Завершить день" повторно</b></i>\n\n'
             '<u><b>Добавление адреса</b></u>\n\n'
             '<i>- Нажмите "Добавить адрес", после выбора дня в календаре</i>.\n'
             '<i>- Нажмите "Добавить адрес филиала" и он будет автоматически добавлен в маршрут</i>.\n'
             '<i>- Скопируйте адрес из "Монтажника" и отправьте его в сообщении<u>(по одному адресу в каждом сообщении)</u></i>.\n'
             '<i>- Нажмите "Сохранить адреса", чтобы они записались в маршрут</i>.\n\n'
             '<u><b>Редактирование/удаление адреса из добавленных</b></u>\n\n'
             '<i>- Нажмите на день в календаре, далее "Адреса за день"</i>.\n'
             '<i>- В открывшемся списке адресов нажмите на нужный вам</i>.\n'
             '<i>- Нажмите "Удалить адрес" для удаления его из маршрута</i>.\n'
             '<i>- Нажмите "Изменить адрес" и в сообщении отправьте новый, для его изменения</i>.\n\n'
             '<u><b>Отчёт за месяц</b></u>\n\n'
             '<i>- Выберите нужный месяц в календаре стрелочками &lt&lt или &gt&gt </i>.\n'
             '<i>- Нажмите кнопку под календарём "Сформировать отчёт за месяц"</i>.\n'
             '<i>- Далее Бот пришлёт вам отчёт</i>.',
    '/feedback': 'Если вы заметили какие-либо ошибки в работе бота, \n'
                 'хотели бы что-то добавить, или изменить\n'
                 'напишите мне в телеграм @dovgaletskiy',
    '/cancel': 'Вы вышли из заполнения анкеты, данные не сохранились\n'
               'Чтобы заново заполнить анкету отправьте /fillform',
    '/cancel_default_state': 'Данная комманда доступна только во время регистрации и добавлении адреса\n'
                             'чтобы зарегистрироваться отправьте /fillform',
    '/fillform_already_registered': 'Вы уже зарегистрированы с этого аккаунта Телеграм',
    '/fillform_insert_name': 'Введите ваше ФИО в формате - "Фамилия Имя Отчество"\n\n'
                             'Пример:\n Иванов Иван Иванович\n\n'
                             'Чтобы начать заново, или выйти отправьте /cancel',
    '/fillform_insert_auto_num': 'Спасибо, теперь введите номер автомобиля\n'
                                 'Только цифры и буквы\n\n'
                                 'Пример:\n Е001КХ199\n\n'
                                 'Чтобы начать заново, или выйти отправьте /cancel',
    '/fillform_insert_wrong_name': 'Неверный формат ввода ФИО. Попробуйте ещё раз в формате\n'
                                   '"Фамилия Имя Отчество".\n'
                                   'Если хотите прервать регистрацию отправьте  /cancel',
    '/fillform_car_model': 'Спасибо, теперь введите марку автомобиля\n\n'
                           'Пример:\n Mercedes-Benz\n\n'
                           'Чтобы начать заново, или выйти отправьте /cancel',
    '/fillform_dogovor_num': 'Спасибо, теперь введите номер договора\n\n'
                             'Пример:\n 0605/25/2121/21 от 22.09.2021 г.\n\n'
                             'Чтобы начать заново, или выйти отправьте /cancel',
    '/fillform_filial': 'Спасибо, теперь введите региональный филиал\n\n'
                        'Пример:\nНижегородский\n\n'
                        'Чтобы начать заново, или выйти отправьте /cancel',
    '/fillform_filial_addresses': 'Спасибо, введите адрес филиала\n\n'
                                  'Пример:\nНижний Новгород, ул. Космонавта Комарова, 13Б\n\n'
                                  'Чтобы начать заново, или выйти отправьте /cancel',
    '/fillform_finish': 'Спасибо за регистрацию, теперь вы можете начать пользоваться ботом',
    'user_created': 'Регистрация успешна!\n'
                    'Чтобы добавить новый адрес откройте календарь через Меню,\n'
                    'или отправьте команду /calendar',
    'not_registered_user': 'Эта команда доступна только зарегистрированным пользователям.\n'
                           'Для регистрации отправьте /fillform',
    'dont_understand': 'Извините, но я, ещё пока, не обучен обрабатывать этот запрос!',
}

LEXICON_ADDRESS = {
    '/address': 'Отправьте адрес в сообщении\n\n'
                'Добавить адрес филиала можно по кнопке "Добавить адрес филиала"\n'
                'Чтобы выйти из добавления адреса нажмите "Закрыть"\n'
                'при этом данные не сохранятся. Чтобы их сохранить нажмите "Сохранить адреса"',
    '/cancel': 'Вы вышли из добавления адреса, данные не сохранились\n'
               'Для повтора выберите день в календаре',
    '/cancel_add_address': 'Закрыть',
    'addresses_added': 'Адрес добавлен.\n\nЧтобы добавить ещё один - отправьте его в сообщении.\n\n'
                       '  Чтобы сохранить адреса и выйти нажмите <b>"Сохранить адреса".</b>\n'
                       '  Чтобы выйти без сохранения нажмите <b>"Закрыть".</b>\n'
                       '  Чтобы добавить адрес филиала нажмите <b>"Добавить адрес филиала".</b>',
    '/filial_address': 'Добавить адрес филиала',
    '/saveaddress': 'Адреса сохранены, вы вышли из заполнения',
    'saveaddress_btn': 'Сохранить адреса',
    'wrong_address': 'То, что вы вводите не очень похоже на адрес \n'
                     'попробуйте ещё раз',
    'no_address_added': 'Вы не добавили ни одного адреса\n'
                        'Нажмите кнопку "закрыть", чтобы выйти,\n'
                        'или добавьте адрес'
}

LEXICON_COMMANDS = {
    '/calendar': 'открыть календарь',
    '/help': 'справка',
    '/feedback': 'обратная связь',

}

LEXICON_CALENDAR = {
    'title': 'Выберите день',
    'wrong_day': 'Выберите день в этом месяце',
    'add_address_btn': 'Добавить адрес',
    'close_address_btn': 'Закрыть',
    'show_addresses': 'Адреса за день',
    'del': '❌ Удалить адрес',
    'update': 'Изменить адрес...',
    'finish_day': 'Завершить день',
    'finish_day_done': f'Если вы внесетё изменения в сохранённый день,\n'
                       f'то не забудьте ещё раз нажать кнопку завершения дня',
    'not_enough_addresses': 'За день должно быть добавлено минимум два разных адреса, чтобы рассчитать пробег \n'
                            'Добавьте ещё один адрес за день и попробуйте снова',
    'make_report_btn': 'Сформировать отчёт за месяц',
    'month_report_done': 'Отчёт за месяц готов',
}

WORD_EXCEPTION = {
    'ш.': 'шоссе',
    'пр-кт': 'проспект',
    'б-р': 'бульвар',
    'мкр.': 'микрорайон',
    'пр-д': 'проезд'
}
