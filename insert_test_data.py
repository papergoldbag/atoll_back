
import asyncio
from datetime import datetime, timedelta

from bson import ObjectId

from atoll_back.core import db
from atoll_back.log import setup_logging
from atoll_back.models import Rating, Timeline
from atoll_back.services import create_user, create_event, get_users


async def insert_test_data():
    setup_logging()
    await db.event_collection.remove_documents()
    users = await get_users()
    await create_event(
        title="TEST",
        description="TEST",
        author_oid=users[0].oid,
        end_dt=datetime.utcnow() + timedelta(days=30),
        ratings=[Rating(team_oid=ObjectId(), place=1)],
        timelines=[Timeline(
            dt=datetime.utcnow(),
            text='TEST TEXT'
        )]
    )


if __name__ == '__main__':
    asyncio.run(insert_test_data())

