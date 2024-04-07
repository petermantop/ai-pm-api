from mongoengine import *
from datetime import datetime

class Task(Document):
    posterId = ReferenceField('user.User', required=True)
    performerIds = ReferenceField('user.User', required=False)
    title = StringField(required=True)
    description = StringField(required=True)
    skillsRequired = ListField(StringField())
    budget = FloatField(required=True)
    duration = StringField(required=True)
    taskType = StringField(required=True, choices=('job', 'task'))
    parentId = ObjectIdField()
    status = StringField(required=True, choices=('open', 'in progress', 'completed'))
    proposals = ListField(ReferenceField('Proposal'))
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
