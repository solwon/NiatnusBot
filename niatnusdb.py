from peewee import *
import json
import datetime
import random

secrets = json.loads(open('secrets.json').read())
db = MySQLDatabase(secrets['DB']['name'], user=secrets['DB']['user'], password=secrets['DB']['pw'])

COOLDOWN = datetime.timedelta(seconds=5)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    userid = CharField(max_length=255)
    username = CharField(max_length=255, null=True)


class Gacha(BaseModel):
    user = ForeignKeyField(User, backref='gacha', unique=True)
    count = IntegerField(default=0)
    star_1 = IntegerField(default=0)
    star_2 = IntegerField(default=0)
    star_3 = IntegerField(default=0)
    star_4 = IntegerField(default=0)
    star_5 = IntegerField(default=0)
    last_run = DateTimeField(default=datetime.datetime.now())
    ticket = IntegerField(default=0)


class DuckSong(BaseModel):
    user = ForeignKeyField(User, backref='songlist')
    link = CharField()


def check_user(userid, username):
    user, created = User.get_or_create(userid=userid)
    if created:
        user_gacha = Gacha(user=user)
        user_gacha.last_run = datetime.datetime.now() - datetime.timedelta(hours=1)
        user_gacha.save()
        user.username = username
        user.save()
    else:
        if user.username != username:
            user.username = username
            user.save()
    return user


def check_gacha_cd(userid, username):
    user = check_user(userid, username)
    gacha = user.gacha[0]
    now = datetime.datetime.now()
    if gacha.last_run + COOLDOWN <= now:
        gacha.last_run = now
        num = random.random()
        result = 0
        if num < 0.305:
            result = 1
            gacha.star_1 += 1
        elif num < 0.805:
            result = 2
            gacha.star_2 += 1
        elif num < 0.955:
            result = 3
            gacha.star_3 += 1
        elif num < 0.995:
            result = 4
            gacha.star_4 += 1
        else:
            result = 5
            gacha.star_5 += 1
        gacha.count += 1
        gacha.save()
        return result
    else:
        return 0


def add_ducksong(url, userid, username):
    user = check_user(userid, username)
    song, created = DuckSong.get_or_create(user=user, link=url)
    song.save()


def get_ducksong():
    songs = DuckSong.select()
    song = songs[int(random.random() * len(songs))]
    return song.link


def initialize():
    with db:
        db.create_tables([DuckSong])

