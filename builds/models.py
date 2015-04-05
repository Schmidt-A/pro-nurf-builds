from django.db.models import *
from mongoengine import *

# Create your models here.

class Game(Document):
    game_id = IntegerField()
