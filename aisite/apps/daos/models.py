from mongoengine import *

class Dao(Document):
    meta = {'collection': 'daos'}
    name = StringField(required=True)