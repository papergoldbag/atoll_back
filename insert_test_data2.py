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


    for i in range(5):
        tu1 = await db.user_collection.insert_document({
            'fullname': "Sportsman1_{i}",
            'mail': f"tu1_{i}@test.ru",
            'tokens': [],
            'birth_dt': None,
            'tg_username': "",
            'tg_id': "",
            'vk_id': "",
            'roles': [UserRoles.sportsman],
            'description': ""
        })
        tu2 = await db.user_collection.insert_document({
            'fullname': "Sportsman2_{i}",
            'mail': f"tu2_{i}@test.ru",
            'tokens': [],
            'birth_dt': None,
            'tg_username': "",
            'tg_id': "",
            'vk_id': "",
            'roles': [UserRoles.sportsman],
            'description': ""
        })
        tu3 = await db.user_collection.insert_document({
            'fullname': "Sportsman3_{i}",
            'mail': f"tu3_{i}@test.ru",
            'tokens': [],
            'birth_dt': None,
            'tg_username': "",
            'tg_id': "",
            'vk_id': "",
            'roles': [UserRoles.sportsman],
            'description': ""
        })
        tteam = await db.team_collection.insert_document({
            'captain_oid': tu1['oid'],
            'title': f'test team {i}',
            'description': f"team with {tu1['fullname']} {tu2['fullname']} {tu3['fullname']}",
            'user_oids': [tu1['oid'],tu2['oid'],tu3['oid'],]
        })
        tevent = await db.event_collection.insert_document({
            'title': f'event_{i}',
            'description': 'event {i}',
            'team_oids': [tteam['oid']],
            'start_dt': datetime.now(),
            'end_dt': datetime.now() + timedelta(days=1),
            'timeline': [Timeline(dt=datetime.now(),text="старт"), Timeline(dt=datetime.now() + timedelta(days=1), text="конец")],
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
    'title': 'Всероссийский хакатон фсп 2023 Воронеж',
    'description': 'Всероссийский хакатон фсп для студентов',
    'team_oids': [],
    'start_dt': datetime.now(),
    'end_dt': datetime.now() + timedelta(days=2),
    'timeline': [
        Timeline(dt=datetime.now(),text="старт"), 
        Timeline(dt=datetime.now() + timedelta(days=1), text="чекпоинт"), 
        Timeline(dt=datetime.now() + timedelta(days=2), text="конец")],
    })
    await db.event_collection.insert_document({
    'title': 'Тестовый хакатон 2023',
    'description': 'Тестовый хакатон для теста',
    'team_oids': [],
    'start_dt': datetime.now(),
    'end_dt': datetime.now() + timedelta(days=3),
    'timeline': [
        Timeline(dt=datetime.now(),text="старт"), 
        Timeline(dt=datetime.now() + timedelta(days=1), text="чекпоинт"),
        Timeline(dt=datetime.now() + timedelta(days=2), text="чекпоинт"), 
        Timeline(dt=datetime.now() + timedelta(days=3), text="конец"), ],
    })


if __name__ == '__main__':
    asyncio.run(insert_test_data())
