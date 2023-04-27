import logging
from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from atoll_back.core import dp
from atoll_back.models import User
from atoll_back.services import get_user, update_user


@dataclass(frozen=True, kw_only=True)
class MiscData:
    user: User


class Initiator(BaseMiddleware):
    # TODO: авто обновление tg_username, если user в базе есть

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)

    async def __do(self, tg_user: types.User, data: dict):
        user = await get_user(tg_id=tg_user.id)

        if user is not None and user.tg_username != tg_user.username:
            await update_user(
                user=user,
                tg_username=tg_user.username
            )
            # TODO: tg notify

        misc_data = MiscData(user=user)
        data["misc"] = misc_data

    async def on_pre_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        self.log.info('on_pre_process_callback_query')
        await self.__do(tg_user=cq.from_user, data=data)

    async def on_pre_process_message(self, m: types.Message, data: dict):
        self.log.info('on_pre_process_message')
        await self.__do(tg_user=m.from_user, data=data)


def setup_middleware():
    dp.setup_middleware(Initiator())
