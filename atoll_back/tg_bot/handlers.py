import logging

from aiogram import types
from emoji import emojize

from atoll_back.consts import TgBotCommands
from atoll_back.core import dp, db
from atoll_back.models import Event
from atoll_back.services import get_events

import emoji

log = logging.getLogger(__name__)

async def get_event_description(event: Event):
    text = f":timer_clock: <strong>Дата</strong>: {str(event.start_dt).split(' ')[0]}\n:party_popper: <strong>Название</strong>: {event.description} \n"
    if len(event.team_oids) == 0:
        text += f":Statue_of_Liberty: Пока команды не записались\n"
    else:
        for team in event.team_oids:
            text +=  f":people_holding_hands: {team}\n"
    return text

@dp.message_handler(commands=TgBotCommands.start)
async def on_cmd_start(message: types.Message):
    await message.answer(message.text)


@dp.message_handler(commands=TgBotCommands.events)
async def on_cmd_events(message: types.Message):
    event_docs = await db.event_collection.get_all_docs()
    events = [Event.parse_document(event_doc) for event_doc in event_docs]

    text = ":bookmark_tabs: Мероприятия:\n"
    for event in events:
        text += await get_event_description(event)
    await message.answer(text=emojize(text))


@dp.message_handler(commands=TgBotCommands.site)
async def on_cmd_site(message: types.Message):
    await message.answer(message.text)


@dp.message_handler(commands=TgBotCommands.echo)
async def on_cmd_echo(message: types.Message):
    await message.answer(message.text)


def import_handlers():
    log.info('handlers were imported')
