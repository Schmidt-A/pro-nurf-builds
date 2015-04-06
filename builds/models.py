from django.db.models import *
from mongoengine import *

# Create your models here.

class Game(Document):
    game_id = IntegerField()

class Post(Document):
    title = StringField()
    text = StringField()

