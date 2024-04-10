from mongoengine import *
from datetime import datetime

# class Task(Document):
#     posterId = ReferenceField('user.User', required=True)
#     performerIds = ReferenceField('user.User', required=False)
#     title = StringField(required=True)
#     description = StringField(required=True)
#     skillsRequired = ListField(StringField())
#     budget = FloatField(required=True)
#     duration = StringField(required=True)
#     taskType = StringField(required=True, choices=('job', 'task'))
#     parentId = ObjectIdField()
#     status = StringField(required=True, choices=('open', 'in progress', 'completed'))
#     proposals = ListField(ReferenceField('Proposal'))
#     createdAt = DateTimeField(default=datetime.now)
#     updatedAt = DateTimeField(default=datetime.now)

class Task(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    worker = ReferenceField('user.Tasker')
    requester = ReferenceField('user.Requester')
    subtasks = ListField(ReferenceField('self', reverse_delete_rule=PULL))  # List of subtasks
    status = StringField(required=False, choices=('open', 'in progress', 'completed'))
    # proposals = ListField(ReferenceField('Proposal'))

    def add_subtask(self, subtask):
        """ Adds a subtask to the current task. """
        self.subtasks.append(subtask)
        self.save()

    def remove_subtask(self, subtask):
        """ Removes a subtask from the current task. """
        if subtask in self.subtasks:
            self.subtasks.remove(subtask)
            self.save()

    @classmethod
    def get_by_id(cls, id):
        """ Retrieve a task by its ID, including all nested subtasks recursively. """
        return cls.objects(id=id).first()

    def __str__(self):
        return f"{self.name}"