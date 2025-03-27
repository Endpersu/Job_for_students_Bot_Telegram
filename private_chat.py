from aiogram import Router, types
from aiogram.filters import Command
from loguru import logger

priver_router = Router()

@private_router.message(Command('start'))
async def private_start(message: types.Message):
    await message.answer("Привет ! Я эхо бот. Просто напиши мне что-нибудь")
    logger.info(f"Пользователь {message.from_user.id} начал чат")


@private_router.message()
async def echo(message: types.Message):
    logger.info(f"Это для пользователя {message.from_user.id}: {message.text}")
