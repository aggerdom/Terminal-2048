from msvcrt import getch
from time import sleep
from config import KEYMAP,WIN,LOSE,DEFAULT_BOARD
import gamelogic

def print_board(board):
    btwn = "+-----"*4 + "+"
    line = ("|{:^5}"*4) + "|"
    for row in board:
        print(btwn)
        print(line.format(*row))
    print(btwn)

def play(state=None, delay=.25):
    if state is None:
        state = gamelogic.add_next_piece(DEFAULT_BOARD)
    while state not in (WIN,LOSE):
        print_board(state)
        move = None
        while not move:
            m_ = getch()
            if m_ in KEYMAP:
                move = KEYMAP[m_]
            sleep(delay)
        state = gamelogic.move(state,move)
    print_board(state)

if __name__ == "__main__":
    play()