from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from atoll_back.core import dp
from atoll_back.services import get_user


class RoleFilter(BoundFilter):
    key = "roles"

    def __init__(self, roles: Union[list[str], str]):
        if isinstance(roles, str):
            roles = [roles]
        self.roles = roles

    async def check(self, update: Union[types.Message, types.CallbackQuery]) -> bool:
        client = await get_user(tg_id=update.from_user.id)
        if client is None:
            return False
        return client.compare_roles(self.roles)


def setup_filters():
    dp.filters_factory.bind(RoleFilter)
