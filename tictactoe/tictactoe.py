"""
Tic Tac Toe Player
"""

import math
import numpy as np
import copy
from collections import Counter

X = "X"
O = "O"
EMPTY = None
boards_states = []

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    board = copy.deepcopy(board)
    counts = Counter(board[0])[None] + Counter(board[1])[None] + Counter(board[2])[None]

    # print(counts)
    # if board == initial_state():
    #     return X
    if counts%2==0:
        return 'O'
    elif counts%2!=0:
        return 'X'
    elif counts==0:
        return 0



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # board=copy.deepcopy(board)
    moves = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]==None:
                moves.add((i,j))
    if moves!=0:
        return moves
    elif moves==0:
        return 0



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # global boards_states
    # boards_states.append(copy.deepcopy(board))
    board = copy.deepcopy(board)
    if player(board)==X:
        board[action[0]][action[1]] = X
        return board
    elif player(board)==O:
        board[action[0]][action[1]] = O
        return board
    else:
        raise Exception('Action invalid')

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # horizontal check
    for i in range(len(board)):
        if Counter(board[i])['X']==3:
            return 1 # print('x won') #1
        elif Counter(board[i])['O']==3:
            return -1

    # vertical check
    for i in range(len(board)):
        if (Counter(board[0][i])['X'] + Counter(board[1][i])['X'] + Counter(board[2][i])['X']) == 3:
            return 1# print('x won in ' + str(i) + ' column') #1
        elif (Counter(board[0][i])['O'] + Counter(board[1][i])['O'] + Counter(board[2][i])['O']) == 3:
            return -1 # print('O won in ' + str(i) + ' column') #-1

    # diagonal
    if (Counter(board[0][0])['X'] + Counter(board[1][1])['X'] + Counter(board[2][2])['X'])==3 or Counter(board[0][2])['X'] + (Counter(board[1][1])['X'] + Counter(board[2][0])['X'])==3:
        return 1 # print('x won') #1
    if (Counter(board[0][0])['O'] + Counter(board[1][1])['O'] + Counter(board[2][2])['O'])==3 or Counter(board[0][2])['O'] + (Counter(board[1][1])['O'] + Counter(board[2][0])['O'])==3:
        return -1 # print('o won') #-1

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)==-1 or winner(board)==1 or player(board)==0:
        return True
    else:
        return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board)==True:
        # X won
        if winner(board)==1:
            return 1
        if winner(board)==-1:
            return -1
        else:
            return 0


def board_state(board):
    # '''
    #
    # :param board: board after movement (action)
    # :return: the smallest or the biggest value of the board after a particular action
    # '''

    # horizontal
    grade = []

    for i in range(len(board)):
        # x

        if Counter(board[i])['X']==3:
            grade.append(4)
        elif Counter(board[i])['O']==2 and Counter(board[i])['X']==1:
            grade.append(3)
        elif Counter(board[i])['X']==2 and Counter(board[i])[None]==1:
            grade.append(2)
        elif Counter(board[i])['X']==1 and Counter(board[i])[None]==2:
            grade.append(1)

        # neutral

        elif Counter(board[i])[None]==3:
            grade.append(0)
        elif Counter(board[i])['X'] == 1 and Counter(board[i])[None] == 1 and Counter(board[i])[None]==1:
            grade.append(0)

            # 'O'

        elif Counter(board[i])['O'] == 1 and Counter(board[i])[None] == 2:
            grade.append(-1)
        elif Counter(board[i])['O'] == 2 and Counter(board[i])[None] == 1:
            grade.append(-2)
        elif Counter(board[i])['X'] == 2 and Counter(board[i])['O'] == 1:
            grade.append(-3)
        elif Counter(board[i])['O']==3:
            grade.append(-4)

    # diagonal check

    diag = [[board[0][0], board[1][1], board[2][2]], [board[2][0], board[1][1], board[0][2]]]

    for i in range(len(diag)):

        if Counter(diag[i])['X'] == 3:
            grade.append(4)
        elif Counter(diag[i])['O'] == 2 and Counter(diag[i])['X'] == 1:
            grade.append(3)
        elif Counter(diag[i])['X'] == 2 and Counter(diag[i])[None] == 1:
            grade.append(2)
        elif Counter(diag[i])['X'] == 1 and Counter(diag[i])[None] == 2:
            grade.append(1)

        # neutral

        elif Counter(diag[i])[None] == 3:
            grade.append(0)
        elif Counter(diag[i])['X'] == 1 and Counter(diag[i])[None] == 1 and Counter(diag[i])[None] == 1:
            grade.append(0)

            # 'O'

        elif Counter(diag[i])['O'] == 1 and Counter(diag[i])[None] == 2:
            grade.append(-1)
        elif Counter(diag[i])['O'] == 2 and Counter(diag[i])[None] == 1:
            grade.append(-2)
        elif Counter(diag[i])['X'] == 2 and Counter(diag[i])['O'] == 1:
            grade.append(-3)
        elif Counter(diag[i])['O'] == 3:
            grade.append(-4)

    # vertical check

    board=np.transpose(board)

    for i in range(len(board)):
        # x

        if Counter(board[i])['X']==3:
            grade.append(4)
        elif Counter(board[i])['O']==2 and Counter(board[i])['X']==1:
            grade.append(3)
        elif Counter(board[i])['X']==2 and Counter(board[i])[None]==1:
            grade.append(2)
        elif Counter(board[i])['X']==1 and Counter(board[i])[None]==2:
            grade.append(1)

        # neutral

        elif Counter(board[i])[None]==3:
            grade.append(0)
        elif Counter(board[i])['X'] == 1 and Counter(board[i])[None] == 1 and Counter(board[i])[None]==1:
            grade.append(0)

            # 'O'

        elif Counter(board[i])['O'] == 1 and Counter(board[i])[None] == 2:
            grade.append(-1)
        elif Counter(board[i])['O'] == 2 and Counter(board[i])[None] == 1:
            grade.append(-2)
        elif Counter(board[i])['X'] == 2 and Counter(board[i])['O'] == 1:
            grade.append(-3)
        elif Counter(board[i])['O']==3:
            grade.append(-4)

    return grade


    # # diagonal
    # if (Counter(board[0][0])['X'] + Counter(board[1][1])['X'] + Counter(board[2][2])['X'])==3 or Counter(board[0][2])['X'] + (Counter(board[1][1])['X'] + Counter(board[2][0])['X'])==3:
    #     return 1
    # if (Counter(board[0][0])['O'] + Counter(board[1][1])['O'] + Counter(board[2][2])['O'])==3 or Counter(board[0][2])['O'] + (Counter(board[1][1])['O'] + Counter(board[2][0])['O'])==3:
    #     return 1

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board)== True:
        return board
    if board==initial_state():
        return (1,1)
    akcje =[]
    vals = []
    if player(board)=='X':
        for action in actions(board):

            vals.append(sum(board_state(result(board,action))))
            akcje.append(action)
        return akcje[vals.index(max(vals))]
    if player(board)=='O':
        for action in actions(board):

            vals.append(min(board_state(result(board,action))))
            akcje.append(action)
        return akcje[vals.index(min(vals))]

min    # print(vals,'\n')
    # print(akcje)
    # print(vals.index(max(vals)))
    # print(akcje[0])return akcje[vals.index(max(vals))]


