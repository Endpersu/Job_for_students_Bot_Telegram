from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from User_menu import get_main_keyboard, get_back_keyboard, get_profile_keyboard
from userdatabase import Database
from loguru import logger
from parser_hh import get_vacancies_by_profession
import json


class Form(StatesGroup):
    first_name = State()
    second_name = State()
    age = State()
    profession = State()


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
        await message.answer("Какой у вас возраст?")

    @dp.message(Form.age)
    async def process_age(message: types.Message, state: FSMContext):
        if not message.text.isdigit():
            await message.answer("Пожалуйста, введите число!")
            logger.info('Пользователь написал возраст некорректно')
            return
        await state.update_data(age=message.text)
        await state.set_state(Form.profession)
        await message.answer(f"Ваш возраст: {message.text}. Какая ваша желаемая сфера деятельности в подработке?")
        logger.info('Пользователь ввел возраст')

    @dp.message(Form.profession)
    async def process_job(message: types.Message, state: FSMContext):
        await state.update_data(profession=message.text)
        logger.info('Пользователь написал свою деятельность')
        data = await state.get_data()
        await message.answer(
            f"Спасибо, что заполнили анкету!\n"
            f"Имя: {data['first_name']}\n"
            f"Фамилия: {data['second_name']}\n"
            f"Возраст: {data['age']}\n"
            f"Сфера деятельности: {data['profession']}"
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
                await message.answer("Введите анкету заново", reply_markup=ReplyKeyboardRemove())
                logger.info("Пользователь вводит анкету заново")
                await message.answer("Как вас зовут?")
            elif message.text == "Да✅":
                await message.answer("Заполнение мини-анкеты завершено. Переходим в меню.", reply_markup=get_main_keyboard())
                logger.info("Пользователь попал в меню")

        @dp.message(F.text == "О нас🔴")
        async def about_bot(message: types.Message):
            about_text = """ℹ️ Информация о боте:

        Этот бот создан для помощи в поиске подработки.
        Здесь вы можете:
        - Найти подходящие вакансии
        - Управлять своим профилем"""
            await message.answer(
                about_text,
                reply_markup=get_back_keyboard()
            )
            logger.info("Пользователь зашел в опцию 'О нас'")

        @dp.message(F.text == "Вернуться в меню⬅️")
        async def back_to_menu(message: types.Message):
            await message.answer(
                "Главное меню:",
                reply_markup=get_main_keyboard()
                )
        
        @dp.message(F.text == "Поиск подработки🔍")
        async def search_job(message: types.Message, state: FSMContext):
            await state.set_state(Form.profession)
            profession = data['profession']
            logger.info(f"Ищем вакансии по профессии: {profession}")

            # Вызываем парсер
            get_vacancies_by_profession(profession)

            try:
                with open("hh_vacancies.json", 'r', encoding='utf-8') as file:
                    vacancies = json.load(file)

                if vacancies.get("items"):
                    for item in vacancies["items"][:5]:  # Показываем первые 5 вакансий
                        vacancy_name = item['name']
                        city_name = item['area']['name']
                        alternate_url = item['alternate_url']

                        money_1 = item['salary']['from'] if item['salary'] else None
                        money_2 = item['salary']['to'] if item['salary'] else None

                        if money_1 and money_2:
                            salary_str = f"{money_1} – {money_2}"
                        elif money_1:
                            salary_str = f"от {money_1}"
                        elif money_2:
                            salary_str = f"до {money_2}"
                        else:
                            salary_str = "Не указана"

                        requirement = item['snippet']['requirement'] or "Не указано"
                        responsibility = item['snippet']['responsibility'] or "Не указано"

                        vacancy_info = (
                            f"📌 Вакансия: {vacancy_name}\n"
                            f"🏙 Город: {city_name}\n"
                            f"💰 Зарплата: {salary_str}\n"
                            f"📝 Требования: {requirement}\n"
                            f"📋 Обязанности: {responsibility}\n"
                            f"🔗 Ссылка: {alternate_url}"
                        )
                        await message.answer(vacancy_info)

                else:
                    await message.answer("Нет вакансий по вашей профессии.")

            except FileNotFoundError:
                await message.answer("Ошибка: данные не загружены. Попробуйте позже.")

        @dp.message(F.text == "Ваш профиль👤")
        async def show_profile(message: types.Message):
            if data:
                profile_text = f"""📌 Ваш профиль:

        👤 Имя: {data['first_name']}
        📝 Фамилия: {data['second_name']}
        🔢 Возраст: {data['age']}
        💼 Сфера деятельности: {data['profession']}
        """
                logger.info("Пользователь зашел в опцию 'Ваш профиль'")
                await message.answer(
                    profile_text,
                    reply_markup=get_profile_keyboard()
                )
            else:
                await message.answer(
                    "Профиль не найден. Заполните анкету сначала.",
                    reply_markup=get_main_keyboard()
                )

        @dp.message(F.text == "Редактировать профиль✏️")
        async def edit_profile(message: types.message, state: FSMContext):
            await state.set_state(Form.first_name)
            await message.answer("Давайте редактируем ваш профиль. Как вас зовут?", reply_markup=ReplyKeyboardRemove())
            logger.info("Пользователь начал редактирование профиля")
        await state.clear()
