from mongoengine import *

class Skill(Document):
    meta = {'collection': 'skills'}
    name = StringField(required=True)