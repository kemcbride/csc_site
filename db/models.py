from peewee import *

with open('/users/ke2mcbri/ceo-mysql-info', 'r') as f:
    for line in f:
        if line.startswith('Password'):
            MYSQL_PASSWORD = line.split()[-1]
            break

CHART_KEY_MEMBERS = [
        'title', 'num_taps', 'num_holds',
        ]


def connect_to_db():
    mysql_db = MySQLDatabase('ke2mcbri', user='ke2mcbri', charset='utf8mb4',
            password=MYSQL_PASSWORD, host='caffeine')
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

    class Meta:
        database = connect_to_db()
        indexes = (
                (('title', 'subtitle', 'length'), True),
                )


class Chart(Model):
    id = AutoField()

    song_id = ForeignKeyField(Song)
    pack = CharField(max_length=80, null=True)
    level = IntegerField(null=True)
    title = CharField(max_length=80)
    steps_type = CharField(max_length=20)
    step_artist = CharField(max_length=80, null=True) # need sm source :|

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

    player_tag = CharField(max_length=4, null=True)
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
