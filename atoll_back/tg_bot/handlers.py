import logging

from aiogram import types

from atoll_back.consts import TgBotCommands
from atoll_back.core import dp

log = logging.getLogger(__name__)


@dp.message_handler(commands=TgBotCommands.start)
async def on_cmd_start(message: types.Message):
    await message.answer(message.text)


@dp.message_handler(commands=TgBotCommands.echo)
async def on_cmd_echo(message: types.Message):
    await message.answer(message.text)


def import_handlers():
    log.info('handlers were imported')
