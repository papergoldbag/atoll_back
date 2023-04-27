from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class BaseUserKeyboard:
    def start_keyboard(self) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.insert(KeyboardButton("Авторизоваться"))
        return keyboard
    

class SportsmanKeyboard:
    def menu_keyboard(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.insert(KeyboardButton("Мероприятия"))
        keyboard.insert(KeyboardButton("Мои сорревнования"))
        return keyboard
    def events_keyboard(self, ):
        keyboard = InlineKeyboardMarkup()


class AdminKeyboard:
     def menu_keyboard(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.insert(KeyboardButton("Заявки"))
        keyboard.insert(KeyboardButton("Архив сорревнований"))
        return keyboard
     
class RepresentativeKeyboard:
     def menu_keyboard(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.insert(KeyboardButton("Заявки"))
        keyboard.insert(KeyboardButton("Архив сорревнований"))
        return keyboard

class PartnerKeyboard:
     def menu_keyboard(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.insert(KeyboardButton("Заявки"))
        keyboard.insert(KeyboardButton("Архив сорревнований"))
        return keyboard

base_user_keyboard = BaseUserKeyboard()