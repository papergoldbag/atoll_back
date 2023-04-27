import pymongo

from atoll_back.db.base import BaseCollection, BaseFields


class EventFields(BaseFields):
    title = "title"
    description = "description"
    requestor_id = "requestor_id"
    start_dt = "start_dt"
    end_dt = "end_dt"
    timeline = "timeline"


class EventCollection(BaseCollection):
    COLLECTION_NAME = "event"