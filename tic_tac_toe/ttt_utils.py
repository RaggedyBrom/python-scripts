# Create the empty 3x3 board.
def new_board():
    return [
        [None, None, None],
        [None, None, None],
        [None, None, None],
        ]

# Print the board to the screen.
def render(board):
    print('  0 1 2')
    print('  ' + '-' * 6)
    for index, y in enumerate(board):
        print(str(index), end='')
        print('|', end='')
        for x in y:
            if x == None:
                print('  ', end='')
            else:
                print(x + ' ', end='')
        print('|')
    print('  ' + '-' * 6)
    
# Accept user input to place an X or O.
def get_move(board):
    while True:
        y = int(input('What is your move\'s Y co-ordinate?: '))
        x = int(input('What is your move\'s X co-ordinate?: '))
        print()
        move = (y, x)
        if is_valid_move(board, move):
            break
        else:
            print('Invalid move, try again.')
    return move

# Update the board with a player's move.
def make_move(board, move, player):
    updated_board = [[x for x in y] for y in board]
    y, x = move
    updated_board[y][x] = player
    return updated_board

# Determine whether a move is valid based on the current board state.
def is_valid_move(board, move):
    y, x = move
    if 0 <= y <= 2 and 0 <= x <= 2:
        if board[y][x] == None:
            return True
        else:
            return False
    else:
        return False

# Returns a list of all legal moves.
def get_legal_moves(board):
    legal_moves = []
    for y in range(3):
        for x in range(3):
            if board[y][x] == None:
                move = (y, x)
                legal_moves.append(move)
    return legal_moves

# Alternate between the two players.
def change_player(current_player):
    if current_player == 'X':
        return 'O'
    else:
        return 'X'
        
# Check every possible win scenario and return the winner if one exists.
def get_winner(board):
    possible_wins = []
    
    for y in range(3):
        row = []
        for x in range(3):
            row.append(board[y][x])
        possible_wins.append(row)
        
    for y in range(3):
        column = []
        for x in range(3):
            column.append(board[x][y])
        possible_wins.append(column)
        
    diagonal_1 = [board[0][0], board[1][1], board[2][2]]
    possible_wins.append(diagonal_1)
    diagonal_2 = [board[0][2], board[1][1], board[2][0]]
    possible_wins.append(diagonal_2)

    for possible_win in possible_wins:
        if possible_win == ['X', 'X', 'X']:
            return 'X'
        elif possible_win == ['O', 'O', 'O']:
            return 'O'
        else:
            continue
    return None

# Determine if a draw has occurred.
def determine_draw(board):
    for row in board:
        for cell in row:
            if cell == None:
                return False
    return True
