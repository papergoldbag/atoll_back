import pymongo

from atoll_back.db.base import BaseCollection, BaseFields


class FeedbackFields(BaseFields):
    event_id = "event_id"
    user_id = "user_id"
    text = "text"


class FeedbackCollection(BaseCollection):
    COLLECTION_NAME = "feedback"