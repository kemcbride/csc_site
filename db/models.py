from peewee import *

with open('/users/ke2mcbri/ceo-mysql-info', 'r') as f:
    for line in f:
        if line.startswith('Password'):
            MYSQL_PASSWORD = line.split()[-1]
            break

mysql_db = MySQLDatabase('ke2mcbri', user='ke2mcbri', charset='utf8mb4',
        password=MYSQL_PASSWORD, host='caffeine')

class Song(Model):
    # This might seem dumb, but I'd like it to be like, use the stats.xml's surviveLength
    # as the "length" of the track.
    # i wish there was an easier way to get this stuff than by looking at the sm files
    # and oggs... :/
    id = PrimaryKeyField()
    title = CharField(max_length=80, )
    subtitle = CharField(max_length=80, null=True)
    bpm = CharField(max_length=80, null=True)
    length = CharField(max_length=80, )
    artist = CharField(max_length=80, null=True) # really cutting it down here, huh...

    class Meta:
        database = mysql_db


class Chart(Model):
    id = PrimaryKeyField()
    song_id = ForeignKeyField(Song)
    level = IntegerField(null=True) # only available from catalog.xml
    title = CharField(max_length=80) # probably "Expert Single"
    num_taps = IntegerField()
    num_mines = IntegerField(null=True) #jeez...
    step_artist = CharField(max_length=80, null=True) # can't be found easily w/out real source

    class Meta:
        database = mysql_db


class Score(Model):
    id = PrimaryKeyField()
    chart_id = ForeignKeyField(Chart)
    grade = CharField() # Grade
    percent = FloatField() # PercentDP
    # player_tag = CharField() # uhh haha apparently it isn't on stats.xml lol. whatever.
    modifiers = TextField(default='')
    num_ecfa_fantastic = IntegerField(null=True)
    num_fantastic = IntegerField()
    num_excellent = IntegerField()
    num_great = IntegerField()
    num_decent = IntegerField(null=True)
    num_wayoff = IntegerField(null=True)
    num_miss = IntegerField()

    class Meta:
        database = mysql_db
        # primary_key = CompositeKey('percent',
        #         'num_fantastic', 'num_excellent',
        #         'num_great', 'num_miss')
