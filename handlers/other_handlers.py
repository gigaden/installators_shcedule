from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU

router: Router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    await message.answer(f'{LEXICON_RU["dont_understand"]} "{message.text}"')
