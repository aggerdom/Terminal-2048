import itertools
import random

from config import WIN, LOSE


def transpose(matrix):
    return [[matrix[row][col] for row in range(len(matrix))]
            for col in range(len(matrix))]


def collapse(row, zeros_on='left'):
    out = []
    # ------ Do an inital sort of all zeros to the left
    # this corresponds to pushing all squares right w/o collapsing them.
    row = sorted(row[:], key=lambda x: x != 0)
    cvals = ((value, list(g)) for value, g in itertools.groupby(row))
    for val, group in cvals:
        ncollapse, nretain = divmod(len(group), 2)
        if zeros_on == 'left':
            group_items = [0] * ncollapse + [val] * nretain + [val * 2] * ncollapse
        else:
            group_items = [val * 2] * ncollapse + [val] * nretain + [0] * ncollapse
        out.extend(group_items)
    # Do a final sort to pull all zeros that have been added to the
    # center to the appropriate side
    if zeros_on == 'left':
        out.sort(key=lambda x: x != 0)
    elif zeros_on == 'right':
        out.sort(key=lambda x: x == 0)
    else:
        raise NotImplementedError("zeros_on argument must be in {'left','right'}")
    return out


assert collapse([0, 2, 2, 0]) == [0, 0, 0, 4]


def is_win(state):
    return 2048 in itertools.chain.from_iterable(state)


def move_blocks(state, move):
    if move == 'right':
        newstate = [collapse(row) for row in state]
    elif move == 'left':
        newstate = [collapse(row, zeros_on='right') for row in state]
    elif move == 'down':
        newstate = transpose([collapse(row) for row in transpose(state)])
    elif move == 'up':
        newstate = transpose([collapse(row, zeros_on='right') for row in transpose(state)])
    else:
        raise ValueError("'%s' is not a valid argument for move." % move)
    return newstate


def add_next_piece(state, random_pos=True, random_piece=True):
    if random_piece:
        piece = random.choice((2, 4))
    else:
        piece = 2
    if random_pos:
        available = [(r, c) for r, c in itertools.product(range(4), range(4))
                     if state[r][c] == 0]
        if len(available) == 0:
            raise ValueError("CAN'T ADD ANYMORE, THE BOARD IS FULL!")
        pos = random.choice(available)
        state[pos[0]][pos[1]] = piece
        return state
    else:
        for r in reversed(range(4)):
            for c in reversed(range(4)):
                if state[r][c] == 0:
                    state[r][c] = 2
                    return state
        raise ValueError("CAN'T ADD ANYMORE, THE BOARD IS FULL!")


def move(state, move):
    # =========================== Move PIECES
    state = move_blocks(state, move)
    # =========================== ADD PIECES
    # Will raise an error if the board is full
    try:
        add_next_piece(state)
    except ValueError as e:
        return LOSE
    # =========================== Check if we win
    if is_win(state):
        return WIN
    # =========================== Return the state for next turn
    else:
        return state


def main():
    assert transpose([[0, 0, 1], [1, 1, 0], [0, 1, 1]]) == [[0, 1, 0], [0, 1, 1], [1, 0, 1]]


if __name__ == '__main__':
    main()
