import os
import json
import xml.etree.ElementTree as ET

from jinja2 import Template
import cherrypy

from itg2.stats_xml import HighScore

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


def template_highscore_song(xml):
    hs = HighScore(xml)
    with open(TMPL_FMT.format('stats_song'), 'r') as tmpl_file:
        song_template = Template(tmpl_file.read())

    return song_template.render(
        song_name=hs.song,
        pct_score=round(hs.pct_score, 2),
        mods=hs.modifiers,
        # difficulty_level=hs.grade, # not right
        difficulty=hs.difficulty,
        radar_values=hs.radar,
        hold_note_scores=hs.holdnotes,
        tap_note_scores=hs.tapnotes,
        )

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
        data = [
            './itg2/{}/Stats.xml'.format(f)
            for f in os.listdir('itg2')
            if os.path.exists('./itg2/{}/Stats.xml'.format(f))
            ]
        xmls = [ET.parse(datum) for datum in data]

        root = xmls[0].getroot()
        tmpled_songs = []
        for song_highscore in root[-3].getchildren():
            tmpled_songs.append(template_highscore_song(song_highscore))

        content = '<br>'.join(tmpled_songs)

        with open(TMPL_FMT.format('basic'), 'r') as tmpl_file:
            basic_template = Template(tmpl_file.read())
        return basic_template.render(content=content)

    @cherrypy.expose
    def itg_nice(self):
        data = [
            './itg2/{}/Stats.xml'.format(f)
            for f in os.listdir('itg2')
            if os.path.exists('./itg2/{}/Stats.xml'.format(f))
            ]
        xml = ET.parse(data[0])
        del data
        root = xml.getroot()
        hss = [HighScore(c) for c in root[-3].getchildren()]
        json_hss = '{ "highscores": [' + ','.join(hs.to_json() for hs in hss) + ']}'

        # Check it out: This is what I'll do:
        # - create indexed template spots that can use the JSON data (js)
        # - load the data on the page root template, and have the js access
        #     each element in [the list] based on the template index! easy!

        with open(TMPL_FMT.format('js_highscore'), 'r') as jstmpl_file:
            js_template = Template(jstmpl_file.read())
            print(js_template)

        # dogs = '<br>'.join([
        #     js_template.render(idx=i, song_name=hs.difficulty)
        #     for i, hs in enumerate(hss)
        #     ])
        dogs = js_template.render(idx=0, song_name='dog')

        with open(TMPL_FMT.format('itg_scores'), 'r') as tmpl_file:
            basic_template = Template(tmpl_file.read())
            print(js_template)
        return basic_template.render(scores_json=json_hss, content=dogs)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def itg_json(self):
        fpaths = [
            './itg2/{}/Stats.xml'.format(f)
            for f in os.listdir('itg2')
            if os.path.exists('./itg2/{}/Stats.xml'.format(f))
            ]
        xmls = [ET.parse(datum) for datum in fpaths]
        response_out = {}
        for idx, fpath in enumerate(fpaths):
            fname = fpath.split('/')[2]
            response_out[fname] = []

            for recent_highscore_raw in xmls[idx].getroot()[-3].getchildren():
                hs = HighScore(recent_highscore_raw)
                response_out[fname].append(hs.to_dict())
        return response_out



cherrypy.quickstart(Website())
