import asyncio
from datetime import datetime

from bson import ObjectId

from atoll_back.consts import UserRoles
from atoll_back.core import db
from atoll_back.log import setup_logging
from atoll_back.services import create_user, create_team, create_event, create_rating


async def insert_test_data():
    setup_logging()

    # create client role = [admin]

    # create client role = [sportsman]
    # create client role = [sportsman]
    # create client role = [sportsman]
    # create client role = [sportsman]
    # create client role = [sportsman]
    # create client role = [sportsman]
    # create client role = [sportsman]
    # create client role = [sportsman]

    # create client role = [representative]

    # create client role = [partner]

    # create client role = [dev]

    # create


if __name__ == '__main__':
    asyncio.run(insert_test_data())
