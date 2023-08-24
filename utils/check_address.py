import re
from lexicon.lexicon_ru import WORD_EXCEPTION


# проверяем валидность вводимого пользователем адреса
def check_address(address: str) -> bool:
    # регулярка ищет вхождение только этих символов
    pattern = r"^[а-яА-яЁё.,\d\s/\\]+$"
    match = re.search(pattern, address)
    if match and len(address) > 15:
        return True
    return False


# чистим адрес для загрузки в бд
def prepare_address(address: str) -> str:
    # убираем через регулярку всё не нужное
    address = re.sub(r"(Мжф,\s)|(г\.)|(пом\.\d+)|(\d+/\d+$)", "", address)
    # проверяем на слова и символы, которые не позволят найти верные координаты
    for word in WORD_EXCEPTION:
        if word in address:
            address = address.replace(word, WORD_EXCEPTION[word])

    return address
