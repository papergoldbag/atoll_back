from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status, Depends, Body

from atoll_back.api.deps import get_strict_current_user, make_strict_depends_on_roles
from atoll_back.api.schema import InTeamUser, OperationStatusOut, SensitiveUserOut, TeamOut, UserOut, UpdateUserIn, \
    UserExistsStatusOut, \
    RegUserIn, AuthUserIn, EventOut, RatingOut, EventRequestIn, EventRequestOut
from atoll_back.consts import MailCodeTypes, UserRoles
from atoll_back.core import db
from atoll_back.db.event import EventFields
from atoll_back.db.user import UserFields
from atoll_back.models import User, Event, Team, Timeline
from atoll_back.services import get_user, get_mail_codes, create_mail_code, generate_token, create_user, get_users, \
    remove_mail_code, update_user, get_events, get_ratings, get_teams, get_team, get_event, create_event_request, \
    get_event_requests, get_event_request, event_request_to_event, create_team
from atoll_back.utils import send_mail

api_v1_router = APIRouter(prefix="/v1")


@api_v1_router.get("/healthcheck")
async def healthcheck():
    return {"working": True}


"""REGISTRATION"""


@api_v1_router.get("/reg.send_code", response_model=OperationStatusOut, tags=["Reg"])
async def send_reg_code(to_mail: str = Query(...)):
    user = await get_user(mail=to_mail)
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is not None")

    mail_code = await create_mail_code(
        to_mail=to_mail,
        type_=MailCodeTypes.reg
    )

    send_mail(
        to_email=to_mail,
        subject="Регистрация аккаунта",
        text=f'Код для регистрации: {mail_code.code}\n'
    )

    return OperationStatusOut(is_done=True)


@api_v1_router.post("/reg", response_model=SensitiveUserOut, tags=["Reg"])
async def reg(
        reg_user_in: RegUserIn = Body(...)
):
    mail_codes = await get_mail_codes(to_mail=reg_user_in.mail, code=reg_user_in.code)
    if not mail_codes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not mail_codes")
    if len(mail_codes) != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not mail_codes")
    mail_code = mail_codes[-1]

    await remove_mail_code(to_mail=mail_code.to_mail, code=mail_code.code)

    if mail_code.to_user_oid is not None:
        user = await get_user(id_=mail_code.to_user_oid)
        if user is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is not None")

    user = await create_user(mail=reg_user_in.mail, auto_create_at_least_one_token=True)

    # TODO: tg notify

    return SensitiveUserOut.parse_dbm_kwargs(
        **user.dict(),
        current_token=user.misc_data["created_token"]
    )


"""AUTH"""


@api_v1_router.get("/auth.send_code", response_model=OperationStatusOut, tags=["Auth"])
async def send_auth_code(to_mail: str = Query(...)):
    user = await get_user(mail=to_mail)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is None")

    mail_code = await create_mail_code(
        to_mail=to_mail,
        type_=MailCodeTypes.auth,
        to_user_oid=user.oid
    )

    send_mail(
        to_email=mail_code.to_mail,
        subject="Вход в аккаунт",
        text=f'Код для входа: {mail_code.code}\n'
    )
    return OperationStatusOut(is_done=True)


@api_v1_router.post("/auth", response_model=SensitiveUserOut, tags=["Auth"])
async def auth(
        auth_user_in: AuthUserIn = Body()
):
    mail_codes = await get_mail_codes(to_mail=auth_user_in.mail, code=auth_user_in.code)
    if not mail_codes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not mail_codes")
    if len(mail_codes) != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="len(mail_codes) != 1")
    mail_code = mail_codes[-1]

    await remove_mail_code(to_mail=mail_code.to_mail, code=mail_code.code)

    if mail_code.to_user_oid is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="mail_code.to_user_oid is None")

    user = await get_user(id_=mail_code.to_user_oid)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user is None")

    token = generate_token()
    await db.user_collection.update_document_by_id(id_=user.oid, push={UserFields.tokens: token})
    user.tokens.append(token)

    # TODO: tg notify

    return SensitiveUserOut.parse_dbm_kwargs(
        **user.dict(),
        current_token=token
    )


"""ME"""


@api_v1_router.get("/me", response_model=SensitiveUserOut, tags=["Me"])
async def get_me(user: User = Depends(get_strict_current_user)):
    return SensitiveUserOut.parse_dbm_kwargs(
        **user.dict(),
        current_token=user.misc_data["current_token"]
    )


@api_v1_router.post('/me.update', response_model=SensitiveUserOut, tags=['Me'])
async def me_update(update_user_in: UpdateUserIn, user: User = Depends(get_strict_current_user)):
    update_user_data = update_user_in.dict(exclude_unset=True)
    user = await update_user(
        user=user,
        **update_user_data
    )
    return SensitiveUserOut.parse_dbm_kwargs(
        **user.dict(),
        current_token=user.misc_data["current_token"]
    )


@api_v1_router.get("/me.invite", tags=["Me"], deprecated=True)
async def get_my_team_requests(user: User = Depends(get_strict_current_user)):
    ...


@api_v1_router.get("/me.accept_invite", tags=["Me"], deprecated=True)
async def get_my_team_requests(user: User = Depends(get_strict_current_user)):
    ...


@api_v1_router.post('/me.create_invite', response_model=OperationStatusOut, tags=['Me'], deprecated=True)
async def me_update(user: User = Depends(get_strict_current_user)):
    ...


"""USER"""


@api_v1_router.get('/user.mail_exists', response_model=UserExistsStatusOut, tags=['User'])
async def user_mail_exists(mail: str = Query(...)):
    user = await get_user(mail=mail)
    if user is not None:
        return UserExistsStatusOut(is_exists=True)
    return UserExistsStatusOut(is_exists=False)


@api_v1_router.get('/user.find', response_model=list[UserOut], tags=['User'])
async def find_user_by_name(q: str = Query(...), user: User = Depends(get_strict_current_user)):
    q = q.lower().strip()

    similar: list[UserOut] = []
    for user in await get_users():
        if user.fullname is not None and q in user.fullname.lower().strip():
            similar.append(UserOut.parse_dbm_kwargs(**user.dict()))
        elif user.mail is not None and q in user.mail.lower().strip():
            similar.append(UserOut.parse_dbm_kwargs(**user.dict()))

    return similar


@api_v1_router.get('/user.all', response_model=list[UserOut], tags=['User'])
async def get_all_users(user: User = Depends(get_strict_current_user)):
    return [UserOut.parse_dbm_kwargs(**user.dict()) for user in await get_users()]


@api_v1_router.get('/user.by_id', response_model=Optional[UserOut], tags=['User'])
async def get_user_by_int_id(int_id: int, user: User = Depends(get_strict_current_user)):
    user = await get_user(id_=int_id)
    if user is None:
        return None
    return UserOut.parse_dbm_kwargs(**user.dict())


@api_v1_router.post('/user.team_request', response_model=OperationStatusOut, tags=['User'], deprecated=True)
async def send_team_invite():
    ...


@api_v1_router.post('/user.edit_role', response_model=OperationStatusOut, tags=['User'], deprecated=True)
async def edit_user_role():
    ...


"""TEAM"""


@api_v1_router.get('/team.all', tags=['Team'])
async def get_all_teams():
    return await get_teams()


@api_v1_router.get('/team.get_by_int_id', response_model=Optional[TeamOut], tags=['Team'])
async def get_team_by_id(int_id: int = Query(...)):
    team = await get_team(id_=int_id)
    if team is None:
        return None
    team_dict = team.dict()
    team_dict['users'] = [
        InTeamUser.parse_dbm_kwargs(
            **(await get_user(id_=x)).dict(), is_captain=True if x == team_dict['captain_oid'] else False)
        for x in team_dict['user_oids']
    ]
    team_dict.pop('user_oids')
    return TeamOut.parse_dbm_kwargs(**team_dict)


"""EVENT"""


@api_v1_router.get('/event.all', response_model=list[EventOut], tags=['Event'])
async def get_all_events(user: User = Depends(get_strict_current_user)):
    events = await get_events()
    events_out = []
    for event in events:
        event_d = event.dict()
        event_d['team_oids'] = [str(x) for x in event.team_oids]
        ratings = await get_ratings(event_oid=event.oid)
        events_out.append(EventOut.parse_dbm_kwargs(**event_d, ratings=ratings))


    return events_out


@api_v1_router.get("/event.join", response_model=TeamOut, tags=["Me"])
async def event_join(
        user: User = Depends(make_strict_depends_on_roles(roles=[UserRoles.sportsman])),
        event_int_id: int = Query(...)
):
    event = await get_event(id_=event_int_id)
    if event is None:
        raise HTTPException(status_code=404, detail=f"event with int id {event_int_id} doesn't exists")
    event_teams = event.team_oids
    for team_oid in event_teams:
        team_e = await get_team(id_=team_oid)
        if user.oid in team_e.user_oids:
            raise HTTPException(status_code=400, detail="u already in event in team")
    team = await create_team(
        captain_oid=user.oid,
        title=user.fullname + " team",
        description=""
    )
    team.users = [InTeamUser.parse_dbm_kwargs(**u.dict(), is_captain=u.oid==team.captain_oid) for u in team.users]
    await db.event_collection.update_document_by_id(id_=event.oid, push={EventFields.team_oids:team.oid})
    return TeamOut.parse_dbm_kwargs(**(team.dict()))


@api_v1_router.get('/event.get_by_int_id', response_model=Optional[EventOut], tags=['Event'])
async def get_event_by_id(int_id: int = Query(...), user: User = Depends(get_strict_current_user)):
    event = await get_event(id_=int_id)
    if event is None:
        return None
    event_dict = event.dict()
    return EventOut.parse_dbm_kwargs(**event_dict, ratings=await get_ratings(event_oid=event_dict['oid']))


@api_v1_router.post('/event.publish_ratings', tags=['Rating'], deprecated=True)
async def publish_ratings():
    ...


@api_v1_router.post('/event.send_feedback', tags=['Event'], deprecated=True)
async def send_feedback():
    ...


@api_v1_router.get('/event.feedbacks', tags=['Event'], deprecated=True)
async def get_event_feedbacks(
        event_int_id: int = Query(...)
):
    ...


@api_v1_router.get('/event.get_all_requests_to_create_event', tags=['Event'], response_model=list[EventRequestOut])
async def get_all_event_requests(
        user: User = Depends(
            make_strict_depends_on_roles([UserRoles.admin])
        )
):
    ev_req = await get_event_requests()
    return [EventRequestOut.parse_dbm_kwargs(**event.dict()) for event in
            ev_req]


@api_v1_router.post('/event.requests_to_create_event', tags=['Event'], response_model=EventRequestOut)
async def add_event_requests(
        event_data: EventRequestIn = Body(...),
        user: User = Depends(
            make_strict_depends_on_roles([UserRoles.admin, UserRoles.representative, UserRoles.partner]))
):
    req = await create_event_request(
        title=event_data.title,
        description=event_data.description,
        requestor_oid=user.oid,
        start_dt=event_data.start_dt,
        end_dt=event_data.end_dt,
        timeline=[Timeline(dt=t.dt, text=t.text) for t in event_data.timeline],
    )
    return EventRequestOut.parse_dbm_kwargs(**(req.dict()))


@api_v1_router.get('/event.accept_request_to_create', tags=['Event'], response_model=EventOut)
async def accept_event_request(
        event_request_int_id: int = Query(...),
        user: User = Depends(
            make_strict_depends_on_roles([UserRoles.admin]))
):
    ev_req = await get_event_request(id_=event_request_int_id)
    if ev_req is None:
        raise HTTPException(status_code=400, detail=f"event request with int id {event_request_int_id} doesn't exists")
    event = await event_request_to_event(event_request_oid=ev_req.oid)
    return EventOut.parse_dbm_kwargs(**(event.dict()), ratings=await get_ratings(event_oid=event.oid))
