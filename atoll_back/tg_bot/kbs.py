# TODO

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from emoji import emojize


class InlineKb:
    cd_main_menu = CallbackData("main_menu")

    @classmethod
    def open_main_menu(cls, *, from_: str = ""):
        kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
        kb.insert(InlineKeyboardButton(
            text=emojize(":control_knobs: Меню"),
            callback_data=cls.cd_main_menu.new()
        ))
        return kb

    @classmethod
    def events(cls, *, from_: str = ""):
        kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
        kb.insert(InlineKeyboardButton(
            text=emojize(":control_knobs: Меню"),
            callback_data=cls.cd_main_menu.new()
        ))
        return kb

