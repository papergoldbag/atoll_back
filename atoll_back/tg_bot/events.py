import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import BotCommand, BotCommandScopeChat
from emoji import emojize

from atoll_back.consts import UserRoles, TgBotCommands
from atoll_back.core import executor_, bot
from atoll_back.services import send_from_tg_bot

log = logging.getLogger(__name__)


async def set_commands():
    visible_commands = [
        BotCommand(TgBotCommands.events, emojize(":bookmark_tabs: События")),
        BotCommand(TgBotCommands.site, emojize(":link: Наш сайт"))
    ]
    await bot.set_my_commands(commands=visible_commands)
    log.info("tg commands were set")


async def on_startup(*args, **kwargs):
    await set_commands()
    await send_from_tg_bot(
        text=f"Telegram bot запущен",
        to_roles=[UserRoles.dev]
    )


async def on_shutdown(*args, **kwargs):
    await send_from_tg_bot(
        text=f"Telegram bot выключен",
        to_roles=[UserRoles.dev]
    )


def setup_events():
    executor_.on_startup(on_startup)
    executor_.on_shutdown(on_shutdown)
    log.info('events were setup')
