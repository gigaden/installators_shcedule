import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import (
    register_handlers,
    add_address_handlers,
    calendar_handlers,
    other_handlers,
    user_handlers,
    edit_user_data_handlers,
    add_scores_handlers,
)
from aiogram.fsm.storage.memory import MemoryStorage

from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.ERROR,
        # filename="bot.log",
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(register_handlers.router)
    dp.include_router(add_address_handlers.router)
    dp.include_router(calendar_handlers.router)
    dp.include_router(edit_user_data_handlers.router)
    dp.include_router(add_scores_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
