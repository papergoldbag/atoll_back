import logging
from datetime import datetime

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

from atoll_back.consts import TgBotCommands
from atoll_back.core import dp, db, settings
from atoll_back.models import Event
from atoll_back.tg_bot.middleware import MiscData

log = logging.getLogger(__name__)


@dp.message_handler(commands=TgBotCommands.start)
async def on_cmd_start(message: types.Message, misc: MiscData):
    await message.answer(
        text=(
            "<b>Здравствуйте</b>\n\n"
            "<i>Данный бот позволит узнать список всех актуальных мероприятий</i>\n\n"
            f"Для этого используйте /{TgBotCommands.events}"
        )
    )


@dp.message_handler(commands=TgBotCommands.events)
async def on_cmd_events(message: types.Message):
    event_docs = await db.event_collection.get_all_docs()
    events = [Event.parse_document(event_doc) for event_doc in event_docs]
    events = [event for event in events if event.end_dt >= datetime.utcnow()]

    if not events:
        text = "Пока что нет мероприятий"
    else:
        text = ":bookmark_tabs: Мероприятия:\n\n"
        for i, event in enumerate(events):
            i += 1
            text += (
                f"<b>{i}. {event.title}</b>\n"
                f"{event.description}\n\n"
                f"<a href='{settings.front_domain}/events/{event.int_id}'>Подробнее</a>\n"
                f"<i>Начало: {event.start_dt.date()}</i>\n"
                f"<i>Конец: {event.end_dt.date()}\n\n</i>"
            )
            pass
        text += (
            f"<i>Для подробностей скачайте наше <a href='{settings.front_domain}/'>мобильное приложение с нашего сайта</a></i>"
        )

    await message.answer(text=emojize(text), disable_web_page_preview=True)


@dp.message_handler(commands=TgBotCommands.site)
async def on_cmd_site(message: types.Message):
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb.insert(InlineKeyboardButton(
        text=emojize(":link: Наш сайт"),
        url="https://atoll.divarteam.ru/"
    ))
    await message.answer(
        "<i>Переходите на наш сайт</i>",
        reply_markup=kb,
        disable_web_page_preview=True
    )


@dp.message_handler(commands=TgBotCommands.echo)
async def on_cmd_echo(message: types.Message):
    await message.answer(message.text)


@dp.message_handler()
async def on_any_msg(message: types.Message):
    await message.answer(
        text="<i>Для общения с ботом используйте команды</i>"
    )


def import_handlers():
    log.info('handlers were imported')
