from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ListField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ObjectIdField,
    PULL,
)
import bson


class SubTask(EmbeddedDocument):
    _id = ObjectIdField(default=bson.ObjectId, required=True)
    title = StringField(required=True)
    description = StringField(required=True)
    worker = ReferenceField("user.Tasker")
    requester = ReferenceField("user.Requester")
    status = StringField(required=False, choices=("open", "in progress", "completed"))
    tasks = ListField(EmbeddedDocumentField("self"), reverse_delete_rule=PULL)


class Task(Document):
    meta = {"collection": "tasks"}
    title = StringField(required=True)
    description = StringField(required=True)
    worker = ReferenceField("user.Tasker")
    requester = ReferenceField("user.Requester")
    status = StringField(required=False, choices=("open", "in progress", "completed"))
    tasks = ListField(EmbeddedDocumentField(SubTask), reverse_delete_rule=PULL)
