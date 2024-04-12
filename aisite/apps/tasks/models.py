from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ListField,
    FloatField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ObjectIdField,
    BooleanField,
    PULL,
)
from ..user.models import Requester, Tasker
import bson


class Chat(EmbeddedDocument):
    message = StringField(required=True)
    response = StringField(required=True)
    is_final_outline = BooleanField(required=True)
    history = ListField()


class SubTask(EmbeddedDocument):
    _id = ObjectIdField(default=bson.ObjectId, required=True)
    title = StringField(required=True)
    description = StringField(required=True)
    requester = ReferenceField(Requester)
    worker = StringField()
    cost = FloatField()
    status = StringField(required=False, choices=("open", "in progress", "completed"))
    tasks = ListField(EmbeddedDocumentField("self"), reverse_delete_rule=PULL)


class Task(Document):
    meta = {"collection": "tasks"}
    title = StringField()
    description = StringField()
    requester = ReferenceField(Requester)
    worker = StringField()
    cost = FloatField()
    status = StringField(
        required=False, choices=("planning", "open", "in progress", "completed")
    )
    tasks = ListField(EmbeddedDocumentField(SubTask), reverse_delete_rule=PULL)
    chat = ListField(EmbeddedDocumentField(Chat))
