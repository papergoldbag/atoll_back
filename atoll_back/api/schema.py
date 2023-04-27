from datetime import datetime
from typing import Optional, Any

from bson import ObjectId
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

    @classmethod
    def parse_dbm_kwargs(
            cls,
            **kwargs
    ):
        res = {}
        for k, v in kwargs.items():
            if isinstance(v, ObjectId):
                v = str(v)
            res[k] = v
        return cls(**res)


class BaseSchemaIn(BaseSchema):
    pass


class Rating(BaseModel):
    place: str
    team_int_id: int


class Timeline(BaseModel):
    dt: datetime
    text: str


class EventOut(BaseOutDBMSchema):
    title: str
    description: str 
    team_ods: Optional[list[str]] 
    author_oid: str 
    start_dt: datetime
    end_dt: datetime 
    ratings: list[Rating] 
    timeline: list[Timeline] 



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
