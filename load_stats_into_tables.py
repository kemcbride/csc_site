import argparse
import xml.etree.ElementTree as ET

from itg2.stats_xml import HighScore
import db.models as models
from db.models import Song, Chart, Score, MYSQL_DB


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('stats_file', type=str)
    arguments = ap.parse_args()

    xml = ET.parse(arguments.stats_file)
    root = xml.getroot()

    # -1 for TopScores
    # -3 for RecentScores ( ??? ) (maybe? i don't remember???)
    for song in root[-1].getchildren():
        try:
            hs = HighScore(song)
        except KeyError:
            continue

        with MYSQL_DB:
            this_song = Song.create(
                    title=hs.song_title,
                    length=hs.song_length
                    )

        with MYSQL_DB:
            this_chart = Chart.create(
                    song_id=this_song,
                    title=hs.difficulty,
                    num_taps=hs.radar['Taps'],
                    num_jumps=hs.radar['Jumps'],
                    num_holds=hs.radar['Holds'],
                    num_mines=hs.radar['Mines'],
                    num_rolls=hs.radar['Rolls'],
                    num_hands=hs.radar['Hands'],
                    )

        with MYSQL_DB:
            this_score = Score.create(
                    grade=hs.grade,
                    percent=hs.pct_score,
                    modifiers=hs.modifiers,

                    num_fantastic=hs.tapnotes['Marvelous'],
                    num_excellent=hs.tapnotes['Perfect'],
                    num_great=hs.tapnotes['Great'],
                    num_decent=hs.tapnotes['Good'],
                    num_wayoff=hs.tapnotes['Boo'],
                    num_miss=hs.tapnotes['Miss'],

                    # foreign key things...
                    # since composite, peewee won't do it for me.
                    song_id=this_song,
                    title=hs.difficulty,
                    num_taps=hs.radar['Taps'],
                    num_jumps=hs.radar['Jumps'],
                    num_holds=hs.radar['Holds'],
                    num_mines=hs.radar['Mines'],
                    num_rolls=hs.radar['Rolls'],
                    num_hands=hs.radar['Hands'],
                    )
