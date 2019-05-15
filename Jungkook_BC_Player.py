'''Jungkook_BC_Player.py
The beginnings of an agent that might someday play Baroque Chess.

'''

from BC_state_etc import *
import time as time

pieces = []
OPONENT_NAME = ''
BASIC_REMARKS = []
MAX_PLY = 3
CURRENT_STATE_STATIC_VAL = 0
N_STATES_EXPANDED = 0
N_STATIC_EVALS = 0
N_CUTOFFS = 0
TIME_LIMIT = 0
START_TIME = 0
count = 0
chosenState = None

piece_vals = {0: 0.0, 2: -13.0, 3: 13.0, 4: -75.0, 5: 75.0, 6: -100.0, 7: 100.0, 8: -13.0, 9: 13.0, 10: -35.0, 11: 35.0,
              12: -1000.0, 13: 1000.0, 14: -100.0, 15: 100.0}
edge_vals = [[9, 8, 8, 8, 8, 8, 8, 9],
             [8, 5, 5, 5, 5, 5, 5, 8],
             [8, 5, 4, 4, 4, 4, 5, 8],
             [8, 5, 4, 3, 3, 4, 5, 8],
             [8, 5, 4, 3, 3, 4, 5, 8],
             [8, 5, 4, 4, 4, 4, 5, 8],
             [8, 5, 5, 5, 5, 5, 5, 8],
             [9, 8, 8, 8, 8, 8, 8, 9]]

middle_vals = [[2, 2, 2, 2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4, 4, 4, 4],
             [5, 5, 5, 5, 5, 5, 5, 5],
             [5, 5, 5, 5, 5, 5, 5, 5],
             [4, 4, 4, 4, 4, 4, 4, 4],
             [3, 3, 3, 3, 3, 3, 3, 3],
             [2, 2, 2, 2, 2, 2, 2, 2]]

piece_advance = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [2, 2, 2, 2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3, 3, 3, 3],
             [3, 3, 3, 3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4, 4, 4, 4],
             [4, 4, 4, 4, 4, 4, 4, 4]]

def parameterized_minimax(currentState, alphaBeta=False, ply=3, \
                          useBasicStaticEval=True, useZobristHashing=False):
    '''Implement this testing function for your agent's basic
    capabilities here.'''
    global N_STATIC_EVALS, N_STATES_EXPANDED, N_CUTOFFS, CURRENT_STATE_STATIC_VAL, MAX_PLY, TIME_LIMIT, chosenState
    CURRENT_STATE_STATIC_VAL = 0
    N_STATES_EXPANDED = 0
    N_STATIC_EVALS = 0
    N_CUTOFFS = 0

    if alphaBeta:
        alpha = +100000
        beta = -100000
        chosenState, provisional = pruned_minimaxHelper([[(0, 0), (0, 0)],currentState], alpha, beta, ply, useBasicStaticEval, useZobristHashing)
    else:
        chosenState, provisional = minimaxHelper([[(0, 0), (0, 0)], currentState], ply, useBasicStaticEval, useZobristHashing)

    return {"CURRENT_STATE_STATIC_VAL": provisional, "N_STATES_EXPANDED": N_STATES_EXPANDED,
            "N_STATIC_EVALS": N_STATIC_EVALS, "N_CUTOFFS": N_CUTOFFS}

def minimaxHelper(currentState, ply, useBasicStaticEval=True, useZobristHashing=False):
    global N_STATIC_EVALS, N_STATES_EXPANDED, CURRENT_STATE_STATIC_VAL, MAX_PLY, chosenState, START_TIME

    successors = generate_successors(currentState[1])
    if(useBasicStaticEval):
        successors = sorted(successors, key=lambda k: translate_move_coord(k[0]))
    
    currPly = ply - 1
    finalState = successors[0]
    tempEv = 0
    whose = currentState[1].whose_move
    while time.perf_counter() - START_TIME < TIME_LIMIT - float(0.2):
        if currPly == 0 or ply == 0:
            tempState = None
            if whose == 1:
                tempMin = -10000
                for s in successors:
                    N_STATES_EXPANDED = N_STATES_EXPANDED + 1
                    if useBasicStaticEval:
                        ev = basicStaticEval(s[1])
                    else:
                        ev = staticEval(s[1])
                    N_STATIC_EVALS = N_STATIC_EVALS + 1
                    if not useBasicStaticEval and ev > tempMin:
                        tempState = s
                        tempMin = ev
                    elif useBasicStaticEval and ev > tempMin:
                        tempState = s
                        tempMin = ev
                tempEv = tempMin
            else:
                tempMax = 10000
                for s in successors:
                    N_STATES_EXPANDED = N_STATES_EXPANDED + 1
                    if useBasicStaticEval:
                        ev = basicStaticEval(s[1])
                    else:
                        ev = staticEval(s[1])
                    N_STATIC_EVALS = N_STATIC_EVALS + 1
                    if not useBasicStaticEval and ev < tempMax:
                        tempState = s
                        tempMax = ev
                    elif useBasicStaticEval and ev < tempMin:
                        tempState = s
                        tempMin = ev
                tempEv = tempMax
            finalState = tempState
            return tempState, tempEv
        else:
            tempState = None
            if whose == 1:
                tempMin = -10000
                for s in successors:
                    N_STATES_EXPANDED = N_STATES_EXPANDED + 1
                    t, ev = minimaxHelper(s, currPly, useBasicStaticEval, useZobristHashing)
                    if not useBasicStaticEval and ev > tempMin:
                        tempState = s
                        tempMin = ev
                    elif useBasicStaticEval and ev > tempMin:
                        tempState = s
                        tempMin = ev
                tempEv = tempMin
            else:
                tempMax = 10000
                for s in successors:
                    N_STATES_EXPANDED = N_STATES_EXPANDED + 1
                    t, ev = minimaxHelper(s, currPly, useBasicStaticEval, useZobristHashing)
                    if not useBasicStaticEval and ev < tempMax:
                        tempState = s
                        tempMax = ev
                    elif useBasicStaticEval and ev < tempMax:
                        tempState = s
                        tempMax = ev
                tempEv = tempMax
            finalState = tempState
    return finalState, tempEv
            
def pruned_minimaxHelper(currentState, alpha, beta, ply, useBasicStaticEval, useZobristHashing):
    global N_STATIC_EVALS, N_STATES_EXPANDED, CURRENT_STATE_STATIC_VAL, MAX_PLY, chosenState, START_TIME

    successors = generate_successors(currentState[1])
    if(useBasicStaticEval):
        successors = sorted(successors, key=lambda k: translate_move_coord(k[0]))
    

    currPly = ply - 1
    finalState = successors[0]
    tempEv = 0
    whose = currentState[1].whose_move
    while time.perf_counter() - START_TIME < TIME_LIMIT - float(0.2):
        if currPly == 0 or ply == 0:
            tempState = None
            if whose == 1:
                tempMin = -10000
                for s in successors:
                    N_STATES_EXPANDED = N_STATES_EXPANDED + 1
                    if useBasicStaticEval:
                        ev = basicStaticEval(s[1])
                    else:
                        ev = staticEval(s[1])
                    N_STATIC_EVALS = N_STATIC_EVALS + 1
                    if not useBasicStaticEval and ev >= tempMin:
                        tempState = s
                        tempMin = ev
                    elif useBasicStaticEval and ev > tempMin:
                        tempState = s
                        tempMin = ev
                    alpha = max(alpha, tempMin)
                    if beta <= alpha:
                        break
                tempEv = tempMin
            else:
                tempMax = 10000
                for s in successors:
                    N_STATES_EXPANDED = N_STATES_EXPANDED + 1
                    if useBasicStaticEval:
                        ev = basicStaticEval(s[1])
                    else:
                        ev = staticEval(s[1])
                    N_STATIC_EVALS = N_STATIC_EVALS + 1
                    if not useBasicStaticEval and ev <= tempMax:
                        tempState = s
                        tempMax = ev
                    elif useBasicStaticEval and ev < tempMax:
                        tempState = s
                        tempMax = ev
                    beta = min(beta, tempMax)
                    if beta <= alpha:
                        break
                tempEv = tempMax
            finalState = tempState
            return tempState, tempEv
        else:
            tempState = None
            if whose == 1:
                tempMin = -10000
                for s in successors:
                    N_STATES_EXPANDED = N_STATES_EXPANDED + 1
                    t, ev = minimaxHelper(s, currPly, useBasicStaticEval, useZobristHashing)
                    if not useBasicStaticEval and ev >= tempMin:
                        tempState = s
                        tempMin = ev
                    elif useBasicStaticEval and ev > tempMin:
                        tempState = s
                        tempMin = ev
                    alpha = max(alpha, tempMin)
                    if beta <= alpha:
                        break
                tempEv = tempMin
            else:
                tempMax = 10000
                for s in successors:
                    N_STATES_EXPANDED = N_STATES_EXPANDED + 1
                    t, ev = minimaxHelper(s, currPly, useBasicStaticEval, useZobristHashing)
                    if not useBasicStaticEval and ev <= tempMax:
                        tempState = s
                        tempMax = ev
                    elif useBasicStaticEval and ev < tempMax:
                        tempState = s
                        tempMax = ev
                    beta = min(beta, tempMax)
                    if beta <= alpha:
                        break
                tempEv = tempMax
            finalState = tempState
    return finalState, tempEv


def generate_successors(state):
    successors = []
    new_s = []
    new_turn = 1-state.whose_move
    for row in range(8):
        for col in range(8):
            piece = state.board[row][col]
            if who(piece) == state.whose_move and piece > 0 and not is_frozen(state, row, col):
                if piece == WHITE_PINCER or piece == BLACK_PINCER or piece == WHITE_IMITATOR or piece == BLACK_IMITATOR:
                    successors = successors + move_pincer(state, row, col)
                if piece == WHITE_KING or piece == BLACK_KING or piece == WHITE_IMITATOR or piece == BLACK_IMITATOR:
                    successors = successors + move_king(state, row, col)
                if piece > 3 and piece != 12 and piece != 13:
                    successors = successors + move_like_queen(state, row, col)
    for s in successors:
        new_s = new_s + [[s[0], BC_state(s[1].board, new_turn)]]
    return new_s


def is_valid(row, col):
    if 0 <= row < 8 and 0 <= col < 8:
        return True
    return False


def move_like_queen(state, row, col):
    piece = state.board[row][col]
    kings = find_kings(state)
    king_row = kings[0]
    king_col = kings[1]
    whose = who(piece)
    successors = []
    checking = True
    move = 1

    # Moves in S direction
    while checking and whose == state.whose_move:
        newState = BC_state(state.board)
        if is_valid(row + move, col) and newState.board[row + move][col] == 0:
            if piece == WHITE_COORDINATOR or piece == BLACK_COORDINATOR:
                newState.board[row + move][col] = piece
                newState.board[row][col] = 0
                if newState.board[king_row][col] != 0 and who(newState.board[king_row][col]) != whose:
                    newState.board[king_row][col] = 0
                if newState.board[row + move][king_col] != 0 and who(newState.board[row + move][king_col]) != whose:
                    newState.board[row + move][king_col] = 0
            elif piece == WHITE_WITHDRAWER or piece == BLACK_WITHDRAWER:
                newState.board[row + move][col] = piece
                newState.board[row][col] = 0
                if is_valid(row-1, col) and newState.board[row - 1][col] != 0 and who(newState.board[row - 1][col]) != whose:
                    newState.board[row - 1][col] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row + move
                new_col = col
                if is_valid(new_row + 1, new_col) and newState.board[new_row + 1][new_col] != 0 and who(newState.board[new_row + 1][new_col]) != whose:
                    if is_valid(new_row + 2, new_col) and newState.board[new_row + 2][new_col] == 0:
                        newState.board[new_row + 1][new_col] = 0
                        new_row += 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row + move][col] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row + move, col))
            temp = BC_state(newState.board, newState.whose_move)
            successors = successors + [[new_move, temp]]
        else:
            checking = False
        move += 1

    checking = True
    move = 1
    # Moves in SW direction
    while checking:
        newState = BC_state(state.board)
        if is_valid(row + move, col - move) and newState.board[row + move][col - move] == 0:
            if piece == WHITE_COORDINATOR or piece == BLACK_COORDINATOR:
                newState.board[row + move][col - move] = piece
                newState.board[row][col] = 0
                if newState.board[king_row][col - move] != 0 and who(newState.board[king_row][col - move]) != whose:
                    newState.board[king_row][col - move] = 0
                if newState.board[row + move][king_col] != 0 and who(newState.board[row + move][king_col]) != whose:
                    newState.board[row + move][king_col] = 0
            elif piece == WHITE_WITHDRAWER or piece == BLACK_WITHDRAWER:
                newState.board[row + move][col - move] = piece
                newState.board[row][col] = 0
                if is_valid(row - 1, col + 1) and newState.board[row - 1][col + 1] != 0 and who(newState.board[row - 1][col + 1]) != whose:
                    newState.board[row - 1][col + 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row + move
                new_col = col - move
                if is_valid(new_row + 1, new_col - 1) and newState.board[new_row + 1][new_col - 1] != 0 and who(newState.board[new_row + 1][new_col - 1]) != whose:
                    if is_valid(new_row + 2, new_col - 2) and newState.board[new_row + 2][new_col - 2] == 0:
                        newState.board[new_row + 1][new_col - 1] = 0
                        new_row += 2
                        new_col -= 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row + move][col - move] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row + move, col - move))
            temp = BC_state(newState.board, newState.whose_move)
            successors = successors + [[new_move, temp]]

        else:
            checking = False
        move += 1

    checking = True
    move = 1
    # Moves in W direction
    while checking:
        newState = BC_state(state.board)
        if is_valid(row, col - move) and newState.board[row][col - move] == 0:
            if piece == WHITE_COORDINATOR or piece == BLACK_COORDINATOR:
                newState.board[row][col - move] = piece
                newState.board[row][col] = 0
                if newState.board[king_row][col - move] != 0 and who(newState.board[king_row][col - move]) != whose:
                    newState.board[king_row][col - move] = 0
                if newState.board[row][king_col] != 0 and who(newState.board[row][king_col]) != whose:
                    newState.board[row][king_col] = 0
            elif piece == WHITE_WITHDRAWER or piece == BLACK_WITHDRAWER:
                newState.board[row][col - move] = piece
                newState.board[row][col] = 0
                if is_valid(row, col + 1) and newState.board[row][col + 1] != 0 and who(newState.board[row][col + 1]) != whose:
                    newState.board[row][col + 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row
                new_col = col - move
                if is_valid(new_row, new_col - 1) and newState.board[new_row][new_col - 1] != 0 and who(newState.board[new_row][new_col - 1]) != whose:
                    if is_valid(new_row, new_col - 2) and newState.board[new_row][new_col - 2] == 0:
                        newState.board[new_row][new_col - 1] = 0
                        new_col -= 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row][col - move] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row, col - move))
            temp = BC_state(newState.board, newState.whose_move)
            successors = successors + [[new_move, temp]]

        else:
            checking = False
        move += 1

    checking = True
    move = 1
    # Moves in NW direction
    while checking:
        newState = BC_state(state.board)
        if is_valid(row - move, col - move) and newState.board[row - move][col - move] == 0:
            if piece == WHITE_COORDINATOR or piece == BLACK_COORDINATOR:
                newState.board[row - move][col - move] = piece
                newState.board[row][col] = 0
                if newState.board[king_row][col - move] != 0 and who(newState.board[king_row][col - move]) != whose:
                    newState.board[king_row][col - move] = 0
                if newState.board[row - move][king_col] != 0 and who(newState.board[row - move][king_col]) != whose:
                    newState.board[row - move][king_col] = 0
            elif piece == WHITE_WITHDRAWER or piece == BLACK_WITHDRAWER:
                newState.board[row - move][col - move] = piece
                newState.board[row][col] = 0
                if is_valid(row + 1, col + 1) and newState.board[row + 1][col + 1] != 0 and who(newState.board[row + 1][col + 1]) != whose:
                    newState.board[row + 1][col + 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row - move
                new_col = col - move
                if is_valid(new_row - 1, new_col - 1) and newState.board[new_row - 1][new_col - 1] != 0 and who(newState.board[new_row - 1][new_col - 1]) != whose:
                    if is_valid(new_row - 2, new_col - 2) and newState.board[new_row - 2][new_col - 2] == 0:
                        newState.board[new_row - 1][new_col - 1] = 0
                        new_col -= 2
                        new_row -= 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row - move][col - move] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row - move, col - move))
            temp = BC_state(newState.board, newState.whose_move)
            successors = successors + [[new_move, temp]]

        else:
            checking = False
        move += 1

    checking = True
    move = 1
    # Moves in N direction
    while checking:
        newState = BC_state(state.board)
        if is_valid(row - move, col) and newState.board[row - move][col] == 0:
            if piece == WHITE_COORDINATOR or piece == BLACK_COORDINATOR:
                newState.board[row - move][col] = piece
                newState.board[row][col] = 0
                if newState.board[king_row][col] != 0 and who(newState.board[king_row][col]) != whose:
                    newState.board[king_row][col] = 0
                if newState.board[row - move][king_col] != 0 and who(newState.board[row - move][king_col]) != whose:
                    newState.board[row - move][king_col] = 0
            elif piece == WHITE_WITHDRAWER or piece == BLACK_WITHDRAWER:
                newState.board[row - move][col] = piece
                newState.board[row][col] = 0
                if is_valid(row + 1, col) and newState.board[row + 1][col] != 0 and who(newState.board[row + 1][col]) != whose:
                    newState.board[row + 1][col] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row - move
                new_col = col
                if is_valid(new_row - 1, new_col) and newState.board[new_row - 1][new_col] != 0 and who(newState.board[new_row - 1][new_col]) != whose:
                    if is_valid(new_row - 2, new_col) and newState.board[new_row - 2][new_col] == 0:
                        newState.board[new_row - 1][new_col] = 0
                        new_row -= 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row - move][col] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row - move, col))
            temp = BC_state(newState.board, newState.whose_move)
            temp.whose_move = 1 - temp.whose_move
            successors = successors + [[new_move, temp]]

        else:
            checking = False
        move += 1

    checking = True
    move = 1
    # Moves in NE direction
    while checking:
        newState = BC_state(state.board)
        if is_valid(row - move, col + move) and newState.board[row - move][col + move] == 0:
            if piece == WHITE_COORDINATOR or piece == BLACK_COORDINATOR:
                newState.board[row - move][col + move] = piece
                newState.board[row][col] = 0
                if newState.board[king_row][col + move] != 0 and who(newState.board[king_row][col + move]) != whose:
                    newState.board[king_row][col + move] = 0
                if newState.board[row - move][king_col] != 0 and who(newState.board[row - move][king_col]) != whose:
                    newState.board[row - move][king_col] = 0
            elif piece == WHITE_WITHDRAWER or piece == BLACK_WITHDRAWER:
                newState.board[row - move][col + move] = piece
                newState.board[row][col] = 0
                if is_valid(row + 1, col - 1) and newState.board[row + 1][col - 1] != 0 and who(newState.board[row + 1][col - 1]) != whose:
                    newState.board[row + 1][col - 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row - move
                new_col = col + move
                if is_valid(new_row - 1, new_col + 1) and newState.board[new_row - 1][new_col + 1] != 0 and who(newState.board[new_row - 1][new_col + 1]) != whose:
                    if is_valid(new_row - 2, new_col + 2) and newState.board[new_row - 2][new_col + 2] == 0:
                        newState.board[new_row - 1][new_col + 1] = 0
                        new_row -= 2
                        new_col += 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row - move][col + move] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row - move, col + move))
            temp = BC_state(newState.board, newState.whose_move)
            successors = successors + [[new_move, temp]]

        else:
            checking = False
        move += 1

    checking = True
    move = 1
    # Moves in E direction
    while checking:
        newState = BC_state(state.board)
        if is_valid(row, col + move) and newState.board[row][col + move] == 0:
            if piece == WHITE_COORDINATOR or piece == BLACK_COORDINATOR:
                newState.board[row][col + move] = piece
                newState.board[row][col] = 0
                if newState.board[king_row][col + move] != 0 and who(newState.board[king_row][col + move]) != whose:
                    newState.board[king_row][col + move] = 0
                if newState.board[row][king_col] != 0 and who(newState.board[row][king_col]) != whose:
                    newState.board[row][king_col] = 0
            elif piece == WHITE_WITHDRAWER or piece == BLACK_WITHDRAWER:
                newState.board[row][col + move] = piece
                newState.board[row][col] = 0
                if is_valid(row, col - 1) and newState.board[row][col - 1] != 0 and who(newState.board[row][col - 1]) != whose:
                    newState.board[row][col - 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row
                new_col = col + move
                if is_valid(new_row, new_col + 1) and newState.board[new_row][new_col + 1] != 0 and who(newState.board[new_row][new_col + 1]) != whose:
                    if is_valid(new_row, new_col + 2) and newState.board[new_row][new_col + 2] == 0:
                        newState.board[new_row][new_col + 1] = 0
                        new_col += 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row][col + move] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row, col + move))
            temp = BC_state(newState.board, newState.whose_move)
            successors = successors + [[new_move, temp]]
            move += 1
        else:
            checking = False

    checking = True
    move = 1
    # Moves in SE direction
    while checking:
        newState = BC_state(state.board)
        if is_valid(row + move, col + move) and newState.board[row + move][col + move] == 0:
            if piece == WHITE_COORDINATOR or piece == BLACK_COORDINATOR:
                newState.board[row + move][col + move] = piece
                newState.board[row][col] = 0
                if newState.board[king_row][col + move] != 0 and who(newState.board[king_row][col + move]) != whose:
                    newState.board[king_row][col + move] = 0
                if newState.board[row + move][king_col] != 0 and who(newState.board[row + move][king_col]) != whose:
                    newState.board[row + move][king_col] = 0
            elif piece == WHITE_WITHDRAWER or piece == BLACK_WITHDRAWER:
                newState.board[row + move][col + move] = piece
                newState.board[row][col] = 0
                if is_valid(row - 1, col - 1) and newState.board[row - 1][col - 1] != 0 and who(newState.board[row - 1][col - 1]) != whose:
                    newState.board[row - 1][col - 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row + move
                new_col = col + move
                if is_valid(new_row + 1, new_col + 1) and newState.board[new_row + 1][new_col + 1] != 0 and who(newState.board[new_row + 1][new_col + 1]) != whose:
                    if is_valid(new_row + 2, new_col + 2) and newState.board[new_row + 2][new_col + 2] == 0:
                        newState.board[new_row + 1][new_col + 1] = 0
                        new_row += 2
                        new_col += 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row + move][col + move] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row + move, col + move))
            temp = BC_state(newState.board, newState.whose_move)
            successors = successors + [[new_move, temp]]
            move += 1
        else:
            checking = False
    return successors


def is_frozen(state, row, col):
    piece = state.board[row][col]
    frozen = False
    b = state.board

    if is_valid(row + 1, col) and (b[row + 1][col] == 14 or b[row + 1][col] == 15 or ((b[row + 1][col] == 8 or b[row + 1][col] == 9) and (piece == 14 or piece == 15))) and \
            who(b[row + 1][col]) != who(piece) and piece != 0:
        frozen = True
    if is_valid(row + 1, col - 1) and (b[row + 1][col - 1] == 14 or b[row + 1][col - 1] == 15 or ((b[row + 1][col - 1] == 8 or b[row + 1][col - 1] == 9) and \
            (piece == 14 or piece == 15))) and who(b[row + 1][col - 1]) != who(piece) and piece != 0:\
        frozen = True
    if is_valid(row, col - 1) and (b[row][col - 1] == 14 or b[row][col - 1] == 15 or ((b[row][col - 1] == 8 or b[row][col - 1] == 9) and (piece == 14 or piece == 15))) and \
            who(b[row][col - 1]) != who(piece) and piece != 0:\
        frozen = True
    if is_valid(row - 1, col - 1) and (b[row - 1][col - 1] == 14 or b[row - 1][col - 1] == 15 or ((b[row - 1][col - 1] == 8 or b[row - 1][col - 1] == 9) and \
            (piece == 14 or piece == 15))) and who(b[row - 1][col - 1]) != who(piece) and piece != 0:\
        frozen = True
    if is_valid(row - 1, col) and (b[row - 1][col] == 14 or b[row - 1][col] == 15 or ((b[row - 1][col] == 8 or b[row - 1][col] == 9) and (piece == 14 or piece == 15))) and \
            who(b[row - 1][col]) != who(piece) and piece != 0:\
        frozen = True
    if is_valid(row - 1, col + 1) and (b[row - 1][col + 1] == 14 or b[row - 1][col + 1] == 15 or ((b[row - 1][col + 1] == 8 or b[row - 1][col + 1] == 9) and \
            (piece == 14 or piece == 15))) and who(b[row - 1][col + 1]) != who(piece) and piece != 0:\
        frozen = True
    if is_valid(row, col + 1) and (b[row][col + 1] == 14 or b[row][col + 1] == 15 or ((b[row][col + 1] == 8 or b[row][col + 1] == 9) and (piece == 14 or piece == 15))) and \
            who(b[row][col + 1]) != who(piece) and piece != 0:\
        frozen = True
    if is_valid(row + 1, col + 1) and (b[row + 1][col + 1] == 14 or b[row + 1][col + 1] == 15 or ((b[row + 1][col + 1] == 8 or b[row + 1][col + 1] == 9) and \
            (piece == 14 or piece == 15))) and who(b[row + 1][col + 1]) != who(piece) and piece != 0:\
        frozen = True
    
    
    return frozen


def find_kings(state):
    board = state.board
    locs = [-1, -1, -1, -1]
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == 12 or piece == 13:
                if who(piece) == state.whose_move:
                    locs[0] = row
                    locs[1] = col
                else:
                    locs[2] = row
                    locs[3] = col
            if locs[0] != -1 and locs[2] != -1:
                return locs
    return locs


# King
# does not return captured list
# returns legal moves and new state resulting from move
# does not include imitator
def move_king(currentState, row, col):
    king = currentState.board[row][col]
    possibleStates = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_valid(row+i, col+j):
                if is_frozen(currentState, row, col):
                    return []
                newState = BC_state(currentState.board)
                # checking imitator capturing king
                if king == 8 and currentState.board[row+i][col+j] == 13 or \
                        king == 9 and currentState.board[row+i][col+j] == 12:
                    move = ((row, col), (row+i, col+j))
                    newState.board[row+i][col+j] = king
                    newState.board[row][col] = 0
                    temp = BC_state(newState.board, newState.whose_move)
                    return [[move, temp]]
                # move king if empty spot next to it or the opposing teams occupying it
                if (king == 12 or king == 13) and (currentState.board[row+i][col+j] == 0 or \
                        who(king) != who(currentState.board[row+i][col+j])):
                    # update new position with king and remove the original
                    newState.board[row+i][col+j] = king
                    newState.board[row][col] = 0
                    move = ((row, col), (row+i, col+j))
                    temp = BC_state(newState.board, newState.whose_move)
                    possibleStates = possibleStates + [[move, temp]]
    return possibleStates


# Pincer
# does not return captured list
# returns legal moves and new state resulting from move
# removes captured pieces from the board
# does not include imitator
def move_pincer(currentState, row, col):
    pincer = currentState.board[row][col]
    possibleStates = []

    if is_frozen(currentState, row, col):
        return []

    for i in range(1, 8):
        newState = BC_state(currentState.board)
        # south direction
        if pincer != 8 and pincer != 9:
            if is_valid(row+i, col):
                if currentState.board[row+i][col] == 0:
                    newState.board[row+i][col] = pincer
                    newState.board[row][col] = 0
                    move = ((row, col), (row+i, col))
                    newState = pincer_capture(newState, row+i, col)
                    temp = BC_state(newState.board, newState.whose_move)
                    possibleStates = possibleStates + [[move, temp]]
                else: break
        else:
            if is_valid(row+i+1, col):
                if (currentState.board[row+i+1][col] == 3 or currentState.board[row+i+1][col] == 2) and \
                        who(currentState.board[row+i+1][col]) != who(currentState.board[row][col]) and \
                            newState.board[row + i][col] == 0:
                    newState.board[row+i][col] = pincer
                    newState.board[row][col] = 0
                    newState = pincer_capture(newState, row+i, col)
                    move = ((row, col), (row+i, col))
                    temp = BC_state(newState.board, newState.whose_move)
                    return [[move, temp]]
                elif currentState.board[row+i][col] != 0: break
    for i in range(1, 8):
        newState = BC_state(currentState.board)
        # north direction
        if pincer != 8 and pincer != 9:
            if is_valid(row-i, col):
                if currentState.board[row-i][col] == 0:
                    newState.board[row-i][col] = pincer
                    newState.board[row][col] = 0
                    move = ((row, col), (row-i, col))
                    newState = pincer_capture(newState, row-i, col)
                    temp = BC_state(newState.board, newState.whose_move)
                    possibleStates = possibleStates + [[move, temp]]
                else: break
        else:
            if is_valid(row-i-1, col):
                if (currentState.board[row-i-1][col] == 3 or currentState.board[row-i-1][col] == 2) and \
                        who(currentState.board[row-i-1][col]) != who(currentState.board[row][col]) and \
                            newState.board[row-i][col] == 0:
                    newState.board[row-i][col] = pincer
                    newState.board[row][col] = 0
                    newState = pincer_capture(newState, row-i, col)
                    move = ((row, col), (row-i, col))
                    temp = BC_state(newState.board, newState.whose_move)
                    return [[move, temp]]
                elif currentState.board[row-i][col] != 0: break
    for i in range(1, 8):
        # east direction
        newState = BC_state(currentState.board)
        if pincer != 8 and pincer != 9:
            if is_valid(row, col+i):
                if currentState.board[row][col+i] == 0:
                    newState.board[row][col+i] = pincer
                    newState.board[row][col] = 0
                    move = ((row, col), (row, col+i))
                    newState = pincer_capture(newState, row, col+i)
                    temp = BC_state(newState.board, newState.whose_move)
                    possibleStates = possibleStates + [[move, temp]]
                else: break
        else:
            if is_valid(row, col+i+1):
                if (currentState.board[row][col+i+1] == 3 or currentState.board[row][col+i+1] == 2) and \
                        who(currentState.board[row][col+i+1]) != who(currentState.board[row][col]) and \
                            newState.board[row][col+i] == 0:
                    newState.board[row][col+i] = pincer
                    newState.board[row][col] = 0
                    newState = pincer_capture(newState, row, col+i)
                    move = ((row, col), (row, col+i))
                    temp = BC_state(newState.board, newState.whose_move)
                    return [[move, temp]]
                elif currentState.board[row][col+i] != 0: break
    for i in range(1, 8):
        # west direction
        newState = BC_state(currentState.board)
        if pincer != 8 and pincer != 9:
            if is_valid(row, col-i):
                if currentState.board[row][col-i] == 0:
                    newState.board[row][col-i] = pincer
                    newState.board[row][col] = 0
                    move = ((row, col), (row, col-i))
                    newState = pincer_capture(newState, row, col-i)
                    temp = BC_state(newState.board, newState.whose_move)
                    possibleStates = possibleStates + [[move, temp]]
                else: break
        else:
            if is_valid(row, col-i-1):
                if (currentState.board[row][col-i-1] == 3 or currentState.board[row][col-i-1] == 2) and \
                        who(currentState.board[row][col-i-1]) != who(currentState.board[row][col]) and \
                            newState.board[row][col-i] == 0:
                    newState.board[row][col-i] = pincer
                    newState.board[row][col] = 0
                    newState = pincer_capture(newState, row, col-i)
                    move = ((row, col), (row, col-i))
                    temp = BC_state(newState.board, newState.whose_move)
                    return [[move, temp]]
                elif currentState.board[row][col-i] != 0: break
    # return all possible states for the board
    return possibleStates


def pincer_capture(newState, row, col):
    updatedBoard = BC_state(newState.board)
    for i in range (-1, 2):
        for j in range (-1, 2):
            # only can capture vertically and horizontally
            if i != 0 and j == 0 or i == 0 and j!= 0:
                if 0 <= row + 2*i < 8 and 0 <= col + 2*j < 8:
                    if updatedBoard.board[row+i][col+j] != 0 and \
                            who(updatedBoard.board[row+2*i][col+2*j]) == who(updatedBoard.board[row][col]) and \
                            who(updatedBoard.board[row+i][col+j]) != who(updatedBoard.board[row][col]) and \
                            updatedBoard.board[row+2*i][col+2*j]!= 0:
                        # captured
                        # imitator can only capture pincers
                        if updatedBoard.board[row][col] == 8 and updatedBoard.board[row+i][col+j] == 3 or \
                            updatedBoard.board[row][col] == 9 and updatedBoard.board[row+i][col+j] == 2:
                            updatedBoard.board[row+i][col+j] = 0
                        elif updatedBoard.board[row][col] != 8 and updatedBoard.board[row][col] != 9:
                            updatedBoard.board[row+i][col+j] = 0
    # return same board if no captures
    # or new board with all the captured pieces removed
    return updatedBoard


def makeMove(currentState, currentRemark, timelimit=10):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.
    global count, chosenState, BASIC_REMARKS, MAX_PLY
    # The following is a placeholder that just copies the current state.
    newState = BC_state(currentState.board)

    # Fix up whose turn it will be.
    # newState.whose_move = 1 - currentState.whose_move

    global TIME_LIMIT, START_TIME
    TIME_LIMIT = timelimit
    START_TIME = time.perf_counter()
    bestMove = None

    # worry: more plys than possible
    totalPieces = getPiece(currentState)
    if totalPieces > 24:
        MAX_PLY = 3
    elif 16 < totalPieces <= 24:
        MAX_PLY = 4
    elif 8 < totalPieces <= 16:
        MAX_PLY = 5
    elif totalPieces <= 8:
        MAX_PLY = 6
   #s = parameterized_minimax(currentState, ply=MAX_PLY, alphaBeta=False, useBasicStaticEval=False)
    for ply in range(1, MAX_PLY):
        s = parameterized_minimax(currentState, ply=ply, alphaBeta=False, useBasicStaticEval=False)
        if bestMove == None:
            bestMove = chosenState
        else:
            if currentState.whose_move == WHITE:
                if staticEval(bestMove[1]) > staticEval(chosenState[1]):
                    bestMove = chosenState
            else:
                if staticEval(bestMove[1]) < staticEval(chosenState[1]):
                    bestMove = chosenState

    if count == 12:
        newRemark = "I make my move, " + str(bestMove[0]) + ". Nice, yeah?"
    elif count == 13:
        newRemark = "Hm... only " + str(getPiece(bestMove[1]) + " pieces left...")
    else:
        newRemark = BASIC_REMARKS[count % 12]
        count = -1
    count = count + 1
    return [bestMove, newRemark]


def getPiece(state):
    pieces = 0
    for row in range(8):
        for col in range(8):
            if state.board[row][col] != 0:
                pieces = pieces + 1
    return pieces


def translate_move_coord(move):
    fr = ''
    to = ''
    for i in range(2):
        num = 0
        letter = 'a'
        for j in range(2):
            if j == 0:
                num = 8 - move[i][j]
            if j == 1:
                letter = str(chr(move[i][j] + 97))
        if i == 0:
            fr = fr + letter + str(num)
        if i == 1:
            to = to + letter + str(num)
    coord = fr+to
    return coord


def nickname():
    return "Jungkook"


def introduce():
    return "Annyeonghaseyo!! I'm Jungkook from BTS, a newbie Baroque Chess agent. " \
           "I was created by Hari Kaushik (harik98@uw.edu) and Lisa Qing (lisaq2@uw.edu)!"


def prepare(player2Nickname):
    ''' Here the game master will give your agent the nickname of
    the opponent agent, in case your agent can use it in some of
    the dialog responses.  Other than that, this function can be
    used for initializing data structures, if needed.'''
    global BASIC_REMARKS
    OPONENT_NAME = player2Nickname

    # Additional remarks added in can move regarding to what moves are being made
    BASIC_REMARKS = ["I hope this game turns out well for me..., " + OPONENT_NAME + ".",
                    "Daebak. This game is getting kind of intense, " + OPONENT_NAME + ".",
                    "I hope you're having fun, " + OPONENT_NAME + ".",
                    "Wow. I'm getting tired already... Can someone get me some banana milk",
                    "Why don't you practice some more befor challenging me again.",
                    "I'm on a very busy schedule. Can you do any better?",
                    "Wow, do you know what would make this game better? Listening to my new album.",
                    "Sorry, I'm just too good. Catch me at the Grammys.",
                    "Can you make this more interesting? I'm getting bored.", 
                    "I have a concert to play at... Can we speed this up, " + OPONENT_NAME + "??",
                    "I have a lot of fans waiting for me. I need to finish this quickly.",
                    "Yo, listen to this bop, Boy with Luv. It'll make the game more fun."]


def basicStaticEval(state):
    '''Use the simple method for state evaluation described in the spec. This is typically
	used in parameterized_minimax calls to verify that minimax and alpha-beta pruning work
	correctly.'''
    total = 0
    for row in state.board:
        for col in row:
            total = total + pieceVal(col)
    return total


def pieceVal(piece):
	# black pieces
    if piece == BLACK_PINCER:
        return -1
    elif piece == BLACK_KING:
        return -100
    elif who(piece) == BLACK and piece != 0:
        return -2

	# white pieces
    elif piece == WHITE_PINCER:
        return 1
    elif piece == WHITE_KING:
        return 100
    elif who(piece) == WHITE and piece != 0:
        return 2

    # empty spaces
    else:
        return 0


def staticEval(state):
    '''Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.'''
    b = state.board
    score = 0.0
    king_locs = find_kings(state)
    whose = state.whose_move
    for row in range(8):
        for col in range(8):
            piece = b[row][col]
            score += piece_vals.get(piece) # - (0.25 * middle_vals[row][col] * -1 ** whose)
            if who(piece) == BLACK and piece != 0:
                score -= piece_advance[row][col] * 5
            elif who(piece) == WHITE:
                score += piece_advance[7-row][col] * 5
            if piece == BLACK_KING:
                score -= (2 * edge_vals[row][col])
            elif piece == WHITE_KING:
                score += (2 * edge_vals[row][col])
            
            if (who(piece) == whose and row != king_locs[0] and col != king_locs[1]) or \
                    (who(piece) != whose and row != king_locs[2] and col != king_locs[3]):
                if piece == BLACK_COORDINATOR:
                    score -= 5
                elif piece == WHITE_COORDINATOR:
                    score += 5

            if is_frozen(state, row, col):
                score -= 0.75 * piece_vals.get(piece)

            if piece == BLACK_WITHDRAWER or piece == WHITE_WITHDRAWER:
                reduction = 0
                for i in range(-1,2):
                    for j in range(-1,2):
                        temp_row = row + i
                        temp_col = col + j
                        temp_row2 = row - i
                        temp_col2 = col - j

                        # adj = b[temp_row][temp_col]
                        # opp = b[temp_row2][temp_col2]
                        if is_valid(temp_row, temp_col) and i != 0 and j != 0 and is_valid(temp_row2, temp_col2):
                            if b[temp_row][temp_col] != 0 and who(b[temp_row][temp_col]) != piece and b[temp_row2][temp_col2] == 0:
                                if abs(piece_vals.get(b[temp_row][temp_col])) > abs(reduction):
                                    reduction = piece_vals.get(b[temp_row][temp_col])
                score += reduction / 10
            
            if piece == BLACK_PINCER or piece == WHITE_PINCER: # pincer
                for i in range(-2, 3, 4):
                    if 0 <= row + i < 8:
                        row_temp = b[row + i][col]
                        if row_temp == piece:
                            score += piece_vals.get(row_temp) / 4
                    if 0 <= col + i < 8:
                        col_temp = b[row][col + i]
                        if col_temp == piece:
                            score += piece_vals.get(col_temp) / 4
                
                if piece == BLACK_PINCER:
                    if who(piece) == whose:
                        score -= (8 - (abs(row - king_locs[0]) + abs(col - king_locs[1])))
                    elif who(piece) != whose:
                        score -= (8 - (abs(row - king_locs[2]) + abs(col - king_locs[3])))
                    score -= middle_vals[row][col]
                if piece == WHITE_PINCER: 
                    if who(piece) == whose:
                        score += (8 - (abs(row - king_locs[0]) + abs(col - king_locs[1])))
                    elif who(piece) != whose:
                        score += (8 - (abs(row - king_locs[2]) + abs(col - king_locs[3])))
                    score += middle_vals[row][col]
                        
    return score