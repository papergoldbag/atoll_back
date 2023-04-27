import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils.executor import Executor

from atoll_back.cache_dir import CacheDir
from atoll_back.db.db import DB
from atoll_back.settings import Settings

settings = Settings()
db = DB(mongo_uri=settings.mongo_uri, mongo_db_name=settings.mongo_db_name)

bot = Bot(token=settings.tg_bot_token, parse_mode=ParseMode.HTML)
bot_storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=bot_storage, loop=asyncio.get_event_loop())
executor_ = Executor(dispatcher=dp, skip_updates=True)

cache_dir = CacheDir(settings.cache_dirpath)
