import json

# This is in a Stats.xml
class HighScore(object):
    def __init__(self, root):
        # root here is a HighScoreForASongAndSteps thing

        raw_song = root.find('Song')
        self.song = ' - '.join([s for s in raw_song.attrib['Dir'].split('/')[1:] if s])

        score = root.find('HighScore')

        self.pct_score = float(score.find('PercentDP').text)*100
        self.modifiers = score.find('Modifiers').text

        # This is Actually !Not! the difficulty level / feet rating
        # This is machine dependent (****, A, D, C, etc.)
        self.grade = int(score.find('Grade').text[4:])

        self.difficulty = root.find('Steps').attrib['Difficulty']
        # also has StepsType = dance-single usually

        self.radar = {i.tag: i.text for i in score.find('RadarValues')}
        self.holdnotes = {i.tag: i.text for i in score.find('HoldNoteScores')}
        self.tapnotes = {i.tag: i.text for i in score.find('TapNoteScores')}

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        """This only works if all of self's properties are JSON serializable
        ie. they have to be like basic types - string, int, double, whatever.
        I tried to have it keept the root xml guy for example - that failed.
        """
        return json.dumps(self.to_dict())
