from peewee import *

with open('/users/ke2mcbri/ceo-mysql-info', 'r') as f:
    for line in f:
        if line.startswith('Password'):
            MYSQL_PASSWORD = line.split()[-1]
            break

CHART_KEY_MEMBERS = [
        'song_id', 'title',
        'num_taps', 'num_jumps', 'num_rolls',
        'num_hands', 'num_holds', 'num_mines',
        ]


MYSQL_DB = MySQLDatabase('ke2mcbri', user='ke2mcbri', charset='utf8mb4',
        password=MYSQL_PASSWORD, host='caffeine')


class Song(Model):
    # This might seem dumb, but I'd like it to be like, use the stats.xml's surviveLength
    # as the "length" of the track. (can only do for passes)
    # i wish there was an easier way to get this stuff than by looking at the sm files
    # and oggs... :/
    title = CharField(max_length=80, primary_key=True)
    pack = CharField(max_length=80, null=True)
    subtitle = CharField(max_length=80, null=True)
    bpm = CharField(max_length=80, null=True)
    length = CharField(max_length=80, )
    artist = CharField(max_length=80, null=True) # really cutting it down here, huh...

    class Meta:
        database = MYSQL_DB

class Chart(Model):
    song_id = ForeignKeyField(Song, backref='chart_song')
    level = IntegerField(null=True) # only available from catalog.xml
    title = CharField(max_length=80) # probably "Expert Single"
    num_taps = IntegerField()
    num_jumps = IntegerField()
    num_holds = IntegerField()
    num_mines = IntegerField()
    num_rolls = IntegerField()
    num_hands = IntegerField()
    step_artist = CharField(max_length=80, null=True) # need sm source :|

    class Meta:
        database = MYSQL_DB
        primary_key = CompositeKey(*CHART_KEY_MEMBERS)


# player_tag = CharField(max_length=4, null=True)
QUOTE_FMTED_CHART_KEY_MEMBERS = ', '.join(f'`{c}`' for c in CHART_KEY_MEMBERS)
SCORE_FK_CONSTRAINT = (
    'CONSTRAINT fk_score_chart_song FOREIGN KEY '
    f'({QUOTE_FMTED_CHART_KEY_MEMBERS})'
    ' REFERENCES '
    f'chart({QUOTE_FMTED_CHART_KEY_MEMBERS})'
    )
class Score(Model):
    grade = CharField(max_length=20)
    percent = FloatField()
    modifiers = CharField(max_length=120)
    num_ecfa_fantastic = IntegerField(null=True)
    num_fantastic = IntegerField()
    num_excellent = IntegerField()
    num_great = IntegerField()
    num_decent = IntegerField(null=True)
    num_wayoff = IntegerField(null=True)
    num_miss = IntegerField()

    song_id = CharField(max_length=80)
    title = CharField(max_length=80)
    num_taps = IntegerField()
    num_jumps = IntegerField()
    num_holds = IntegerField()
    num_mines = IntegerField()
    num_rolls = IntegerField()
    num_hands = IntegerField()

    class Meta:
        database = MYSQL_DB
        primary_key = CompositeKey('percent',
                'num_fantastic', 'num_excellent',
                'num_great', 'num_miss')
        constraints = [
                SQL(SCORE_FK_CONSTRAINT),
            ]
