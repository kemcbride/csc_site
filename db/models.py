from peewee import *
import datetime
import os

MYSQL_HOST = os.environ.get("MARIADB_HOST")
MYSQL_DATABASE = os.environ.get("MARIADB_DATABASE")
MYSQL_USER = os.environ.get("MARIADB_USER")
MYSQL_PASSWORD = os.environ.get("MARIADB_PASSWORD")


CHART_KEY_MEMBERS = [
        'title', 'num_taps', 'num_holds',
        ]


def connect_to_db():
    print(MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD)
    mysql_db = MySQLDatabase(MYSQL_DATABASE, user=MYSQL_USER, charset='utf8mb4',
        password=MYSQL_PASSWORD, host=MYSQL_HOST)
    return mysql_db


class Song(Model):
    # This might seem dumb, but I'd like it to be like, use the stats.xml's surviveLength
    # as the "length" of the track. (can only do for passes)
    # i wish there was an easier way to get this stuff than by looking at the sm files
    # and oggs... :/
    id = AutoField()

    title = CharField(max_length=80)
    maintitle = CharField(max_length=80, null=True)
    subtitle = CharField(max_length=80, null=True)
    bpm = CharField(max_length=80, null=True)
    length = CharField(max_length=80, )
    artist = CharField(max_length=80, null=True)
    genre = TextField(null=True)

    class Meta:
        database = connect_to_db()
        indexes = (
                (('title', 'subtitle', 'length'), True),
                )


class Chart(Model):
    id = AutoField()

    song_id = ForeignKeyField(Song)
    title = CharField(max_length=80)
    steps_type = CharField(max_length=20)

    pack = CharField(max_length=80, null=True) # need sm source
    level = IntegerField(null=True)
    step_artist = CharField(max_length=80, null=True)
    banner = TextField(null=True)
    background = TextField(null=True)
    genre = TextField(null=True)

    taps = IntegerField()
    jumps = IntegerField()
    holds = IntegerField()
    mines = IntegerField()
    rolls = IntegerField()
    hands = IntegerField()

    class Meta:
        database = connect_to_db()
        indexes = (
                (('title', 'pack', 'steps_type', 'taps', 'jumps',
                    'holds', 'mines', 'rolls', 'hands',
                    ), True),
                )


class Score(Model):
    id = AutoField()

    chart_id = ForeignKeyField(Chart)
    grade = CharField(max_length=20)
    percent = FloatField()

    player_tag = CharField(max_length=4, null=True, default='LR')
    datetime = TextField(null=True)
    modifiers = CharField(max_length=120)

    ecfa_fantastic = IntegerField(null=True)
    fantastic = IntegerField()
    excellent = IntegerField()
    great = IntegerField()
    decent = IntegerField(null=True)
    wayoff = IntegerField(null=True)
    miss = IntegerField()

    ng = IntegerField()
    ok = IntegerField()

    class Meta:
        database = connect_to_db()
        indexes = (
                (('chart_id', 'percent', 'fantastic', 'excellent', 'great', 'miss'),
                    True),
                )

class TimelinePost(Model):
    id = AutoField()

    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = connect_to_db()
        indexes = (
                (('chart_id', 'percent', 'fantastic', 'excellent', 'great', 'miss'),
                    True),
                )

TABLES = [TimelinePost, Song, Chart, Score] # in order of dependency
