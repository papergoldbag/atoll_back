import logging

from aiogram import types

from atoll_back.core import db
from atoll_back.consts import TgBotCommands
from atoll_back.core import dp
from atoll_back.tg_bot.filters import RoleFilter
from atoll_back.tg_bot.keyboards import base_user_keyboard
from atoll_back.tg_bot.utils import return_user_keyboard
from atoll_back.services import get_user

log = logging.getLogger(__name__)


@dp.message_handler(commands=TgBotCommands.start)
async def on_cmd_start(message: types.Message):
    await message.answer(f"Здраствуйте, {message.from_user.first_name}, пожалуйста авторизуйтесь!", reply_markup=base_user_keyboard.start_keyboard())

@dp.message_handler()
async def on_btn_auth(message: types.Message):
    client = await get_user(tg_id=message.from_user.id)
    if client is None:
        await message.answer("Зарегистрируйтесь на нашем сайте!\n")
    await message.answer("Вы успешно авторизировались", reply_markup=return_user_keyboard().menu_keyboard())

def import_handlers():
    log.info('handlers were imported')
