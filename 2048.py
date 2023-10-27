import random
import curses

def create_board():
    board = [[0] * 4 for _ in range(4)]
    return board

def add_tile(board):
    empty_tiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = random.randint(1, 2) * 2

def move_left(board):
    for i in range(4):
        board[i] = merge_tiles(board[i])
    return board

def move_right(board):
    for i in range(4):
        board[i] = merge_tiles(board[i][::-1])[::-1]
    return board

def move_up(board):
    transposed_board = transpose(board)
    for i in range(4):
        transposed_board[i] = merge_tiles(transposed_board[i])
    return transpose(transposed_board)

def move_down(board):
    transposed_board = transpose(board)
    for i in range(4):
        transposed_board[i] = merge_tiles(transposed_board[i][::-1])[::-1]
    return transpose(transposed_board)

def merge_tiles(row):
    new_row = [0] * 4
    j = 0
    for i in range(4):
        if row[i] != 0:
            if new_row[j] == 0:
                new_row[j] = row[i]
            elif new_row[j] == row[i]:
                new_row[j] *= 2
                j += 1
            else:
                j += 1
                new_row[j] = row[i]
    return new_row

def transpose(board):
    return [[board[j][i] for j in range(4)] for i in range(4)]

def is_game_over(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if i < 3 and board[i][j] == board[i+1][j]:
                return False
            if j < 3 and board[i][j] == board[i][j+1]:
                return False
    return True

def print_board(stdscr, board):
    stdscr.clear()
    for i in range(5):
        for j in range(5):
            x = j * 5 + 1
            y = i * 2 + 1
            if i % 2 == 0 and j < 4:
                stdscr.addstr(y, x, "-" * 5)
            elif i % 2 == 1 and j < 4:
                stdscr.addstr(y, x, "|" + " " * 4)
            if i < 4 and j < 4:
                stdscr.addstr(y, x, str(board[i][j]), curses.A_BOLD)
    stdscr.refresh()

def main(stdscr):
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_MAGENTA, -1)
    stdscr.bkgd(curses.color_pair(1))
    stdscr.nodelay(1)
    stdscr.timeout(100)

    board = create_board()
    add_tile(board)
    add_tile(board)

    while True:
        print_board(stdscr, board)
        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == curses.KEY_LEFT:
            board = move_left(board)
            add_tile(board)
        elif key == curses.KEY_RIGHT:
            board = move_right(board)
            add_tile(board)
        elif key == curses.KEY_UP:
            board = move_up(board)
            add_tile(board)
        elif key == curses.KEY_DOWN:
            board = move_down(board)
            add_tile(board)
        
        if is_game_over(board):
            stdscr.addstr(10, 10, "GAME OVER!")
            stdscr.refresh()
            break

curses.wrapper(main)



