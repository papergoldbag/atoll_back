import asyncio
import binascii
import os
from datetime import datetime
from random import randint
from typing import Union, Optional

import pymongo
from bson import ObjectId

from atoll_back.consts import UserRoles, RolesType
from atoll_back.core import db, bot
from atoll_back.db.base import Id
from atoll_back.db.mailcode import MailCodeFields
from atoll_back.db.user import UserFields
from atoll_back.helpers import NotSet, is_set
from atoll_back.models import User, MailCode
from atoll_back.utils import roles_to_list

"""USER LOGIC"""


async def update_user(
        *,
        user: Union[User, ObjectId],
        fullname: Union[NotSet, Optional[str]] = NotSet,
        birth_dt: Union[NotSet, Optional[datetime]] = NotSet,
        tg_id: Union[NotSet, Optional[int]] = NotSet,
        tg_username: Union[NotSet, Optional[str]] = NotSet
) -> User:
    if isinstance(user, User):
        pass
    elif isinstance(user, ObjectId):
        user = await get_user(id_=user)
    else:
        raise TypeError("bad type for user")

    if user is None:
        raise ValueError("user is None")

    set_ = {}
    if is_set(fullname):
        if fullname is not None:
            fullname = fullname.strip()
        set_[UserFields.fullname] = fullname
    if is_set(birth_dt):
        set_[UserFields.birth_dt] = birth_dt
    if is_set(tg_id):
        set_[UserFields.tg_id] = tg_id
    if is_set(tg_username):
        set_[UserFields.tg_username] = tg_username

    if set_:
        await db.user_collection.update_document_by_id(
            id_=user.oid,
            set_=set_
        )

        if is_set(fullname):
            user.fullname = fullname
        if is_set(birth_dt):
            user.birth_dt = birth_dt
        if is_set(tg_id):
            user.tg_id = tg_id
        if is_set(tg_username):
            user.tg_username = tg_username

    return user


def generate_token() -> str:
    res = binascii.hexlify(os.urandom(20)).decode() + str(randint(10000, 1000000))
    return res[:128]


async def create_user(
        *,
        fullname: Optional[str] = None,
        mail: str,
        tokens: Optional[list[str]] = None,
        auto_create_at_least_one_token: bool = True,
        birth_dt: Optional[datetime] = None,
        tg_username: Optional[str] = None,
        tg_id: Optional[int] = None,
        roles: RolesType = None
):
    if roles is None:
        roles = [UserRoles.sportsman]
    else:
        roles = roles_to_list(roles)

    created_token: Optional[str] = None
    if tokens is None:
        tokens = []
        if auto_create_at_least_one_token is True:
            created_token = generate_token()
            tokens.append(created_token)

    mail = mail.strip()

    if fullname is not None:
        fullname = fullname.strip()

    if tg_username is not None:
        tg_username = tg_username.strip()

    doc_to_insert = {
        UserFields.fullname: fullname,
        UserFields.mail: mail,
        UserFields.birth_dt: birth_dt,
        UserFields.tokens: tokens,
        UserFields.tg_username: tg_username,
        UserFields.tg_id: tg_id,
        UserFields.roles: roles
    }
    inserted_doc = await db.user_collection.insert_document(doc_to_insert)
    created_user = User.parse_document(inserted_doc)
    created_user.misc_data["created_token"] = created_token
    return created_user


async def get_user(
        *,
        id_: Optional[Id] = None,
        mail: Optional[str] = None,
        token: Optional[str] = None,
        tg_id: Union[NotSet, Optional[int]] = NotSet,
        tg_username: Union[NotSet, Optional[str]] = NotSet
) -> Optional[User]:
    filter_ = {}
    if id_ is not None:
        filter_.update(db.user_collection.create_id_filter(id_=id_))
    if mail is not None:
        filter_[UserFields.mail] = mail
    if token is not None:
        filter_[UserFields.tokens] = {"$in": [token]}
    if is_set(tg_id):
        filter_[UserFields.tg_id] = tg_id
    if is_set(tg_username):
        filter_[UserFields.tg_username] = tg_username

    if not filter_:
        raise ValueError("not filter_")

    doc = await db.user_collection.find_document(filter_=filter_)
    if doc is None:
        return None
    return User.parse_document(doc)


async def get_users(*, roles: Optional[list[str]] = None) -> list[User]:
    users = [User.parse_document(doc) async for doc in db.user_collection.create_cursor()]
    if roles is not None:
        users = [user for user in users if user.compare_roles(roles)]
    return users


async def remove_token(*, client_id: Id, token: str):
    await db.user_collection.motor_collection.update_one(
        db.user_collection.create_id_filter(id_=client_id),
        {'$pull': {UserFields.tokens: token}}
    )


"""TELEGRAM BOT LOGIC"""


async def send_from_tg_bot(*, text: str, to_roles: Optional[RolesType] = None, to_user_ids: Optional[list[Id]] = None):
    if to_roles is None:
        users_to_send = [await get_user(id_=id_) for id_ in to_user_ids]
    elif to_user_ids is None:
        users_to_send: list[User] = await get_users(roles=to_roles)
    else:
        raise ValueError("bad params")

    for user in users_to_send:
        if user.tg_id is None:
            continue
        await bot.send_message(
            chat_id=user.tg_id,
            text=text
        )


"""MAIL CODE LOGIC"""


async def remove_mail_code(
        *,
        id_: Optional[Id] = None,
        to_mail: Optional[str] = None,
        code: Optional[str] = None
):
    filter_ = {}
    if id_ is not None:
        filter_.update(db.mail_code_collection.create_id_filter(id_=id_))
    if to_mail is not None:
        filter_[MailCodeFields.to_mail] = to_mail
    if code is not None:
        filter_[MailCodeFields.code] = code

    if not filter_:
        raise ValueError("not filter_")

    await db.mail_code_collection.remove_document(
        filter_=filter_
    )


def _generate_mail_code() -> str:
    return str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9)) + str(randint(1, 9))


async def generate_unique_mail_code() -> str:
    mail_code = _generate_mail_code()
    while await db.mail_code_collection.document_exists(filter_={MailCodeFields.code: mail_code}):
        mail_code = _generate_mail_code()
    return mail_code


async def get_mail_codes(
        *,
        id_: Optional[Id] = None,
        to_mail: Optional[str] = None,
        code: Optional[str] = None,
        type_: Optional[str] = None,  # use MailCodeTypes
        to_user_oid: Union[NotSet, Optional[ObjectId]] = NotSet
) -> list[MailCode]:
    filter_ = {}
    if id_ is not None:
        filter_.update(db.mail_code_collection.create_id_filter(id_=id_))
    if to_mail is not None:
        filter_[MailCodeFields.to_mail] = to_mail
    if code is not None:
        filter_[MailCodeFields.code] = code
    if type_ is not None:
        filter_[MailCodeFields.type] = type_
    if is_set(to_user_oid):
        filter_[MailCodeFields.to_user_oid] = to_user_oid

    cursor = db.mail_code_collection.create_cursor(
        filter_=filter_,
        sort_=[(MailCodeFields.created, pymongo.DESCENDING)],
    )

    return [MailCode.parse_document(doc) async for doc in cursor]


async def create_mail_code(
        *,
        to_mail: str,
        code: str = None,
        type_: str,  # use MailCodeTypes
        to_user_oid: Optional[ObjectId] = None
) -> MailCode:
    to_user: Optional[User] = None
    if to_user_oid is not None:
        to_user = await get_user(id_=to_user_oid)
        if to_user is None:
            raise Exception("to_user is None")

    if code is None:
        code = await generate_unique_mail_code()

    doc_to_insert = {
        MailCodeFields.to_mail: to_mail,
        MailCodeFields.code: code,
        MailCodeFields.type: type_,
        MailCodeFields.to_user_oid: to_user_oid
    }
    inserted_doc = await db.mail_code_collection.insert_document(doc_to_insert)
    created_mail_code = MailCode.parse_document(inserted_doc)

    created_mail_code.to_user = to_user

    return created_mail_code


async def __example():
    await send_from_tg_bot(text='asfasf')


if __name__ == '__main__':
    asyncio.run(__example())
