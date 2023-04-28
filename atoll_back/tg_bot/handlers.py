import logging
from typing import Optional

from aiogram import types
from emoji import emojize

from atoll_back.consts import TgBotCommands
from atoll_back.core import dp, db
from atoll_back.models import Event, User
from atoll_back.services import get_events, get_user
from atoll_back.tg_bot.middleware import MiscData

log = logging.getLogger(__name__)


@dp.message_handler(commands=TgBotCommands.start)
async def on_cmd_start(message: types.Message, misc: MiscData):
    # try to define referrer from msg
    # user: Optional[User] = misc.user
    # user_msg_text = message.text.strip()
    # if user_msg_text.count(" ") == 1:
    #     user_int_id = user_msg_text.split(" ")[1].strip()
    #     if user_int_id != misc.user.int_id:
    #         user = await get_user(id_=user_int_id)

    await message.answer(
        text=(
            "<b>Здравствуйте, данный бот позволит узнать список всех актуальных мероприятий</b>"
        )
    )


@dp.message_handler(commands=TgBotCommands.events)
async def on_cmd_events(message: types.Message):
    event_docs = await db.event_collection.get_all_docs()
    events = [Event.parse_document(event_doc) for event_doc in event_docs]

    if not events:
        text = "Пока что нет мероприятий"
    else:
        text = ":bookmark_tabs: Мероприятия:\n\n"
        for i, event in enumerate(events):
            i += 1
            text += (
                f"{i} <b>{event.title}</b>\n"
                f"{event.description}\n"
                f"Начало: {event.start_dt.date()}\n"
                f"Конец: {event.end_dt.date()}\n\n"
            )
            pass
        text += (
            "<i>Для подробностей скачайте наше <a href='https://atoll.divarteam.ru/'>мобильное приложение с нашего сайта</a></i>"
        )

    await message.answer(text=emojize(text))


@dp.message_handler(commands=TgBotCommands.site)
async def on_cmd_site(message: types.Message):
    await message.answer("<a href='https://atoll.divarteam.ru/'>Переходите на наш сайт</a>")


@dp.message_handler(commands=TgBotCommands.echo)
async def on_cmd_echo(message: types.Message):
    await message.answer(message.text)


def import_handlers():
    log.info('handlers were imported')
