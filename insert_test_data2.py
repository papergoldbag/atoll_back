import asyncio
from datetime import datetime, timedelta

from bson import ObjectId

from atoll_back.consts import UserRoles
from atoll_back.core import db
from atoll_back.log import setup_logging
from atoll_back.models import Event, Team, Timeline, User
from atoll_back.services import create_user, create_team, create_event, create_rating


async def insert_test_data():
    setup_logging()
    await db.user_collection.drop_collection()
    
    await db.user_collection.insert_document({
        'fullname': "Arsen",
        'mail': "sabarsenrash@gmail.com",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "arpakit",
        'tg_id': "269870432",
        'vk_id': "",
        'roles': [UserRoles.admin],
        'description': ""
    })

    
    await db.user_collection.insert_document({
        'fullname': "Rustam",
        'mail': "recrea.tor@yandex.ru",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "rcr_tg",
        'tg_id': "373740493",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })
    await db.user_collection.insert_document({
        'fullname': "Ilya",
        'mail': "ilyakhakimov03@gmail.com",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "pirat2003",
        'tg_id': "1525214974",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })
    await db.user_collection.insert_document({
        'fullname': "Denchik",
        'mail': "dbarov3@gmail.com",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "brightos",
        'tg_id': "426220634",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })
    await db.user_collection.insert_document({
        'fullname': "Ivanya",
        'mail': "ermolovivan2018@gmail.com",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "ivan_20190721",
        'tg_id': "457643251",
        'vk_id': "",
        'roles': [UserRoles.sportsman],
        'description': ""
    })


    for i in range(5):
        tu1: User = User.parse_document(await db.user_collection.insert_document({
            'fullname': "Sportsman1_{i}",
            'mail': f"tu1_{i}@test.ru",
            'tokens': [],
            'birth_dt': None,
            'tg_username': "",
            'tg_id': "",
            'vk_id': "",
            'roles': [UserRoles.sportsman],
            'description': ""
        }))
        tu2: User = User.parse_document(await db.user_collection.insert_document({
            'fullname': "Sportsman2_{i}",
            'mail': f"tu2_{i}@test.ru",
            'tokens': [],
            'birth_dt': None,
            'tg_username': "",
            'tg_id': "",
            'vk_id': "",
            'roles': [UserRoles.sportsman],
            'description': ""
        }))
        tu3: User = User.parse_document(await db.user_collection.insert_document({
            'fullname': "Sportsman3_{i}",
            'mail': f"tu3_{i}@test.ru",
            'tokens': [],
            'birth_dt': None,
            'tg_username': "",
            'tg_id': "",
            'vk_id': "",
            'roles': [UserRoles.sportsman],
            'description': ""
        }))
        tteam: Team = Team.parse_document(await db.team_collection.insert_document({
            'captain_oid': tu1.oid,
            'title': f'test team {i}',
            'description': f"team with {tu1.fullname} {tu2.fullname} {tu3.fullname}",
            'user_oids': [tu1.oid, tu2.oid, tu3.oid,]
        }))
        tevent = Event.parse_document(await db.event_collection.insert_document({
            'title': f'event_{i}',
            'description': 'event {i}',
            'team_oids': [tteam.oid],
            'start_dt': datetime.now(),
            'end_dt': datetime.now() + timedelta(days=1),
            'timeline': [Timeline(dt=datetime.now(),text="старт").dict(), 
                         Timeline(dt=datetime.now() + timedelta(days=1), text="конец").dict()],
        }))


    await db.user_collection.insert_document({
        'fullname': "Тестовый представитель",
        'mail': "",
        'tokens': [],
        'birth_dt': None,
        'tg_username': "no exists",
        'tg_id': "",
        'vk_id': "",
        'roles': [UserRoles.representative],
        'description': ""
    })
    await db.user_collection.insert_document({
        'fullname': "Тестовый Партнер",
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
        Timeline(dt=datetime.now(),text="старт").dict(), 
        Timeline(dt=datetime.now() + timedelta(days=1), text="чекпоинт").dict(), 
        Timeline(dt=datetime.now() + timedelta(days=2), text="конец").dict()],
    })
    await db.event_collection.insert_document({
    'title': 'Тестовый хакатон 2023',
    'description': 'Тестовый хакатон для теста',
    'team_oids': [],
    'start_dt': datetime.now(),
    'end_dt': datetime.now() + timedelta(days=3),
    'timeline': [
        Timeline(dt=datetime.now(),text="старт").dict(), 
        Timeline(dt=datetime.now() + timedelta(days=1), text="чекпоинт").dict(),
        Timeline(dt=datetime.now() + timedelta(days=2), text="чекпоинт").dict(), 
        Timeline(dt=datetime.now() + timedelta(days=3), text="конец").dict(), ],
    })


if __name__ == '__main__':
    asyncio.run(insert_test_data())
