import os
import json
import xml.etree.ElementTree as ET

from jinja2 import Template
import cherrypy

from itg2.stats_xml import HighScore
from db.models import MYSQL_DB, Song, Chart, Score

PORT = 25777 # high but not 28000-28500
TMPL_FMT = 'templates/{}.html.j2'
CTNT_FMT = 'content/{}.content.html'
CONFIG_DICT = {
    'server.socket_port': PORT,
    'server.socket_host': '129.97.134.72',
    'tools.caching.on': True,
    'tools.caching.delay': 3600,
    }
cherrypy.config.update(CONFIG_DICT)


def template_highscore(record):
    with open(TMPL_FMT.format('stats_song'), 'r') as tmpl_file:
        song_template = Template(tmpl_file.read())
    return song_template.render(r=record)


class Website(object):
    @cherrypy.expose
    def index(self):
        with open(CTNT_FMT.format('index'), 'r') as content_file:
            index_content = content_file.read()

        with open(TMPL_FMT.format('basic'), 'r') as tmpl_file:
            basic_template = Template(tmpl_file.read())

        return basic_template.render(content=index_content)

    @cherrypy.expose
    def stuff(self):
        with open(CTNT_FMT.format('stuff'), 'r') as content_file:
            content = content_file.read()

        with open(TMPL_FMT.format('basic'), 'r') as tmpl_file:
            basic_template = Template(tmpl_file.read())
        return basic_template.render(content=content)

    @cherrypy.expose
    def itg(self):
        with MYSQL_DB.atomic():
            results = Song.select(
                    Song.title, Song.length,
                    Chart.title, Chart.taps, Chart.holds, 
                    Chart.jumps, Chart.mines, Chart.rolls,
                    Chart.hands,
                    Score.grade, Score.percent, Score.modifiers,
                    Score.fantastic, Score.excellent,
                    Score.great, Score.decent, Score.wayoff,
                    Score.miss, Score.ng, Score.ok,
                    ).join(Chart).join(Score).where(Score.percent >= 96.0
                            ).order_by(Score.percent.desc()).limit(10)

        tmpled_songs = []
        for record in results:
            tmpled_songs.append(template_highscore(record))

        content = ''.join(tmpled_songs)

        with open(TMPL_FMT.format('basic'), 'r') as tmpl_file:
            basic_template = Template(tmpl_file.read())
        return basic_template.render(content=content)


cherrypy.quickstart(Website())
