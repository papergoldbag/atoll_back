import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
import emoji

from atoll_back.core import db
from atoll_back.consts import TgBotCommands
from atoll_back.core import dp
from atoll_back.tg_bot.filters import RoleFilter
from atoll_back.tg_bot.keyboards import base_user_keyboard
from atoll_back.tg_bot.utils import get_event_description, get_my_event
from atoll_back.tg_bot.states import UserStates
from atoll_back.services import get_user, get_events
from atoll_back.models import User

log = logging.getLogger(__name__)

@dp.message_handler(commands=TgBotCommands.start)
async def on_cmd_start(message: types.Message):
    await message.answer(f"Здраствуйте, {message.from_user.first_name}, пожалуйста авторизуйтесь!", reply_markup=base_user_keyboard.start_keyboard)

@dp.message_handler(text="Авторизоваться", state=None)
async def on_btn_auth(message: types.Message, state: FSMContext):
    client = await get_user(tg_username=message.from_user.username)
    if client is None:
         await message.answer("Вы не зарегистрированы!\n")
    async with state.proxy() as data:
            data["roles"] = client.roles[0]
    await message.answer("Вы успешно авторизировались", reply_markup=base_user_keyboard.menu_keyboard)
    await UserStates.authorized.set()

@dp.message_handler(text = "Мероприятия", state=[UserStates.authorized])
async def on_btn_event(message: types.Message):
    events = await get_events()
    if len(events) == 0:
        await message.answer("Мероприятий не запланировано!")
    else:
        await message.answer(emoji.emojize(":calendar: Запланированы следующие мероприятия :calendar:\n"))
        
    for event in events:
         await message.answer(await get_event_description(event))

@dp.message_handler(text = "Мои события", state=[UserStates.authorized])
async def on_btn_event(message: types.Message):
    user: User = await get_user(tg_username=message.from_user.username)
    events = await get_my_event(useroid=user.oid)
    if len(events) == 0:
        await message.answer("Вы не участвуете в мероприятиях!")
    else:
        await message.answer(emoji.emojize(":calendar: Запланированы следующие мероприятия :calendar:\n"))
        for event in events:
            await message.answer(await get_event_description(event))


def import_handlers():
    log.info('handlers were imported')
