# from peewee import *
import json
import datetime
import random
from playhouse.migrate import *
# from playhouse.pool import PooledMySQLDatabase
import helper

secrets = json.loads(open('secrets.json').read())
db = MySQLDatabase(secrets['DB']['name'], user=secrets['DB']['user'], password=secrets['DB']['pw'])

COOLDOWN = datetime.timedelta(seconds=1)


def ensure_connection(f):
    def wrapper(*args, **kwargs):
        db.connect()
        result = f(*args, **kwargs)
        db.close()
        return result
    return wrapper


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
    star_6 = IntegerField(default=0)
    last_run = DateTimeField(default=datetime.datetime.now())
    banned_until = DateTimeField(default=datetime.datetime.now() - datetime.timedelta(days=1))
    rate_penalty = DoubleField(default=1)
    ticket = IntegerField(default=0)


class Gacha2(Gacha):
    user = ForeignKeyField(User, backref='gacha2', unique=True)


class DuckSong(BaseModel):
    user = ForeignKeyField(User, backref='songlist')
    link = CharField()
    vid = CharField(default='')


class Food(BaseModel):
    user = ForeignKeyField(User, backref='foodlist')


def check_user(userid, username):
    user, created = User.get_or_create(userid=userid)
    if created:
        user_gacha = Gacha(user=user)
        user_gacha.last_run = datetime.datetime.now() - datetime.timedelta(hours=1)
        user_gacha.save()
        user_gacha2 = Gacha2(user=user)
        user_gacha2.last_run = datetime.datetime.now() - datetime.timedelta(hours=1)
        user_gacha2.save()
        user.username = username
        user.save()
    else:
        if user.username != username:
            user.username = username
            user.save()
        if user.gacha2.count() == 0:
            user_gacha2 = Gacha2(user=user)
            user_gacha2.last_run = datetime.datetime.now() - datetime.timedelta(hours=1)
            user_gacha2.save()
            user.save()
    return user


@ensure_connection
def check_gacha_cd(userid, username):
    user = check_user(userid, username)
    gacha = user.gacha2[0]
    now = datetime.datetime.now()
    if gacha.banned_until > now:
        return -1
    if gacha.last_run + COOLDOWN <= now:
        gacha.last_run = now
        num = random.random()
        result = 0
        atari = 0.01 * gacha.rate_penalty
        if num < atari:
            if num < atari * 0.2:
                result = 6
                gacha.star_6 += 1
            else:
                result = 5
                gacha.star_5 += 1
        elif num < atari + 0.06:
            result = 4
            gacha.star_4 += 1
        elif num < atari + 0.21:
            result = 3
            gacha.star_3 += 1
        elif num < atari + 0.71:
            result = 2
            gacha.star_2 += 1
        else:
            result = 1
            gacha.star_1 += 1
        gacha.count += 1
        gacha.save()
        return result
    else:
        return 0


@ensure_connection
def gacha_stats(userid, username, season=1):
    user = check_user(userid, username)
    if season == 1:
        return user.gacha[0]
    elif season == 2:
        return user.gacha2[0]


@ensure_connection
def add_ducksong(url, userid, username):
    flag = False
    user = check_user(userid, username)
    vid = helper.get_youtube_id(url)
    song = DuckSong.get_or_none(vid=vid)
    if not song:
        song = DuckSong.create(user=user, link=url, vid=vid)
        flag = True
        song.save()
    return flag


@ensure_connection
def get_ducksong():
    songs = DuckSong.select()
    song = songs[int(random.random() * len(songs))]
    return song.link


def initialize():
    with db:
        db.create_tables([Gacha2])


def migration():
    migrator = MySQLMigrator(db)
    user = ForeignKeyField(User, backref='gacha2', unique=True, null=True)
    migrate(
        migrator.add_column('gacha2', 'user', user)
    )
