import emoji

from atoll_back.models import Event
from atoll_back.core import db

# def return_user_keyboard(role: str):
#     if role == "sportsman":
#         return SportsmanKeyboard
#     elif role == "admin":
#         return AdminKeyboard
#     elif role == "representative":
#         return RepresentativeKeyboard
#     elif role == "partner":
#         return PartnerKeyboard
    
async def get_event_description(event: Event):
    text = emoji.emojize(f":timer_clock: <strong>Дата</strong>: {str(event.start_dt).split(' ')[0]}\n:party_popper: <strong>Название</strong>: {event.description} \n")
    if len(event.team_oids) == 0:
        text += emoji.emojize(f":Statue_of_Liberty: Пока команды не записались\n")
    else:
        for team in event.team_oids:
            text +=  emoji.emojize(f":people_holding_hands: {team}\n")
    user = await db.user_collection.find_document_by_oid(event.author_oid)
    return text