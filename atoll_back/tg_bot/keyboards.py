from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from atoll_back.models import Event

class BaseUserKeyboard:
    start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    start_keyboard.insert(KeyboardButton("Авторизоваться"))
    
    menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_keyboard.insert(KeyboardButton("Мероприятия"))
    menu_keyboard.insert(KeyboardButton("Мои события"))

base_user_keyboard = BaseUserKeyboard()
