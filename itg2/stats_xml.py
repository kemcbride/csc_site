import os
import json
import pandas as pd


class HighScore(object):
    """ This is for a single "score" object from a Stats.xml """
    DELIM = ' · '
    def __init__(self, root):
        # root here is a HighScoreForASongAndSteps thing

        raw_song = root.find('Song')
        self.song = HighScore.DELIM.join([s for s in raw_song.attrib['Dir'].split('/')[1:] if s])
        self.song_title = self.song.split(HighScore.DELIM)[-1]

        score = root.find('HighScore')

        self.pct_score = float(score.find('PercentDP').text)*100
        self.grade = self.convert_to_grade(self.pct_score)

        self.modifiers = score.find('Modifiers').text

        # This is Actually !Not! the difficulty level / feet rating
        # This is machine dependent (****, A, D, C, etc.)
        self.tier = int(score.find('Grade').text[4:])

        seconds_survived = float(score.find('SurviveSeconds').text)
        self.song_length = '%02d:%02d' % divmod(seconds_survived, 60)

        self.difficulty = root.find('Steps').attrib['Difficulty']
        # also has StepsType = dance-single usually

        self.radar = {i.tag: i.text for i in score.find('RadarValues')}
        self.holdnotes = {i.tag: i.text for i in score.find('HoldNoteScores')}
        self.tapnotes = {i.tag: i.text for i in score.find('TapNoteScores')}

    def convert_to_grade(self, pct_score):
        """ see: https://gaming.stackexchange.com/questions/233873/what-is-the-grading-system-in-the-groove """
        if pct_score == 0.0:
            return 'F'
        if pct_score < 55.0:
            return 'D'
        elif pct_score < 60.0:
            return 'C-'
        elif pct_score < 64.0:
            return 'C'
        elif pct_score < 68.0:
            return 'C+'
        elif pct_score < 72.0:
            return 'B-'
        elif pct_score < 76.0:
            return 'B'
        elif pct_score < 80.0:
            return 'B+'
        elif pct_score < 83.0:
            return 'A-'
        elif pct_score < 86.0:
            return 'A'
        elif pct_score < 89.0:
            return 'A+'
        elif pct_score < 92.0:
            return 'S-'
        elif pct_score < 94.0:
            return 'S'
        elif pct_score < 96.0:
            return 'S+'
        elif pct_score < 98.0:
            return '🟊'
        elif pct_score < 99.0:
            return '🟊🟊'
        elif pct_score < 100.0:
            return '🟊🟊🟊'
        elif pct_score == 100.0:
            return '🟊🟊🟊🟊' # as if! bahaha
        return 'F'

    def to_dict(self):
        """ yes... """
        return self.__dict__

    def to_json(self):
        """This only works if all of self's properties are JSON serializable
        ie. they have to be like basic types - string, int, double, whatever.
        I tried to have it keept the root xml guy for example - that failed.
        """
        return json.dumps(self.to_dict())

    def to_csv(self):
        """ umm... this is like.. the idea... is that ...
        i can put this into a database and then that'd be really cool
        """

        # something like this: except wait! I wnat like, a whole bunch of scores,
        #... presumably
        return pd.Dataframe(self.to_dict()).to_csv()


class Stats(object):
    """ OK, so this is for like "a set of scores" or whatever i get from a Stats.xml"""
    def __init__(self, xml):
        # this looks at RecentScoresForASong or something...
        data = []
        for recent_highscore_raw in xml.getroot()[-3].getchildren():
            hs = HighScore(recent_highscore_raw)
            data.append(hs)
        self.scores = data


class AllStats(object):
    def __init__(self, paths_format='./itg2/data/{}/Stats.xml'):
        fpaths = [
            paths_format.format(f)
            for f in os.listdir('itg2/data') # maybe this should change lol
            if os.path.exists(paths_format.format(f))
            ]
        xmls = [ET.parse(datum) for datum in fpaths]
        response_out = {}
        for idx, fpath in enumerate(fpaths):
            fname = fpath.split('/')[2]
            response_out[fname] = Stats(xmls[idx])
        self.data = response_out
