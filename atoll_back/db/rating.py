from atoll_back.db.base import BaseCollection, BaseFields


class RatingFields(BaseFields):
    team_oid = "team_oid"
    place = "place"


class RatingCollection(BaseCollection):
    COLLECTION_NAME = "team"
