from atoll_back.db.base import BaseCollection, BaseFields


class TeamFields(BaseFields):
    title = "title"
    description = "description"
    user_oids = "user_oids"


class TeamCollection(BaseCollection):
    COLLECTION_NAME = "team"
