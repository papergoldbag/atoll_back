from fastapi import APIRouter, HTTPException, Query, status, Depends

from atoll_back.api.deps import get_strict_current_user
from atoll_back.api.schema import OperationStatusOut, SensitiveUserOut, UserOut, UpdateUserIn, ExistsStatusOut, \
    UserExistsStatusOut
from atoll_back.consts import MailCodeTypes
from atoll_back.core import db
from atoll_back.db.user import UserFields
from atoll_back.models import User
from atoll_back.services import get_user, get_mail_codes, create_mail_code, generate_token, create_user, get_users, \
    remove_mail_code, update_user
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
        mail: str = Query(...),
        code: str = Query(...)
):
    mail_codes = await get_mail_codes(to_mail=mail, code=code)
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

    user = await create_user(mail=mail, auto_create_at_least_one_token=True)

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
        mail: str = Query(...),
        code: str = Query(...)
):
    mail_codes = await get_mail_codes(to_mail=mail, code=code)
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
    return [UserOut.parse_dbm_kwargs(x) for x in await get_users()]


@api_v1_router.get('/user.by_id', response_model=UserOut, tags=['User'])
async def get_user_by_int_id(int_id: int, user: User = Depends(get_strict_current_user)):
    return UserOut.parse_dbm_kwargs(**(await get_user(id_=int_id)).dict())

