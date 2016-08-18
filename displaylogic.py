import colorama

for console_row in range(5):
    print('\n'+' '*25)

def print_board(board):
    btwn = "+-----" * 4 + "+"
    line = ("|{:^5}" * 4) + "|"
    for row in board:
        print(btwn)
        print(line.format(*row))
    print(btwn)

if __name__ == '__main__':
    from .config import DEFAULT_BOARD
    print_board(DEFAULT_BOARD)