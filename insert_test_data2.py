import asyncio
from datetime import datetime, timedelta

from bson import ObjectId

from atoll_back.consts import UserRoles
from atoll_back.core import db
from atoll_back.log import setup_logging
from atoll_back.models import Timeline
from atoll_back.services import create_user, create_team, create_event, create_rating


async def insert_test_data():
    setup_logging()

    await db.user_collection.insert_document({
        'fullname': "Arsen",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.admin],
        'description': ""
    })

    
    await db.user_collection.insert_document({
        'fullname': "Rustam",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })
    await db.user_collection.insert_document({
        'fullname': "Ilya",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })
    await db.user_collection.insert_document({
        'fullname': "Denchik",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })
    await db.user_collection.insert_document({
        'fullname': "Ivanya",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })

    
    await db.user_collection.insert_document({
        'fullname': "Sportsman1",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })
    await db.user_collection.insert_document({
        'fullname': "Sportsman2",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })
    await db.user_collection.insert_document({
        'fullname': "Sportsman3",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })


    await db.user_collection.insert_document({
        'fullname': "Repr1",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.representative],
        'description': ""
    })
    await db.user_collection.insert_document({
        'fullname': "Part1",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.partner],
        'description': ""
    })


    await db.user_collection.insert_document({
        'fullname': "Dev1",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.dev],
        'description': ""
    })


    await db.event_collection.insert_document({
    'title': '',
    'description': '',
    'team_oids': [],
    'start_dt': datetime.now(),
    'end_dt': datetime.now() + timedelta(days=1),
    'timeline': [Timeline(dt=datetime.now(),text="старт")],
    })


if __name__ == '__main__':
    asyncio.run(insert_test_data())
