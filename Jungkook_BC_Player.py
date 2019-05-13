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


def parameterized_minimax(currentState, alphaBeta=False, ply=3, \
                          useBasicStaticEval=True, useZobristHashing=False):
    '''Implement this testing function for your agent's basic
    capabilities here.'''
    global N_STATIC_EVALS, N_STATES_EXPANDED, N_CUTOFFS, CURRENT_STATE_STATIC_VAL

    # using alpha beta pruning
    if alphaBeta:
        alpha = +100000
        beta = -100000
        provisional = pruned_minimaxHelper(currentState, alpha, beta, ply, useBasicStaticEval, useZobristHashing)
    else:
        provisional = minimaxHelper(currentState, ply, useBasicStaticEval, useZobristHashing)

    return {"CURRENT_STATE_STATIC_VAL": provisional, "N_STATES_EXPANDED": N_STATES_EXPANDED,
            "N_STATIC_EVALS": N_STATIC_EVALS, "N_CUTOFFS": N_CUTOFFS}



def minimaxHelper(currentState, ply, useBasicStaticEval=True, useZobristHashing=False):
    global N_STATIC_EVALS, N_STATES_EXPANDED, N_CUTOFFS, CURRENT_STATE_STATIC_VAL

    if ply == 0 and useBasicStaticEval:
        N_STATIC_EVALS = N_STATIC_EVALS + 1
        print(basicStaticEval(currentState))
        return basicStaticEval(currentState), currentState
    if ply % 2 == MAX_PLY % 2:
        provisional = -100000
    else:
        provisional = 100000
    successors = generate_successors(currentState)
    # Problem in sorting: bc state is not subscriptable
    # successors = sorted(successors, key=lambda k: [k[0], k[1]])
    for s in successors:
        N_STATES_EXPANDED = N_STATES_EXPANDED + 1
        # how to pass in just the state of successors of form [(move, move), newstate]
        newVal, newMove = minimaxHelper(s, ply - 1)
        if ply % 2 == MAX_PLY % 2 and newVal > provisional or ply % 2 != MAX_PLY % 2 and newVal < provisional:
            provisional = newVal

    return provisional


def pruned_minimaxHelper(currentState, alpha, beta, ply, useBasicStaticEval=True, useZobristHashing=False):
    return 1000


def generate_successors(state):
    successors = []
    for row in range(8):
        for col in range(8):
            piece = state.board[row][col]
            # if who(sq) == currentState.whose_move and sq > 0:
            if who(piece) == state.whose_move and piece > 0 and not is_frozen(state, row, col):
                if piece == WHITE_PINCER or piece == BLACK_PINCER or piece == WHITE_IMITATOR or piece == BLACK_IMITATOR:
                    successors = successors + move_pincer(state, row, col)
                if piece == WHITE_KING or piece == BLACK_KING or piece == WHITE_IMITATOR or piece == BLACK_IMITATOR:
                    successors = successors + move_king(state, row, col)
                if piece > 3 and piece != 12 and piece != 13:
                    successors = successors + move_like_queen(state, row, col)
    return successors


def is_valid(row, col):
    if 0 <= row < 8 and 0 <= col < 8:
        return True
    return False


def move_like_queen(state, row, col):
    piece = state.board[row][col]
    board = state.board
    kings = find_kings(state)
    king_row = kings[0]
    king_col = kings[1]
    whose = who(piece)
    successors = []
    captures = []

    checking = True
    move = 1

    # Moves in S direction
    while checking:
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
                if row - 1 > -1 and newState.board[row - 1][col] != 0 and who(newState.board[row - 1][col]) != whose:
                    newState.board[row - 1][col] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row + move
                new_col = col
                if newState.board[new_row + 1][new_col] != 0 and who(newState.board[new_row + 1][new_col]) != whose:
                    if is_valid(new_row + 2, new_col) and newState.board[new_row + 2][new_col] == 0:
                        newState.board[new_row + 1][new_col] = 0
                        new_row += 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row + move][col] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row + move, col))
            temp = BC_state(newState.board)
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
                if newState.board[row - 1][col + 1] != 0 and who(newState.board[row - 1][col + 1]) != whose:
                    newState.board[row - 1][col + 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row + move
                new_col = col - move
                if newState.board[new_row + 1][new_col - 1] != 0 and who(newState.board[new_row + 1][new_col - 1]) != whose:
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
            temp = BC_state(newState.board)
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
                if newState.board[row][col + 1] != 0 and who(newState.board[row][col + 1]) != whose:
                    newState.board[row][col + 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row
                new_col = col - move
                if newState.board[new_row][new_col - 1] != 0 and who(newState.board[new_row][new_col - 1]) != whose:
                    if is_valid(new_row, new_col - 2) and newState.board[new_row][new_col - 2] == 0:
                        newState.board[new_row][new_col - 1] = 0
                        new_col -= 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row][col - move] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row, col - move))
            temp = BC_state(newState.board)
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
                if newState.board[row + 1][col + 1] != 0 and who(newState.board[row + 1][col + 1]) != whose:
                    newState.board[row + 1][col + 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row - move
                new_col = col - move
                if newState.board[new_row - 1][new_col - 1] != 0 and who(newState.board[new_row - 1][new_col - 1]) != whose:
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
            temp = BC_state(newState.board)
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
                if newState.board[row + 1][col] != 0 and who(newState.board[row + 1][col]) != whose:
                    newState.board[row + 1][col] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row - move
                new_col = col
                if newState.board[new_row - 1][new_col] != 0 and who(newState.board[new_row - 1][new_col]) != whose:
                    if is_valid(new_row - 2, new_col) and newState.board[new_row - 2][new_col] == 0:
                        newState.board[new_row - 1][new_col] = 0
                        new_row -= 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row - move][col] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row - move, col))
            temp = BC_state(newState.board)
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
                if newState.board[row + 1][col - 1] != 0 and who(newState.board[row + 1][col - 1]) != whose:
                    newState.board[row + 1][col - 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row - move
                new_col = col + move
                if newState.board[new_row - 1][new_col + 1] != 0 and who(newState.board[new_row - 1][new_col + 1]) != whose:
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
            temp = BC_state(newState.board)
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
                if newState.board[row][col - 1] != 0 and who(newState.board[row][col - 1]) != whose:
                    newState.board[row][col - 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row
                new_col = col + move
                if newState.board[new_row][new_col + 1] != 0 and who(newState.board[new_row][new_col + 1]) != whose:
                    if is_valid(new_row, new_col + 2) and newState.board[new_row][new_col + 2] == 0:
                        newState.board[new_row][new_col + 1] = 0
                        new_col += 2
                newState.board[new_row][new_col] = piece
                newState.board[row][col] = 0
            else:
                newState.board[row][col + move] = piece
                newState.board[row][col] = 0
            new_move = ((row, col), (row, col + move))
            temp = BC_state(newState.board)
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
                if newState.board[row - 1][col - 1] != 0 and who(newState.board[row - 1][col - 1]) != whose:
                    newState.board[row - 1][col - 1] = 0
            elif piece == WHITE_LEAPER or piece == BLACK_LEAPER:
                new_row = row + move
                new_col = col + move
                if newState.board[new_row + 1][new_col + 1] != 0 and who(newState.board[new_row + 1][new_col + 1]) != whose:
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
            temp = BC_state(newState.board)
            successors = successors + [[new_move, temp]]
            move += 1
        else:
            checking = False
    return successors


def is_frozen(state, row, col):
    piece = state.board[row][col]
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i != 0 and j != 0) and is_valid(row + i, col + j):
                b = state.board
                if b[row + i][col + j] == 15 or b[row + i][col + j] == 14:
                    if who(b[row + i][col + j]) != who(piece):
                        return True
    return False


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
                    return [[move, newState]]                      
                # move king if empty spot next to it or the opposing teams occupying it
                if (king == 12 or king == 13) and (currentState.board[row+i][col+j] == 0 or \
                        who(king) != who(currentState.board[row+i][col+j])):
                    # update new position with king and remove the original
                    newState.board[row+i][col+j] = king
                    newState.board[row][col] = 0
                    move = ((row, col), (row+i, col+j))
                    possibleStates = possibleStates + [[move, newState]]
    return possibleStates


# Pincer
# does not return captured list
# returns legal moves and new state resulting from move
# removes captured pieces from the board
# does not include imitator
def move_pincer(currentState, row, col):
    pincer = currentState.board[row][col]
    possibleStates = []
    if pincer == 8 or pincer == 9:
        print("HELLO")

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
                    possibleStates = possibleStates + [[move, newState]]
                else: break
        else:
            if is_valid(row+i+1, col):
                if (currentState.board[row+i+1][col] == 3 or currentState.board[row+i+1][col] == 2) and \
                        who(currentState.board[row+i+1][col]) != who(currentState.board[row][col]):
                    newState.board[row+i][col] = pincer
                    newState.board[row][col] = 0
                    newState = pincer_capture(newState, row+i, col)
                    move = ((row, col), (row+i, col))
                    return [[move, newState]]
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
                    possibleStates = possibleStates + [[move, newState]]
                else: break
        else:
            if is_valid(row-i-1, col):
                if (currentState.board[row-i-1][col] == 3 or currentState.board[row-i-1][col] == 2) and \
                        who(currentState.board[row-i-1][col]) != who(currentState.board[row][col]):
                    newState.board[row-i][col] = pincer
                    newState.board[row][col] = 0
                    newState = pincer_capture(newState, row-i, col)
                    move = ((row, col), (row-i, col))
                    return [[move, newState]]
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
                    possibleStates = possibleStates + [[move, newState]]
                else: break
        else:
            if is_valid(row, col+i+1):
                if (currentState.board[row][col+i+1] == 3 or currentState.board[row][col+i+1] == 2) and \
                        who(currentState.board[row][col+i+1]) != who(currentState.board[row][col]):
                    newState.board[row][col+i] = pincer
                    newState.board[row][col] = 0
                    newState = pincer_capture(newState, row, col+i)
                    move = ((row, col), (row, col+i))
                    return [[move, newState]]
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
                    possibleStates = possibleStates + [[move, newState]]
                else: break
        else:
            if is_valid(row, col-i-1):
                if (currentState.board[row][col-i-1] == 3 or currentState.board[row][col-i-1] == 2) and \
                        who(currentState.board[row][col-i-1]) != who(currentState.board[row][col]):
                    newState.board[row][col-i] = pincer
                    newState.board[row][col] = 0
                    newState = pincer_capture(newState, row, col-i)
                    move = ((row, col), (row, col-i))
                    return [[move, newState]]
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
                            who(updatedBoard.board[row+i][col+j]) != who(updatedBoard.board[row][col]):
                        # captured
                        updatedBoard.board[row+i][col+j] = 0
    # return same board if no captures
    # or new board with all the captured pieces removed 
    return updatedBoard


def makeMove(currentState, currentRemark, timelimit=10):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.

    # The following is a placeholder that just copies the current state.
    newState = BC_state(currentState.board)

    # Fix up whose turn it will be.
    #newState.whose_move = 1 - currentState.whose_move
    
    startTime = time.perf_counter()
    #while time.perf_counter()-startTime < timelimit - float(.1):
        
    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:

    
    successors = generate_successors(currentState)
    print(successors)

    #move = ((6, 4), (3, 4))
    move = successors[2][0]
    newState = successors[2][1]
    newState.whose_move = 1 - currentState.whose_move
    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]

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
    coord = (fr, to)
    return coord
                


def nickname():
    return "Jungkook"


def introduce():
    return "I'm Jungkook from BTS, a newbie Baroque Chess agent. " \
           "I was created by Hari Kaushik (harik98@uw.edu) and Lisa Qing (lisaq2@uw.edu)!"


def prepare(player2Nickname):
    ''' Here the game master will give your agent the nickname of
    the opponent agent, in case your agent can use it in some of
    the dialog responses.  Other than that, this function can be
    used for initializing data structures, if needed.'''
    OPONENT_NAME = player2Nickname

    # Additional remarks added in can move regarding to what moves are being made
    BASIC_REMARKS = ["I hope this game turns out well for me...," + OPONENT_NAME + ".",
                    "This game is getting kind of intense, " + OPONENT_NAME + ".", 
                    "I hope you're having fun, " + OPONENT_NAME + ".",
                    "Wow. I'm getting tired already...",
                    "Why don't you practice some more befor challenging me again.",
                    "Can you do any better?", 
                    "Sorry, I'm just too good.",
                    "Can you make this more interesting? I'm getting bored."]



def basicStaticEval(state):
	'''Use the simple method for state evaluation described in the spec. This is typically
	used in parameterized_minimax calls to verify that minimax and alpha-beta pruning work
	correctly.'''

	# The value of the function is the sum of the values of the pieces on the board in the given state
	total = 0
	for row in state.board:
		for col in row:
			total = total + pieceVal(col)


def pieceVal(piece):
	# black pieces
    if piece == BLACK_PINCER:
        return -1
    elif piece == BLACK_KING:
        return -100
    elif who(piece) == BLACK:
        return -2

	# white pieces
    elif piece == WHITE_PINCER:
        return 1
    elif piece == WHITE_KING:
        return 100
    elif who(piece) == WHITE:
        return 2

    # empty spaces
    else:
        return 0

def staticEval(state):
    currentState = state.board
    
    '''Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.'''
    pass