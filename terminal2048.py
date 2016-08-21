from msvcrt import getch
from time import sleep
from config import KEYMAP, WIN, LOSE, DEFAULT_BOARD
import sys
import gamelogic
import displaylogic
from operator import attrgetter
from displaylogic import Screen

IS_WINDOWS = sys.platform == "win32"
if IS_WINDOWS:
    from win32api import GetAsyncKeyState
    from win32con import VK_DOWN, VK_UP, VK_LEFT, VK_RIGHT

ticks = 0

def play(screen, state=None, pause_after_move=.5):
    global ticks
    if state is None:
        state = gamelogic.add_next_piece(DEFAULT_BOARD)
    else:
        raise ValueError(state)
    # Initializing the board
    displaylogic.print_board(screen) # initialize the board
    displaylogic.print_numbers(screen, state) # draw the pieces
    # Play the game
    while state not in (WIN, LOSE):
        # Redraw if user has resized terminal
        if screen.has_resized():
            screen.clear()
            displaylogic.print_board(screen)
            displaylogic.print_numbers(screen, state)
        screen.refresh()
        # Figure out the player's move
        valid_move_found = False
        while not valid_move_found:
            screen.print_at(str(ticks),0,40)
            screen.refresh()
            event = screen.get_event()
            if event and displaylogic.event_to_move(event):
                move = displaylogic.event_to_move(event)
                if move:
                    valid_move_found = True
            if IS_WINDOWS and not valid_move_found:
                arrows_pressed = [GetAsyncKeyState(vkcode) for vkcode in (VK_DOWN, VK_UP, VK_LEFT, VK_RIGHT)]
                if arrows_pressed.count(0) == 3:
                    for i, keystate in enumerate(arrows_pressed):
                        if keystate != 0:
                            move = ('down','up','left','right')[i]
                            valid_move_found = True
                            break
        # Respond accordingly
        if move == 'quit':
            sys.exit()
        else:
            state = gamelogic.move(state, move)
            displaylogic.print_numbers(screen, state)
            screen.refresh()
            sleep(pause_after_move)
    sleep(5)

if __name__ == "__main__":
    try:
        displaylogic.Screen.wrapper(play)
    except KeyboardInterrupt:
        sleep(10)
