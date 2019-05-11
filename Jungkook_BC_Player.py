'''Jungkook_BC_Player.py
The beginnings of an agent that might someday play Baroque Chess.

'''

from BC_state_etc import *

pieces = []

def parameterized_minimax(currentState, alphaBeta=False, ply=3, \
                          useBasicStaticEval=True, useZobristHashing=False):
    '''Implement this testing function for your agent's basic
    capabilities here.'''
    successors = generate_successors(currentState)

    pass

def generate_successors(currentState):
    successors = []
    for i in range(8):
        for j in range(8):
            sq = currentState.board[i][j]
            # if who(sq) == currentState.whose_move and sq > 0:


def is_valid(row, col):
    if 0 <= row < 8 and 0 <= col < 8:
        return True
    return False

def move_coordinator(state, row, col):
    piece = state.board[row][col]
    board = state.board
    kings = find_kings(state)
    kingX = kings[0]
    kingY = kings[1]
    whose = who(piece)
    # newState = BC_state(board)
    successors = []
    captures = []

    checking = True
    move = 1

    while checking:
        kill = False
        temp = BC_state(state.board)
        if not is_valid(row + move, col) or temp.board[row + move][col] != 0:
            break
        temp.board[row + move][col] = temp.board[row][col]
        temp.board[row][col] = 0
        if piece is 4 or piece is 5:
            intersect1 = -1
            intersect2 = -1
            if who(temp.board[kingX][col]) != who(temp.board[row][col + move] and temp.board[kingX][col + move] != 0:
                intersect1 = temp.board[kingX][col]
                temp.board[kingX][col] = 0
                kill = True

            if who(temp.board[row+move][kingCol])
            



def find_kings(state):
    board = state.board
    locs = [-1, -1, -1, -1]
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == 12 or piece == 13:
                if who(piece) == state.whose_turn:
                    locs[0] = row
                    locs[1] = col
                else:
                    locs[2] = row
                    locs[3] = col
            if locs[0] != -1 and locs[2] != -1:
                return locs
    return locs

def makeMove(currentState, currentRemark, timelimit=10):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.

    # The following is a placeholder that just copies the current state.
    newState = BC_state(currentState.board)

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = ((6, 4), (3, 4))

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]


def nickname():
    return "Jungkook"


def introduce():
    return "I'm Jungkook from BTS, a newbie Baroque Chess agent. " \
           "I was created by Hari Kaushik (harik98@uw.edu) and Lisa Qing (@uw.edu)!"


def prepare(player2Nickname):
    ''' Here the game master will give your agent the nickname of
    the opponent agent, in case your agent can use it in some of
    the dialog responses.  Other than that, this function can be
    used for initializing data structures, if needed.'''
    pass


def basicStaticEval(state):
    '''Use the simple method for state evaluation described in the spec.
    This is typically used in parameterized_minimax calls to verify
    that minimax and alpha-beta pruning work correctly.'''
    pass


def staticEval(state):
    '''Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.'''
    pass

def checkImmobilized(state, row, col, piece):
    if state[row][col] is 14 or 15:
        # checking if the piece is immobilized
        team = state[row][col] % 2
        if team != piece % 2:
            return True
    return False

# King
# does not return captured list
# returns legal move and new state resulting from move
# does not include imitator

def move_king(currentState, row, col):
    king = currentState.board[row][col]
    possibleStates = []

    for i in range (-1, 2):
        for j in range(-1, 2):
            if (i != 0 and j!= 0) and 0 <= row + i < 8 and 0 <= col + j < 8:
                if checkImmobilized(currentState.board, row + i, col + j, king):
                    return []
                newState = BC_state(currentState.board)
                if currentState.board[row+i][col+j] == 0 or \
                        king % 2 != currentState.board[row+i][col+j] % 2:
                    newState.board[row+i][col+j] = king
                    newState.board[row][col] = 0
                    move = ((row, col), (row+i, row+j))
                    possibleStates = possibleStates + [move, newState]
    return possibleStates