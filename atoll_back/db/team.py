import pymongo

from atoll_back.db.base import BaseCollection, BaseFields


class TeamFields(BaseFields):
    title = "title"
    description = "description"
    user_ids = "user_ids"


class TeamCollection(BaseCollection):
    COLLECTION_NAME = "team"