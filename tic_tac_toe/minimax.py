import json
from ttt_utils import (get_legal_moves, get_winner, change_player,
                       make_move, determine_draw)

# Minimizes opponent's outcomes while maximizing own outcomes.
#
# 'board' is a 2-D grid of the state to be scored
# 'current_player' is the player whose turn it is
#   ('X' or 'O')
def minimax_score(board, player_to_move, player_to_optimize):

    # If 'board' is a terminal state, immediately return
    # the appropriate score.
    winner = get_winner(board)
    if winner is not None:
        if winner == player_to_optimize:
            return +10
        else:
            return -10
    elif determine_draw(board):
        return 0

    # If 'board' is not a terminal state, get all moves that could
    # be played.
    legal_moves = get_legal_moves(board)

    # Iterate through these moves, calculating a score for them and
    # adding it to the 'scores' array.
    scores = []
    for move in legal_moves:
        # First make the move
        temp_board = [[c for c in r] for r in board]
        new_board = make_move(temp_board, move, player_to_move)

        # Then get the minimax score for the resulting state, passing
        # in 'current_player's opponents because it's their turn now.
        #
        # You may notice that 'minimax_score' is calling itself -
        # this is known as "recursion".
        opponent = change_player(player_to_move)
        score = minimax_score(new_board, opponent, player_to_optimize)
        scores.append(score)

    # If 'current_player' our AI, then they are trying to maximize
    # the score, so we should return the maximum of all the scores that
    # we calculated.
    if player_to_move == player_to_optimize:
        return max(scores)
    # If 'current_player' is our opponent, then the AI is trying to
    # minimize the score. We should return the minimum.
    else:
        return min(scores)

def minimax_score_with_cache(board, player_to_move, player_to_optimize):
    # Turn the board into a string so it can be used as a dictionary
    # key to access our hash.
    # This conversion can be done any way you like as long as each board
    # produces a unique string.
    board_cache_key = str(board)

    # Only calculate a score if the board is not already in our cache.
    if board_cache_key not in cache:
        score = minimax_score(board, player_to_move, player_to_optimize)

        # Once the new score has been calculated, stuff it into
        # the cache.
        cache[board_cache_key] = score

    # Finally, return the score from the cache. Either it was already there,
    # or it wasn't and we just calculated it in the block above.
    return cache[board_cache_key]

# An AI that uses the minimax function to recursively search through all
# possible outcomes and chooses the optimal move.
def minimax_ai(board, player):
    f = open('cache.json', 'r')
    cache = json.load(f)
    best_move = None
    best_score = None

    legal_moves = get_legal_moves(board)
    for move in legal_moves:
        temp_board = [[c for c in r] for r in board]
        temp_board = make_move(temp_board, move, player)
        board_string = str(temp_board)
        score = cache[board_string]

        if best_score == None or score > best_score:
            best_score = score
            best_move = move

    f.close()
    return best_move
