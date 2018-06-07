import sys

import xml.etree.ElementTree as ET


TIMING_TERMS = {
        'Marvelous': 'Fantastic',
        'Perfect':   'Excellent',
        'Great':     'Great',
        'Good':      'Decent',
        'Boo':       'Wayoff',
        'Miss':      'Miss',
        }


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

    The following attributes are added if you 'update_from_catalog':
     - level
     - main_title
       ~ what the machine shows as the title
     - sub_title
       ~ what the machine shows as the subtitle
    """
    DELIM = ' · '
    def __init__(self, root):
        self.level = -1
        self.maintitle = ''
        self.subtitle = ''
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

        self.modifiers = score.find('Modifiers').text

        self.datetime = score.find('DateTime').text

        # This is Actually !Not! the difficulty level / feet rating
        # This is machine dependent (****, A, D, C, etc.)
        self.passed = not score.find('Grade').text.startswith('Fail')
        self.grade = self.pct_to_grade(self.pct_score)

        seconds_survived = float(score.find('SurviveSeconds').text)
        self.song_length = '%02d:%02d' % divmod(seconds_survived, 60)

        self.radar = {i.tag: i.text for i in score.find('RadarValues')}
        self.holdnotes = {i.tag: i.text for i in score.find('HoldNoteScores')}
        self.tapnotes = {i.tag: i.text for i in score.find('TapNoteScores')}

    def _song_title_init(self, song_node):
        self.dir = song_node.get('Dir')
        song_path_str = song_node.get('Dir')
        song_path_str.replace('-R21READY', '') # if it has this substring, please, delete it.
        song_path_str = song_path_str.split('/')[1:]
        self.cat_dir = '/'.join(song_path_str[1:])

        self.song = HighScore.DELIM.join([s for s in song_path_str if s])
        self.song_title = self.song.split(HighScore.DELIM)[-1]

    def _difficuty_steps_init(self, steps_node):
        self.difficulty = steps_node.get('Difficulty')
        self.steps_type = steps_node.get('StepsType') # generally dance-single

    def pct_to_grade(self, pct_score):
        """ see: https://gaming.stackexchange.com/questions/233873/what-is-the-grading-system-in-the-groove """
        if pct_score == 0.0 or not self.passed:
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
            return '*'
        elif pct_score < 99.0:
            return '**'
        elif pct_score < 100.0:
            return '***'
        elif pct_score == 100.0:
            return '****'
        return 'F'

    # ! NOTE! see catalog classes comments/
    # this function is useless. not ready to kill it yet though :(
    def update_from_catalog(self, catalog):
        try:
            song = catalog.songs[self.cat_dir]
            print (song)
            steps = catsong[self.steps_type][self.difficulty]

            self.level = steps.level
            self.maintitle = song.maintitle
            self.subtitle = song.subtitle
        except KeyError:
            print('{} not found in catalog.'.format(self.song_title),
                    file=sys.stderr)
            print('{}: {}'.format(self.cat_dir, self.cat_dir in catalog.songs.keys()),
                    file=sys.stderr)


class TopScores(object):
    def __init__(self, stats_file):
        self.stats_xml = stats_file

        xml = ET.parse(stats_file)
        root = xml.getroot()
        records = []
        for song in root.find('SongScores').getchildren():
            try:
                hs = HighScore(song)
                records.append(hs)
            except KeyError:
                continue
        self.scores = records


class RecentScores(object):
    def __init__(self, stats_file):
        self.stats_xml = stats_file

        xml = ET.parse(stats_file)
        root = xml.getroot()
        records = []
        for song in root.find('RecentSongScores').getchildren():
            try:
                hs = HighScore(song)
                records.append(hs)
            except KeyError:
                continue
        self.scores = records


###
# !NOTE: seems like the catalog is useles unless we already know what pack
#     a given song is from. oh well...
# like, at that point, might as well just use the raw sm source data.
###

class CatalogSteps(object):
    def __init__(self, steps):
        self.difficulty = steps.get('Difficulty')
        self.steps_type = steps.get('StepsType')
        self.level = int(steps.find('Meter').text)
        self.radar = {i.tag: i.text for i in steps.find('RadarValues')}


class CatalogSong(object):
    def __init__(self, song):
        self.dir = song.get('Dir')

        self.maintitle = song.find('MainTitle').text
        self.subtitle = song.find('SubTitle').text
        self.steps = {
                'dance-single': {},
                'dance-double': {},
                }
        for steps in song.findall('Steps'):
            steps = song.find('Steps')
            difficulty = steps.get('Difficulty')
            steps_type = steps.get('StepsType')
            self.steps[steps_type][difficulty] = CatalogSteps(steps)


class Catalog(object):
    def __init__(self, catalog_file):
        self.catalog_xml = catalog_file

        xml = ET.parse(catalog_file)
        root = xml.getroot()
        self.songs = {}
        for song in root.find('Songs').getchildren():
            self.songs[song.get('Dir')] = CatalogSong(song)
