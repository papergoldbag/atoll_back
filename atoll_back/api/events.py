import logging

from atoll_back.consts import UserRoles, Modes
from atoll_back.core import db, settings
from atoll_back.db.db import CannotConnectToDb
from atoll_back.services import send_from_tg_bot

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
        await send_from_tg_bot(text="API активен", to_roles=[UserRoles.dev, ])


async def on_shutdown(*args, **kwargs):
    if settings.mode == Modes.prod:
        await send_from_tg_bot(text="API не активен", to_roles=[UserRoles.dev, ])
