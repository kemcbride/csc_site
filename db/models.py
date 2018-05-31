from peewee import *

with open('/users/ke2mcbri/ceo-mysql-info', 'r') as f:
    for line in f:
        if line.startswith('Password'):
            MYSQL_PASSWORD = line.split()[-1]
            break

CHART_KEY_MEMBERS = [
        'title', 'num_taps', 'num_holds',
        ]


MYSQL_DB = MySQLDatabase('ke2mcbri', user='ke2mcbri', charset='utf8mb4',
        password=MYSQL_PASSWORD, host='caffeine')


class Song(Model):
    # This might seem dumb, but I'd like it to be like, use the stats.xml's surviveLength
    # as the "length" of the track. (can only do for passes)
    # i wish there was an easier way to get this stuff than by looking at the sm files
    # and oggs... :/
    id = AutoField()

    title = CharField(max_length=80)
    subtitle = CharField(max_length=80, null=True)
    bpm = CharField(max_length=80, null=True)
    length = CharField(max_length=80, )
    artist = CharField(max_length=80, null=True)

    class Meta:
        database = MYSQL_DB
        indexes = (
                (('title', 'subtitle', 'length'), True),
                )


class Chart(Model):
    id = AutoField()

    song_id = ForeignKeyField(Song)
    pack = CharField(max_length=80, null=True)
    level = IntegerField(null=True) # only available from catalog.xml
    title = CharField(max_length=80) # probably "Expert Single"
    steps_type = CharField(max_length=20) # i pretty much never play doubles...
    step_artist = CharField(max_length=80, null=True) # need sm source :|

    num_taps = IntegerField()
    num_jumps = IntegerField()
    num_holds = IntegerField()
    num_mines = IntegerField()
    num_rolls = IntegerField()
    num_hands = IntegerField()

    class Meta:
        database = MYSQL_DB
        indexes = (
                (('title', 'pack', 'steps_type', 'num_taps', 'num_jumps',
                    'num_holds', 'num_mines', 'num_rolls', 'num_hands',
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

    num_ecfa_fantastic = IntegerField(null=True)
    num_fantastic = IntegerField()
    num_excellent = IntegerField()
    num_great = IntegerField()
    num_decent = IntegerField(null=True)
    num_wayoff = IntegerField(null=True)
    num_miss = IntegerField()

    class Meta:
        database = MYSQL_DB
        indexes = (
                (('percent', 'num_fantastic', 'num_excellent', 'num_great', 'num_miss'),
                    True),
                )
