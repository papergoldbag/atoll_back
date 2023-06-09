import logging
from dataclasses import dataclass
from typing import Optional

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from atoll_back.core import dp, db
from atoll_back.db.user import UserFields
from atoll_back.models import User
from atoll_back.services import get_user, update_user


@dataclass(frozen=True, kw_only=True)
class MiscData:
    user: Optional[User]


class Initiator(BaseMiddleware):
    # TODO: авто обновление tg_username, если user в базе есть

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)

    async def __do(self, tg_user: types.User, data: dict):
        user = await get_user(tg_id=tg_user.id)
        if user is None:
            user_dor = await db.user_collection.find_document(filter_={UserFields.tg_username: tg_user.username})
            if user_dor is not None:
                user = User.parse_document(user_dor)

        if user is not None:
            await update_user(
                user=user,
                tg_username=tg_user.username,
                tg_id=tg_user.id
            )

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
