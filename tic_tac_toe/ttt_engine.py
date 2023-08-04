from ttt_utils import (new_board, render, get_move, make_move,
                   get_legal_moves, change_player, get_winner, determine_draw)
from ai_functions import player_mapping
                           
# Play a full game of tic-tac-toe autonomously and returns the outcome
# of the match.
def auto_play(player1_name, player2_name):
    board = new_board()
    player1 = 'X'
    player2 = 'O'
    current_player = player1
    current_player_name = player1_name

    while True:

        move = player_mapping(current_player_name, board, current_player)
        board = make_move(board, move, current_player)

        current_player = change_player(current_player)
        if current_player_name == player1_name:
            current_player_name = player2_name
        else:
            current_player_name = player1_name

        if get_winner(board) ==  'X':
            return 1
        elif get_winner(board) == 'O':
            return 2
        elif determine_draw(board):
            return 0
        else:
            continue

# Simulate repeated battles and tally the outcomes.
def repeated_battle(player1_name, player2_name, num):
    player1_wins = 0
    player2_wins = 0
    draws = 0
    for i in range(num):
        outcome = auto_play(player1_name, player2_name)
        if outcome == 1:
            player1_wins += 1
        elif outcome == 2:
            player2_wins += 1
        else:
            draws +=1

    print('The win rate of ' + player1_name + ' was ' + str(player1_wins / num))
    print('The win rate of ' + player2_name + ' was ' + str(player2_wins / num))
    print('The rate of draws was ' + str(draws / num))

# Play a normal game of tic-tac-toe, including rendering the board.
def normal_play(player1_name, player2_name):
    board = new_board()
    player1 = 'X'
    player2 = 'O'
    current_player = player1
    current_player_name = player1_name

    render(board)

    while True:
        move = player_mapping(current_player_name, board, current_player)
        board = make_move(board, move, current_player)
        render(board)

        current_player = change_player(current_player)
        if current_player_name == player1_name:
            current_player_name = player2_name
        else:
            current_player_name = player1_name

        winner = get_winner(board)
        if winner == 'X':
            print('GAME OVER! Player \'X\' has won the game!')
            input()
            break
        elif winner == 'O':
            print('GAME OVER! Player \'O\' has won the game!')
            input()
            break
        elif determine_draw(board):
            print('GAME OVER! The game has resulted in a draw!')
            input()
            break
        else:
            continue

normal_play('minimax_ai', 'human_player')
