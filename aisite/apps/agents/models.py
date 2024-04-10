from mongoengine import *

class Agent(Document):
    meta = {'collection': 'agents'}
    name = StringField(required=True)
    img = StringField(required=True)