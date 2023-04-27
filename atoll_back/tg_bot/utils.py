import emoji

from atoll_back.models import Event
from atoll_back.core import db
from atoll_back.services import get_user, get_team, get_teams, get_events

async def get_team_ids(useroid: str):
    team_ids = []
    for team in await get_teams():
        for uoid in team.user_oids:
            if useroid == uoid:
                team_ids += [team.oid]
    return team_ids

async def get_my_event(useroid: str):
    team_ids = await get_team_ids(useroid)
    if len(team_ids) == 0:
        return []
    else:
        my_events = list()
        events = await get_events()
        for event in events:
            for teamoid in event.team_oids:
                if teamoid in team_ids:
                    my_events += [event]
    return my_events

async def get_event_description(event: Event):
    text = emoji.emojize(f":timer_clock: <strong>Дата</strong>: {str(event.start_dt).split(' ')[0]}\n:party_popper: <strong>Название</strong>: {event.description} \n")
    if len(event.team_oids) == 0:
        text += emoji.emojize(f":Statue_of_Liberty: Пока команды не записались\n")
    else:
        for team_oids in event.team_oids:
            team = await get_team(id_=team_oids)
            text +=  emoji.emojize(f":people_holding_hands: {team.title}\n")
    return text