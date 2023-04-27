from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Extra


class BaseSchema(BaseModel):
    class Config:
        extra = Extra.ignore
        arbitrary_types_allowed = True
        allow_population_by_field_name = True


class BaseSchemaOut(BaseSchema):
    misc: dict[str, Any] = {}


class BaseOutDBMSchema(BaseSchemaOut):
    oid: str
    int_id: int
    created: datetime


class BaseSchemaIn(BaseSchema):
    pass


class RatingOut(BaseOutDBMSchema):
    event_oid: str
    place: int
    team_oid: str


class TimelineOut(BaseModel):
    dt: datetime
    text: str


class EventOut(BaseOutDBMSchema):
    title: str
    description: str 
    team_ods: Optional[list[str]] 
    author_oid: str 
    start_dt: datetime
    end_dt: datetime 
    timeline: list[TimelineOut]


class TeamOut(BaseOutDBMSchema):
    captain_oid: str
    title: str
    description: str
    user_oids: list[str]


class InviteOut(BaseOutDBMSchema):
    from_team_oid: str
    to_user_oid: str


class EventRequestOut(BaseOutDBMSchema):
    title: str
    description: str
    requestor_oid: str
    start_dt: datetime
    end_dt: datetime
    timeline: list[TimelineOut]


class FeedbackOut(BaseOutDBMSchema):
    event_oid: str
    user_oid: str
    text: str


class UserOut(BaseOutDBMSchema):
    fullname: Optional[str] = None
    mail: str
    birth_dt: Optional[datetime] = None
    tg_username: Optional[str] = None
    tg_id: Optional[str] = None
    roles: list[str] = []


class SensitiveUserOut(UserOut):
    tokens: list[str]
    current_token: str


class OperationStatusOut(BaseSchemaOut):
    is_done: bool


class ExistsStatusOut(BaseSchemaOut):
    is_exists: bool


class UpdateUserIn(BaseSchemaIn):
    fullname: Optional[str] = None
    birth_dt: Optional[datetime] = None
    tg_username: Optional[str] = None


class UserExistsStatusOut(BaseSchemaOut):
    is_exists: bool


class RegUserIn(BaseSchemaIn):
    mail: str
    code: str


class AuthUserIn(BaseSchemaIn):
    mail: str
    code: str
