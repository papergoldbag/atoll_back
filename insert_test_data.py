
import asyncio

from atoll_back.core import db
from atoll_back.log import setup_logging
from atoll_back.services import create_user


async def drop_db():
    setup_logging()
    await create_user(mail="mail@gmail.com", fullname="Test Test")


if __name__ == '__main__':
    asyncio.run(drop_db())

