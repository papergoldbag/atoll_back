import logging

from atoll_back.core import db, settings, bot
from atoll_back.consts import UserRoles, Modes
from atoll_back.services import get_users, send_from_tg_bot
from atoll_back.db.db import CannotConnectToDb

log = logging.getLogger(__name__)


async def prepare_db():
    try:
        await db.check_conn()
    except CannotConnectToDb as e:
        log.exception(e)
        raise e
    await db.ensure_all_indexes()
    log.info("db conn is good")


async def on_startup(*args, **kwargs):
    await prepare_db()
    if settings.mode == Modes.prod:
        await send_from_tg_bot(text="API включен", to_roles=[UserRoles.admin,])


async def on_shutdown(*args, **kwargs):
    if settings.mode == Modes.prod:
        await send_from_tg_bot(text="API выключен", to_roles=[UserRoles.admin,])

