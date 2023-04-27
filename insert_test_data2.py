import asyncio
from datetime import datetime

from bson import ObjectId

from atoll_back.consts import UserRoles
from atoll_back.core import db
from atoll_back.log import setup_logging
from atoll_back.services import create_user, create_team, create_event, create_rating


async def insert_test_data():
    setup_logging()
    # await db.drop_collections(only_using=False)
    # await db.ensure_all_indexes()

    # await create_rating(
    #     event_oid=ObjectId("644a948bc018c1bc08743148"),
    #     team_oid=ObjectId("644acf57ce14e2b756623e05"),
    #     place=1
    # )
    # await create_rating(
    #     event_oid=ObjectId("644a948bc018c1bc08743148"),
    #     team_oid=ObjectId("644ab1b7a9a83e916ab24f5e"),
    #     place=2
    # )

    # sportsman1 = await create_user(
    #     fullname="Спортсмен 1",
    #     mail="test1@gmail.com",
    #     roles=UserRoles.admin
    # )
    # sportsman2 = await create_user(
    #     fullname="Спортсмен 2",
    #     mail="test2@gmail.com",
    #     roles=UserRoles.sportsman
    # )
    # partner = await create_user(
    #     fullname="Партнёр",
    #     mail="test3@gmail.com",
    #     roles=UserRoles.partner
    # )
    # representative=  await create_user(
    #     fullname="Представитель",
    #     mail="test4@gmail.com",
    #     roles=UserRoles.representative
    # )
    # admin = await create_user(
    #     fullname="Админ",
    #     mail="test5@gmail.com",
    #     roles=UserRoles.admin
    # )
    #
    # team1 = await create_team(
    #     captain_oid=sportsman1.oid,
    #     title='Команда 1',
    #     description='Описание 1',
    #     user_oids=[sportsman1.oid, sportsman2.oid]
    # )
    #
    # await create_event(
    #     title='Title 1',
    #     description="Desc 1",
    #     team_oids=[team1.oid],
    #     end_dt=datetime.utcnow(),
    #     author_oid=admin.oid
    # )


if __name__ == '__main__':
    asyncio.run(insert_test_data())
