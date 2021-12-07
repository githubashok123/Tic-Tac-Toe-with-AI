from random import randint


def initial_state():
    board = [['_' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    return board, current_player


def print_board(board):
    print('---------')
    for i in range(3):
        print('|', *board[i], '|')
    print('---------')


def check_if_empty(row, column):
    if board[row][column] == '_':
        return True
    return False


def make_move():
    """Getting input from user and validating the same"""
    while True:
        try:
            row, column = input('Enter the coordinates: ').split()
            row = int(row) - 1
            column = int(column) - 1
        except ValueError:
            print("You should enter numbers!")
            continue
        if row < 0 or row > 2 or column < 0 or column > 2:
            print("Coordinates should be from 1 to 3!")
            continue
        if check_if_empty(row, column):
            board[row][column] = current_player
            break
        else:
            print("This cell is occupied! Choose another one!")
            continue


def check_end_condition(grid):
    """Check the state of the game, return who is won,
    if status draw it return True, if game not end return False"""
    for co in ([(0, 0), (0, 1), (0, 2)],
               [(1, 0), (1, 1), (1, 2)],
               [(2, 0), (2, 1), (2, 2)],
               [(0, 0), (1, 0), (2, 0)],
               [(0, 1), (1, 1), (2, 1)],
               [(0, 2), (1, 2), (2, 2)],
               [(0, 2), (1, 1), (2, 0)],
               [(0, 0), (1, 1), (2, 2)]):
        if [grid[x][y] for x, y in co].count('X') == 3:
            return 'X'
        elif [grid[x][y] for x, y in co].count('O') == 3:
            return 'O'
    if '_' not in grid[0] and '_' not in grid[1] and '_' not in grid[2]:
        return 'Draw'
    else:
        return False


def change_player(current_player):
    if current_player == 'X':
        return 'O'
    elif current_player == 'O':
        return 'X'


def computer_move_easy():
    """At this level the computer makes random moves.
    This should be perfect for people who have never played the game before!"""
    while True:
        row, column = randint(0, 2), randint(0, 2)
        if check_if_empty(row, column):
            board[row][column] = current_player
            break


def computer_move_medium():
    """When the AI is playing at medium difficulty level,
     it makes moves using the following logic:

    1. If it already has two in a row and can win with one further move, it does so.
    2. If its opponent can win with one move, it plays the move necessary to block this.
    3. Otherwise, it makes a random move"""
    for co in ([(0, 0), (0, 1), (0, 2)],
               [(1, 0), (1, 1), (1, 2)],
               [(2, 0), (2, 1), (2, 2)],
               [(0, 0), (1, 0), (2, 0)],
               [(0, 1), (1, 1), (2, 1)],
               [(0, 2), (1, 2), (2, 2)],
               [(0, 2), (1, 1), (2, 0)],
               [(0, 0), (1, 1), (2, 2)]):

        if (([board[x][y] for x, y in co].count('X') == 2 and [board[x][y] for x, y in co].count('_') == 1)
                or ([board[x][y] for x, y in co].count('O') == 2 and [board[x][y] for x, y in co].count('_') == 1)):
            r, c = co[[board[x][y] for x, y in co].index('_')]
            board[r][c] = current_player
            return

    while True:
        row, column = randint(0, 2), randint(0, 2)
        if check_if_empty(row, column):
            board[row][column] = current_player
            break


def computer_move_hard(player_no):
    """Implemented the 'hard' difficulty level using the minimax algorithm.
    At this level,It will calculate all possible moves that might be played during the game,
    and choose the best one based on the assumption that its opponent will also play perfectly.
    If played against User AI will either Win or game will be Draw but opponent will never will."""
    move, score = minimax(board, player_no, player_no)
    x, y = move[0], move[1]
    board[x][y] = player_symbols[player_no]
    print('Making move level "hard"')


def minimax(temp_data, player_no_this_move, playing_player_no):
    winner = check_end_condition(temp_data)
    if winner == player_symbols[playing_player_no]:
        return None, 10
    elif winner == player_symbols[playing_player_no ^ 1]:  # XOR = the other player
        return None, -10
    elif winner == "Draw":
        return None, 0

    moves = {}
    empty_fields = []
    for x, y in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
        if temp_data[x][y] == '_':
            empty_fields.append((x, y))

    # loop through available spots
    for x, y in empty_fields:
        # set the empty spot to the current player
        temp_data[x][y] = player_symbols[player_no_this_move]

        # collect the score resulted from calling minimax
        # alternating between the two players
        move, score = minimax(temp_data, player_no_this_move ^ 1, playing_player_no)

        # reset the spot to empty
        temp_data[x][y] = "_"

        moves[(x, y)] = score

    # if it is the computer's turn loop over the moves and choose
    # the move with the highest score
    if player_no_this_move == playing_player_no:
        best_move = max(moves, key=moves.get)
        best_score = moves[best_move]

    # else loop over the moves and choose the move with the lowest score
    else:
        best_move = min(moves, key=moves.get)
        best_score = moves[best_move]

    return best_move, best_score


modes = ('user', 'easy', 'medium', 'hard')
player_symbols = ["X", "O"]


while True:
    """Performs the main sequence of actions of the game with selected level and rules"""
    player_no = 0
    start = input()
    if start == 'exit':
        break
    else:
        try:
            s, first, second = start.split()
            if s != 'start' or first not in modes or second not in modes:
                raise ValueError
        except ValueError:
            print("Bad parameters!")
            continue

    board, current_player = initial_state()
    turn = 'first'
    print_board(board)
    while True:
        if turn == 'first':
            player_no = 0
            if first == 'user':
                make_move()
            elif first == 'easy':
                print('Making move level "easy"')
                computer_move_easy()
            elif first == 'medium':
                print('Making move level "medium"')
                computer_move_medium()
            elif first == 'hard':
                computer_move_hard(player_no)
            turn = 'second'
        elif turn == 'second':
            player_no = 1
            if second == 'user':
                make_move()
            elif second == 'easy':
                print('Making move level "easy"')
                computer_move_easy()
            elif second == 'medium':
                print('Making move level "medium"')
                computer_move_medium()
            elif second == 'hard':
                computer_move_hard(player_no)
            turn = 'first'
        end = check_end_condition(board)
        current_player = change_player(current_player)
        print_board(board)
        if end:
            if end == 'draw':
                print("Draw")
            else:
                print(f"{end} wins")
            break
