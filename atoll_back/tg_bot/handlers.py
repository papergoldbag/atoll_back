import logging

from aiogram import types
from emoji import emojize

from atoll_back.consts import TgBotCommands
from atoll_back.core import dp, db
from atoll_back.models import Event
from atoll_back.services import get_events

log = logging.getLogger(__name__)


@dp.message_handler(commands=TgBotCommands.start)
async def on_cmd_start(message: types.Message):
    await message.answer(message.text)


@dp.message_handler(commands=TgBotCommands.events)
async def on_cmd_events(message: types.Message):
    event_docs = await db.event_collection.get_all_docs()
    events = [Event.parse_document(event_doc) for event_doc in event_docs]

    if not events:
        text = "Пока что нет мероприятий"
    else:
        text = ":bookmark_tabs: Мероприятия:\n\n"
        for event in events:
            text += (
                f"<b>{event.title}</b>\n"
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
    await message.answer(message.text)


@dp.message_handler(commands=TgBotCommands.echo)
async def on_cmd_echo(message: types.Message):
    await message.answer(message.text)


def import_handlers():
    log.info('handlers were imported')
