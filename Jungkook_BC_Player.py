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
            if who(sq) == currentState.whose_move and sq > 0:


def piece_noncapture_moves(i, j, currentState):
    moves = []
    sq = currentState.board[i][j]
    if sq // 2 == 1:
        directions = [NORTH, WEST, EAST, SOUTH]
    else:
        directions = [NORTH, SOUTH, WEST, EAST, NW, NE, SW, SE]
    if sq // 2 == 1:
        distance = 7
        while distance > 0:

        # for y in range(8):
        #     empty = True
        #     delta = 1
        #     curr = j
        #     if j > y: delta = -1
        #     while curr != y and empty:
        #         if currentState.board[i][curr] != 0:
        #             empty = False
        #         curr += delta
        #     if currentState.board[i][y] != 0 and empty:
        #         new_board = [r[:] for r in currentState.board]
        #         new_board[i][y] = sq
        #         new_board[i][j] = 0
        #         moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))
        # for x in range(8):
        #     empty = True
        #     delta = 1
        #     curr = j
        #     if j > x: delta = -1
        #     while curr != x and empty:
        #         if currentState.board[curr][j] != 0:
        #             empty = False
        #         curr += delta
        #     if currentState.board[x][j] != 0 and empty:
        #         new_board = [r[:] for r in currentState.board]
        #         new_board[x][j] = sq
        #         new_board[i][j] = 0
        #         moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))

    if sq // 2 == 1:
        directions = [NORTH, SOUTH, WEST, EAST]
    else:
        directions = [NORTH, SOUTH, WEST, EAST, NW, NE, SW, SE]
    # for dir in directions:
    #     spaces = 1
    #
    #     if dir == NORTH:
    #         while(currentState.board[i][j - spaces] == 0):
    #             new_board = [r[:] for r in currentState.board]
    #             new_board[i][j - spaces] = sq
    #             new_board[i][j] = 0
    #             moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))
    #             spaces += 1
    #     if dir == SOUTH:
    #         while currentState.board[i][j + spaces] == 0:
    #             new_board = [r[:] for r in currentState.board]
    #             new_board[i][j + spaces] = sq
    #             new_board[i][j] = 0
    #             moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))
    #             spaces += 1
    #     if dir == EAST:
    #         while currentState.board[i + spaces][j] == 0:
    #             new_board = [r[:] for r in currentState.board]
    #             new_board[i + spaces][j] = sq
    #             new_board[i][j] = 0
    #             moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))
    #             spaces += 1
    #     if dir == WEST:
    #         while currentState.board[i - spaces][j] == 0:
    #             new_board = [r[:] for r in currentState.board]
    #             new_board[i - spaces][j] = sq
    #             new_board[i][j] = 0
    #             moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))
    #             spaces += 1
    #     if dir == NW:
    #         while currentState.board[i - spaces][j - spaces] == 0:
    #             new_board = [r[:] for r in currentState.board]
    #             new_board[i - spaces][j - spaces] = sq
    #             new_board[i][j] = 0
    #             moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))
    #             spaces += 1
    #     if dir == NE:
    #         while currentState.board[i + spaces][j - spaces] == 0:
    #             new_board = [r[:] for r in currentState.board]
    #             new_board[i + spaces][j - spaces] = sq
    #             new_board[i][j] = 0
    #             moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))
    #             spaces += 1
    #     if dir == SW:
    #         while currentState.board[i - spaces][j + spaces] == 0:
    #             new_board = [r[:] for r in currentState.board]
    #             new_board[i - spaces][j + spaces] = sq
    #             new_board[i][j] = 0
    #             moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))
    #             spaces += 1
    #     if dir == SE:
    #         while currentState.board[i + spaces][j + spaces] == 0:
    #             new_board = [r[:] for r in currentState.board]
    #             new_board[i + spaces][j + spaces] = sq
    #             new_board[i][j] = 0
    #             moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))
    #             spaces += 1







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