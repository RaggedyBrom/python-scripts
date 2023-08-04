from random import randint

from minimax import minimax_ai
from ttt_utils import is_valid_move, get_legal_moves, get_winner, change_player

# An AI that returns a random coordinate which is checked for validity.    
def random_ai(board, player):
    while True:
        y = randint(0,2)
        x = randint(0,2)
        move = (y, x)
        if is_valid_move(board, move):
            return move
        else:
            continue

# An AI that returns a winning move if one exists, otherwise returns
# a random coordinate.
def finds_winning_moves_ai(board, player):
    for y in range(3):
        for x in range(3):
            if board[y][x] == None:
                temp_board = [[x for x in y] for y in board]
                temp_board[y][x] = player
                if get_winner(temp_board) == player:
                    move = (y, x)
                    return move
                else:
                    continue
                
    return random_ai(board, player)

# An AI that returns a winning move if one exists, otherwise returns a
# blocking move if one exists, otherwise returns a random coordinate.
def finds_winning_and_losing_moves_ai(board, player):
    for y in range(3):
        for x in range(3):
            if board[y][x] == None:
                temp_board = [[x for x in y] for y in board]
                temp_board[y][x] = player
                if get_winner(temp_board) == player:
                    move = (y, x)
                    return move
                else:
                    continue

    opponent = change_player(player)
    for y in range(3):
        for x in range(3):
            if board[y][x] == None:
                temp_board = [[x for x in y] for y in board]
                temp_board[y][x] = opponent
                if get_winner(temp_board) == opponent:
                    move = (y, x)
                    return move
                else:
                    continue

    return random_ai(board, player)

# Take input from a human player and return the coordinate.
def human_player(board, player):
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

# Return the correct move based on the current player.
def player_mapping(current_player_name, board, player):
    if current_player_name == 'random_ai':
        return random_ai(board, player)
    elif current_player_name == 'finds_winning_moves_ai':
        return finds_winning_moves_ai(board, player)
    elif current_player_name == 'finds_winning_and_losing_moves_ai':
        return finds_winning_and_losing_moves_ai(board, player)
    elif current_player_name == 'human_player':
        return human_player(board, player)
    elif current_player_name == 'minimax_ai':
        return minimax_ai(board, player)
