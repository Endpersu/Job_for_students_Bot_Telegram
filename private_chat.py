import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    first_name = State()
    second_name = State()
    age = State()
    job = State()

def anketa(dp: Dispatcher):
    @dp.message(Command('start'))
    async def cmd_start(message: types.Message, state: FSMContext):
        await state.set_state(Form.first_name)
        await message.answer("Как вас зовут?")

    @dp.message(Form.first_name)
    async def process_first_name(message: types.Message, state: FSMContext):
        await state.update_data(first_name=message.text)
        await state.set_state(Form.second_name)
        await message.answer(
            f"Приятно познакомиться, {message.text}! Какая у вас фамилия?")

    @dp.message(Form.second_name)
    async def process_second_name(message: types.Message, state: FSMContext):
        await state.update_data(second_name=message.text)
        await state.set_state(Form.age)
        await message.answer(
            f"Какой у вас возраст?")

    @dp.message(Form.age)
    async def process_age(message: types.Message, state: FSMContext):
        if not message.text.isdigit():
            await message.answer("Пожалуйста, введите число!")
            return
        await state.update_data(age=message.text)
        await state.set_state(Form.job)
        await message.answer(
            f"Ваш возраст: {message.text}. Какая ваша желаемая сфера деятельности в подработке?"
        )

    @dp.message(Form.job)
    async def process_job(message: types.Message, state: FSMContext):
        await state.update_data(job=message.text)

        data = await state.get_data()
        print(data)
        

        await message.answer(
            f"Спасибо, что заполнили анкету!\n"
            f"Имя: {data['first_name']}\n"
            f"Фамилия: {data['second_name']}\n"
            f"Возраст: {data['age']}\n"
            f"Сфера деятельности: {data['job']}"
        )
        
        await state.clear()

if __name__ == '__main__':
    anketa(dp)
    dp.run_polling(bot)