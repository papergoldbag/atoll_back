import pymongo

from atoll_back.db.base import BaseCollection, BaseFields


class InviteFields(BaseFields):
    from_team_id = "from_team_id"
    to_user_id = "to_user_id"


class InviteCollection(BaseCollection):
    COLLECTION_NAME = "invite"