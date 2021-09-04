from peewee import *
import json
import datetime

secrets = json.loads(open('secrets.json').read())
db = MySQLDatabase(secrets['DB']['name'], user=secrets['DB']['user'], password=secrets['DB']['pw'])

COOLDOWN = datetime.timedelta(seconds=30)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    userid = CharField(max_length=255)


class Gacha(BaseModel):
    user = ForeignKeyField(User, backref='gacha', unique=True)
    count = IntegerField(default=0)
    last_run = DateTimeField(default=datetime.datetime.now())
    ticket = IntegerField(default=0)


def check_user(userid):
    user, created = User.get_or_create(userid=userid)
    if created:
        user_gacha = Gacha(user=user)
        user_gacha.save()
        user.save()
    return user


def check_gacha_cd(userid):
    user = check_user(userid)
    gacha = user.gacha[0]
    now = datetime.datetime.now()
    if gacha.last_run + COOLDOWN <= now:
        gacha.last_run = now
        gacha.count += 1
        gacha.save()
        return True
    else:
        return False


def initialize():
    with db:
        db.create_tables([User, Gacha])

