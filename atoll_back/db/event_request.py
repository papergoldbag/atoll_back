from atoll_back.db.base import BaseCollection, BaseFields


class EventRequestFields(BaseFields):
    title = "title"
    description = "description"
    requestor_oid = "requestor_int_id"
    start_dt = "start_dt"
    end_dt = "end_dt"
    timeline = "timeline"


class EventRequestCollection(BaseCollection):
    COLLECTION_NAME = "event_request"
