from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="О нас🔴"), KeyboardButton(text="Ваш профиль👤")],
        [KeyboardButton(text="Поиск подработки🔍")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def get_back_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Вернуться в меню⬅️")]], resize_keyboard=True)


def get_profile_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="Редактировать профиль✏️")],
        [KeyboardButton(text="Вернуться в меню⬅️")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    
