from time import sleep
from asciimatics.screen import Screen
import re
import itertools
from collections import namedtuple, defaultdict
from pprint import pprint
from config import DEFAULT_BOARD
from operator import itemgetter

token_board = """+------------+------------+------------+------------+
|            |            |            |            |
|            |            |            |            |
|    2048    |    2048    |    2048    |    2048    |
|            |            |            |            |
|            |            |            |            |
+------------+------------+------------+------------+
|            |            |            |            |
|            |            |            |            |
|    2048    |    2048    |    2048    |    2048    |
|            |            |            |            |
|            |            |            |            |
+------------+------------+------------+------------+
|            |            |            |            |
|            |            |            |            |
|    2048    |    2048    |    2048    |    2048    |
|            |            |            |            |
|            |            |            |            |
+------------+------------+------------+------------+
|            |            |            |            |
|            |            |            |            |
|    2048    |    2048    |    2048    |    2048    |
|            |            |            |            |
|            |            |            |            |
+------------+------------+------------+------------+"""


Token = namedtuple("Token", ("ttype", "length"))

def s_plus(scanner, token): 
    return Token("+", len(token))


def s_minus(scanner, token): 
    return Token("-", len(token))


def s_bar(scanner, token): 
    return Token("|", len(token))


def s_space(scanner, token): 
    return Token(" ", len(token))


def s_num(scanner, token): 
    return Token("d", len(token))

scanner = re.Scanner([
    (r"[+]", s_plus),
    (r"[-]", s_minus),
    (r"\d", s_num),
    (r"\ +", s_space),
    (r"[\|]", s_bar),
])

token_starts = defaultdict(list)
for y, row in enumerate(token_board.splitlines(False)):
    row_tokens = scanner.scan(row)[0]
    ttypes = [t.ttype for t in row_tokens]
    tlens = [t.length for t in row_tokens]
    tstarts = [tx - 1 for tx in itertools.accumulate(tlens)]
    for ttype, x in zip(ttypes, tstarts):
        token_starts[ttype].append((x, y))

cur_starts = token_starts['d'][:]
token_starts['d'] = [c for i, c in enumerate(cur_starts)
                     if (c[0] - 1, c[1]) not in cur_starts]
del cur_starts

def print_board(screen):
    for ttype in ("+", "-", "|"):
        for x, y in token_starts[ttype]:
            screen.print_at(ttype, x, y)

def print_numbers(screen, state, ignore_zeros=False):
    digits = itertools.chain.from_iterable(state)
    for i, coord in enumerate(token_starts['d']):
        x, y = coord
        d = next(digits)
        if ignore_zeros and d == 0:
            pass
        else:
            screen.print_at("{:^4}".format(d),
                            x, y)

MOVES = {
    'quit':(ord('q'),ord('Q')),
    'up':(ord('i'),ord('I'),Screen.KEY_NUMPAD8,Screen.KEY_RIGHT),
    'down':(ord('k'),ord('K'),Screen.KEY_NUMPAD2,Screen.KEY_RIGHT),
    'left':(ord('j'),ord('J'),Screen.KEY_NUMPAD4,Screen.KEY_RIGHT),
    'right':(ord('l'),ord('L'),Screen.KEY_NUMPAD6,Screen.KEY_RIGHT),
}
EVENT_TO_MOVE = dict()
for move,keycodes in MOVES.items():
    for k in keycodes:
        EVENT_TO_MOVE[k] = move

def event_to_move(event):
    try:
        return EVENT_TO_MOVE.get(event.key_code,None)
    except AttributeError:
        return None
