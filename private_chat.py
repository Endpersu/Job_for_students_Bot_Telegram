from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from userdatabase import Database
from loguru import logger


class Form(StatesGroup):
    first_name = State()
    second_name = State()
    age = State()
    job = State()


def anketa(dp: Dispatcher):
    @dp.message(Command('start'))
    async def cmd_start(message: types.Message, state: FSMContext):
        await state.set_state(Form.first_name)
        await message.answer("Здравствуйте, давайте заполним мини-анкету")
        await message.answer("Как вас зовут?")
        db = Database()
        db.add_user(message.from_user.id, message.from_user.username)
        db.print_users()

    @dp.message(Form.first_name)
    async def process_first_name(message: types.Message, state: FSMContext):
        await state.update_data(first_name=message.text)
        logger.info('Пользователь написал свое имя')
        await state.set_state(Form.second_name)
        await message.answer(f"Приятно познакомиться, {message.text}! Какая у вас фамилия?")

    @dp.message(Form.second_name)
    async def process_second_name(message: types.Message, state: FSMContext):
        if message.text.isdigit():
            await message.answer("Пожалуйста, введите фамилию.")
            logger.info("Пользователь написал фамилию некорректно")
            return
        await state.update_data(second_name=message.text)
        logger.info('Пользователь написал свою фамилию')
        await state.set_state(Form.age)
        await message.answer(f"Какой у вас возраст?")

    @dp.message(Form.age)
    async def process_age(message: types.Message, state: FSMContext):
        if not message.text.isdigit():
            await message.answer("Пожалуйста, введите число!")
            logger.info('Пользователь написал возраст некорректно')
            return
        await state.update_data(age=message.text)
        await state.set_state(Form.job)
        await message.answer(f"Ваш возраст: {message.text}. Какая ваша желаемая сфера деятельности в подработке?")
        logger.info('Пользователь ввел возраст')

    @dp.message(Form.job)
    async def process_job(message: types.Message, state: FSMContext):
        await state.update_data(job=message.text)
        logger.info('Пользователь написал свою деятельность')
        data = await state.get_data()
        await message.answer(
            f"Спасибо, что заполнили анкету!\n"
            f"Имя: {data['first_name']}\n"
            f"Фамилия: {data['second_name']}\n"
            f"Возраст: {data['age']}\n"
            f"Сфера деятельности: {data['job']}"
        )
        logger.info('Пользователь получил свою анкету')
        buttons = [
            [types.KeyboardButton(text="Да✅"), types.KeyboardButton(text="Нет❌")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons)
        await message.answer("Вы правильно ввели свои данные?", reply_markup=keyboard)
        logger.info("Пользователь проверяет свои данные")
        @dp.message(lambda message: message.text in ["Да✅", "Нет❌"])
        async def handle_button_click(message: types.Message, state: FSMContext):
            if message.text == "Нет❌":
                await state.set_state(Form.first_name)
                await message.answer("Введите анкету заново")
                logger.info("Пользователь вводит анкету заново")
                await message.answer("Как вас зовут?")
            elif message.text == "Да✅":
                await message.answer("Заполнение мини-анкеты завершено. Переходим в меню.")
        
        await state.clear()
