import json
import xml.etree.ElementTree as ET

from itg2.stats_xml import HighScore
import db.models as models
from db.models import Song, Chart, Score, mysql_db


DATA_FILE = '/users/ke2mcbri/www/app/itg2/data/greenguy/Stats.xml'

if __name__ == '__main__':
    xml = ET.parse(DATA_FILE)
    root = xml.getroot()
    
    with mysql_db:

        # Song, Chart, Score
        mysql_db.create_tables([Song, Chart, Score])

    for song_highscore in root[-3].getchildren():
        hs = HighScore(song_highscore)

        with mysql_db:
            this_song = Song.create(
                    title=hs.song_title,
                    length=hs.song_length
                    )

        with mysql_db:
            this_chart = Chart.create(
                    song_id=this_song,
                    title=hs.difficulty,
                    num_taps=hs.radar['Taps'],
                    )

        with mysql_db:
            this_score = Score.create(
                    chart_id=this_chart,
                    grade=hs.grade,
                    percent=hs.pct_score,
                    modifiers=hs.modifiers,

                    num_fantastic=hs.tapnotes['Marvelous'],
                    num_excellent=hs.tapnotes['Perfect'],
                    num_great=hs.tapnotes['Great'],
                    num_decent=hs.tapnotes['Good'],
                    num_wayoff=hs.tapnotes['Boo'],
                    num_miss=hs.tapnotes['Miss'],
                    )
