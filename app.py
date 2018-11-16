import os
import json

from jinja2 import Template
import cherrypy

from itg2.stats_xml import HighScore
from peewee import MySQLDatabase
from db.models import connect_to_db, Song, Chart, Score

from util import (
    STATIC_PATH,
    KODONODO_DIRS,
    linkify,
    make_static_config
)

APP_PATH = os.path.abspath(os.path.dirname(__file__))

PORT = 25777 # high but not 28000-28500
TMPL_FMT = 'templates/{}.html.j2'
CTNT_FMT = 'content/{}.content.html'
CONFIG_DICT = {
    'global': {
        'server.socket_port': PORT,
        'server.socket_host': '129.97.134.72',  # caffeine
        'tools.caching.on': True,
        'tools.caching.delay': 3600,
    },
    STATIC_PATH: {
        'tools.staticdir.on': True,
        'tools.staticdir.root': STATIC_PATH,
        'tools.staticdir.dir': STATIC_PATH,
    },
}

for DIRNAME in KODONODO_DIRS:
    cfg = make_static_config(DIRNAME)
    print(cfg)
    CONFIG_DICT.update(cfg)



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
    def codenames_dirs(self):
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        static_path =  'static/codenames_pics'
        picpath = os.path.join(os.path.dirname(APP_PATH), static_path)
        entries = os.listdir(picpath)
        links = [linkify(e, 'codenames') for e in entries]
        return '\n'.join(links)

    @cherrypy.expose
    def codenames(self, path=''):
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        https = False
        
        if path.endswith('.txt'):  # HACK FOR CODONODOS:
            path = path[:-4]
        static_path_elements = [STATIC_PATH, 'codenames_pics', path]

        static_path = '/'.join(static_path_elements)
        picpath = os.path.join(os.path.dirname(APP_PATH), static_path)
        entries = os.listdir(picpath)
        links = [linkify(e, static_path, https=https) for e in entries]
        return '\n'.join(links)

    @cherrypy.expose
    def itg(self):
        db = connect_to_db()
        with db.atomic():
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
        db.close()
        tmpled_songs = []
        for record in results:
            tmpled_songs.append(template_highscore(record))

        content = ''.join(tmpled_songs)

        with open(TMPL_FMT.format('basic'), 'r') as tmpl_file:
            basic_template = Template(tmpl_file.read())
        return basic_template.render(content=content)


# I have no idea if this is necessary, but I'm leaving it here.
class FileServer(object):
    pass

if __name__ == '__main__':
    cherrypy.config.update(CONFIG_DICT)
    cherrypy.tree.mount(Website(), "/", config=CONFIG_DICT)
    cherrypy.tree.mount(FileServer(), STATIC_PATH, config=CONFIG_DICT)

    cherrypy.engine.start()
    cherrypy.engine.block()  # Allow the cherrypy server to restart itself on file update
