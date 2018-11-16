""" Utility functions used to interact with garcia/simfile module live here.
"""


STEP_KEYS = ['1', '2', '4']


# TODO: test this... it can pretty easily be compared with Groovestats
def count_notes(notes):
    """ Take a simfile.chart's notes and return the counted "radar"
    (as in a Stats.xml, not as in the garcia/simfile object's radar)
    """
    taps = 0
    holds = 0
    jumps = 0
    hands = 0
    rolls = 0
    mines = 0

    hold_state = [False, False, False, False]
    for row in notes:
        line = row[1]
        curr_notes = len(list(filter(lambda s: s in STEP_KEYS, line)))
        # simultaneous notes resulting in a jump or hand
        if curr_notes >= 2:
            jumps += 1
            taps -= 1
        if curr_notes >= 3:
            hands += 1
            taps -= 1

        for idx, note in enumerate(line):
            curr_holds = len(list(filter(lambda s: s, hold_state)))
            # held notes resulting in a hand (doesn't count as jump if only 2)

            if note == '1':
                taps += 1
                if curr_holds > 2:
                    hands += 1
            elif note == '2':
                taps += 1
                holds += 1
                hold_state[idx] = True
                if curr_holds > 2:
                    hands += 1
            elif note == 'M':
                mines += 1
            elif note == '4':
                rolls += 1
                hold_state[idx] = True
                if curr_holds > 2:
                    hands += 1
            elif note == '3':
                hold_state[idx] = False
    return {
            'taps': taps,
            'holds': holds,
            'jumps': jumps,
            'hands': hands,
            'rolls': rolls,
            'mines': mines,
            }
