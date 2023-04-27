
import asyncio
from datetime import datetime, timedelta

from bson import ObjectId

from atoll_back.core import db
from atoll_back.log import setup_logging
from atoll_back.models import Rating, Timeline, Team
from atoll_back.services import create_user, create_event, get_users
from atoll_back.db.rating import RatingFields
from atoll_back.db.team import TeamFields


async def insert_test_data():
    setup_logging()
    await db.event_collection.remove_documents()
    await db.ensure_all_indexes()

    user = await create_user(fullname="abob1", mail="recrea.tor@yandex.ru")

    team1 = Team.parse_document(
        await db.team_collection.insert_document(
            {
                TeamFields.captain_oid: user.oid,
                TeamFields.title: "Divar",
                TeamFields.description: "Descr",
                TeamFields.user_oids: [user.oid] 
            }
        ))
    team2 = Team.parse_document(
        await db.team_collection.insert_document(
            {
                TeamFields.captain_oid: user.oid,
                TeamFields.title: "Divar",
                TeamFields.description: "Descr",
                TeamFields.user_oids: [user.oid] 
            }
        ))
    team3 = Team.parse_document(
        await db.team_collection.insert_document(
            {
                TeamFields.captain_oid: user.oid,
                TeamFields.title: "Divar3",
                TeamFields.description: "Descr3",
                TeamFields.user_oids: [user.oid] 
            }
        ))
    ev1 = await create_event(
        title="TEST",
        description="TEST",
        team_oids=[team1.oid, team2.oid, team3.oid],
        author_oid=user,
        end_dt=datetime.utcnow() + timedelta(days=30),
        timeline=[Timeline(
            dt=datetime.utcnow(),
            text='TEST TEXT'
        )]
    )

    await db.rating.insert_document({
        RatingFields.event_oid: ev1.oid,
        RatingFields.place: 1,
        RatingFields.team_oid: team1.oid
    })
    await db.rating.insert_document({
        RatingFields.event_oid: ev1.oid,
        RatingFields.place: 2,
        RatingFields.team_oid: team2.oid
    })
    await db.rating.insert_document({
        RatingFields.event_oid: ev1.oid,
        RatingFields.place: 2,
        RatingFields.team_oid: team2.oid
    })

    await create_event(
        title="TEST2",
        description="TEST22",
        author_oid=user,
        end_dt=datetime.utcnow() + timedelta(days=30),
        timeline=[Timeline(
            dt=datetime.utcnow(),
            text='TEST TEXT2'
        )]
    )
    
    await create_event(
        title="TEST3",
        description="TEST33",
        author_oid=user,
        end_dt=datetime.utcnow() + timedelta(days=30),
        timeline=[Timeline(
            dt=datetime.utcnow(),
            text='TEST TEXT3'
        )]
    )
    
    


if __name__ == '__main__':
    asyncio.run(insert_test_data())

