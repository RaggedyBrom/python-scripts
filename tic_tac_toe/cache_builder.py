import json

from minimax import minimax_score
from ttt_utils import (get_legal_moves, new_board, change_player, make_move,
                       get_winner, determine_draw)

def cache_builder(board, player_to_move, player_to_optimize):
    
    legal_moves = get_legal_moves(board)
    for move in legal_moves:
        new_board = [[x for x in y] for y in board]
        new_board = make_move(new_board, move, player_to_move)
        opponent = change_player(player_to_move)
        score = minimax_score(new_board, opponent, player_to_optimize)
        board_string = str(new_board)
        cache[board_string] = score
        if get_winner(board) is not None or determine_draw(board):
            continue
        cache_builder(new_board, opponent, player_to_optimize)

player1 = 'X'
cache = {}
board = new_board()
cache_builder(board, player1, player1)
print(len(cache))
f = open('cache.json', 'w')
json.dump(cache, f)
f.close()
