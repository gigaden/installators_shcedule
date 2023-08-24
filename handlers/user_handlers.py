from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU

router: Router = Router()


# хэндлер будет срабатывать на комманду старт вне состояний и предлагать заполнить анкету для регистрации
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU["/start"])


# сработает при отправке команды '/help'
@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU["/help"], parse_mode="HTML")


# сработает при отправке команды '/feedback'
@router.message(Command(commands="feedback"))
async def process_feedback_command(message: Message):
    await message.answer(LEXICON_RU["/feedback"])
