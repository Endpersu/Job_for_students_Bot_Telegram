import asyncio
import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from userdatabase import Database

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")


async def main():
    logger.add("file.log",
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               rotation="3 days",
               backtrace=True,
               diagnose=True)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    dp = Dispatcher()
    db = Database()
    
    @dp.message(Command('start'))
    async def start_command(message: types.Message):
        user_id = message.from_user.id
        username = message.from_user.username if message.from_user.username else "У пользователя нет username"
        
        db.add_user(user_id, username)
        db.print_users()


    from private_chat import anketa
    from group_chat import setup_group_handlers
    from channel import setup_channel_handlers

    anketa(dp)
    setup_group_handlers(dp)
    setup_channel_handlers(dp, bot)


    logger.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == '__main__':
    asyncio.run(main())