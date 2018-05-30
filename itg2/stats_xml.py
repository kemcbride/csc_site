import os
import sys
import json
import pandas as pd


class HighScore(object):
    """ This is for a single "score" object from a Stats.xml
    Attributes:
     - song
       ~ long-form "nicely" delimited song path
     - song_title
     - song_length
     - difficulty
     - steps_type
     - datetime
       ~ usually not accurate, since arcade machines often have wonky time
     - pct_score
     - grade
     - modifiers
     - radar
       ~ dict of the num of Holds, Taps, Mines, Rolls, Hands, Jumps for the chart
     - hold_notes
       ~ dict of NG/OK for Hold arrows
     - tap_notes
       ~ dict of timing scores for the score. (Excellent, Fantastic, etc.)
       * these actually use DDR terms [ Marvelous, Perfect, Great, Good, Boo, Miss ]
    """
    DELIM = ' · '
    def __init__(self, root):
        if root.tag == "HighScoreForASongAndSteps": # recent scores
            self._hs4song_n_steps_init(root)

        elif root.tag == "Song": # top scores
            succeeded = self._song_init(root)
            if not succeeded:
                raise KeyError('Failed to find HighScore in _song_init')

        else:
            raise ValueError('Unknown Root Tag: {}'.format(root.tag))

    def _hs4song_n_steps_init(self, root):
        self._song_title_init(root.find('Song'))
        self._difficuty_steps_init(root.find('Steps'))

        score = root.find('HighScore')
        self._hs_init(score)

    def _song_init(self, root):
        """ This function actually returns something,
        since it can fail (or, i have observed it possibly failing
        """
        self._song_title_init(root)
        
        song_steps = root.getchildren()[0]
        self._difficuty_steps_init(song_steps)

        hiscore_list = song_steps.getchildren()[0]
        hiscore = hiscore_list.find('HighScore')
        if hiscore is None:
            print('Failed to find HighScore in hiscorelist '
                'element for song {}'.format(self.song_title),
                file=sys.stderr)
            # we want to skip this song if we couldn't find it,
            # it probably means I didn't pass it lol
            return False

        self._hs_init(hiscore)
        return True

    def _hs_init(self, score):
        self.pct_score = float(score.find('PercentDP').text)*100
        self.grade = self.pct_to_grade(self.pct_score)

        self.modifiers = score.find('Modifiers').text

        self.datetime = score.find('DateTime').text

        # This is Actually !Not! the difficulty level / feet rating
        # This is machine dependent (****, A, D, C, etc.)
        # TODO: ValueError when "Failed" instead of eg "Tier11"
        # self.tier = int(score.find('Grade').text[4:])

        seconds_survived = float(score.find('SurviveSeconds').text)
        self.song_length = '%02d:%02d' % divmod(seconds_survived, 60)

        self.radar = {i.tag: i.text for i in score.find('RadarValues')}
        self.holdnotes = {i.tag: i.text for i in score.find('HoldNoteScores')}
        self.tapnotes = {i.tag: i.text for i in score.find('TapNoteScores')}

    def _song_title_init(self, song_node):
        song_path_str = song_node.get('Dir')
        song_path_str.replace('-R21READY', '') # if it has this substring, please, delete it.
        song_path_str = song_path_str.split('/')[1:]

        self.song = HighScore.DELIM.join([s for s in song_path_str if s])
        self.song_title = self.song.split(HighScore.DELIM)[-1]

    def _difficuty_steps_init(self, steps_node):
        self.difficulty = steps_node.get('Difficulty')
        self.steps_type = steps_node.get('StepsType') # generally dance-single

    def pct_to_grade(self, pct_score):
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
            return bytes('Star', 'utf-8')
        elif pct_score < 99.0:
            return bytes('Double Star', 'utf-8')
        elif pct_score < 100.0:
            return bytes('Tri-Star', 'utf-8')
        elif pct_score == 100.0:
            return bytes('Quad', 'utf-8') # as if! bahaha
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
