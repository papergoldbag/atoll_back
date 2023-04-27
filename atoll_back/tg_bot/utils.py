import emoji

from atoll_back.models import Event
from atoll_back.core import db
from atoll_back.services import get_user

async def get_team_id(useroid: str):
    teams = db.team_collection.pymongo_collection.find({})
    team_id = -1
    for team in teams:
        print(team)
        for uoid in teams.user_oids:
            if useroid == uoid:
                return team.oid
    return None 

async def get_my_event(useroid: str):
    team_id = await get_team_id(useroid)
    if team_id is None:
        return []
    else:
        my_events = list()
        events = db.event_collection.pymongo_collection.find({})
        for event in events:
            for teamoid in event.team_oids:
                if teamoid == team_id:
                    my_events += [event]
    return my_events

async def get_event_description(event: Event):
    text = emoji.emojize(f":timer_clock: <strong>Дата</strong>: {str(event.start_dt).split(' ')[0]}\n:party_popper: <strong>Название</strong>: {event.description} \n")
    if len(event.team_oids) == 0:
        text += emoji.emojize(f":Statue_of_Liberty: Пока команды не записались\n")
    else:
        for team in event.team_oids:
            text +=  emoji.emojize(f":people_holding_hands: {team}\n")
    user = await db.user_collection.find_document_by_oid(event.author_oid)
    return text