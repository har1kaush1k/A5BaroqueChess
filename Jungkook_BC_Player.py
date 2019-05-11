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
    newState = BC_state(board)
    successors = []
    captures = []

    checking = True
    move = 1

    while checking:
        kill = False
        temp = BC_state(state.board)
        if not is_valid(row + move, col) or newState.board[row + move][col] != 0:
            break
        temp.board[row + move][col] = temp.board[row][col]
        temp.board[row][col] = 0
        if piece is 4 or piece is 5:
            


    pass


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

# def piece_noncapture_moves(i, j, currentState):
#     moves = []
#     sq = currentState.board[i][j]
#     if sq // 2 == 1:
#         directions = [NORTH, WEST, EAST, SOUTH]
#     else:
#         directions = [NORTH, SOUTH, WEST, EAST, NW, NE, SW, SE]
#     if sq // 2 == 1:
#         distance = 7
#         while distance > 0:
#
#         # for y in range(8):
#         #     empty = True
#         #     delta = 1
#         #     curr = j
#         #     if j > y: delta = -1
#         #     while curr != y and empty:
#         #         if currentState.board[i][curr] != 0:
#         #             empty = False
#         #         curr += delta
#         #     if currentState.board[i][y] != 0 and empty:
#         #         new_board = [r[:] for r in currentState.board]
#         #         new_board[i][y] = sq
#         #         new_board[i][j] = 0
#         #         moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))
#         # for x in range(8):
#         #     empty = True
#         #     delta = 1
#         #     curr = j
#         #     if j > x: delta = -1
#         #     while curr != x and empty:
#         #         if currentState.board[curr][j] != 0:
#         #             empty = False
#         #         curr += delta
#         #     if currentState.board[x][j] != 0 and empty:
#         #         new_board = [r[:] for r in currentState.board]
#         #         new_board[x][j] = sq
#         #         new_board[i][j] = 0
#         #         moves.append(BC_state(old_board=new_board, whose_move=1 - currentState.whose_move))

    # if sq // 2 == 1:
    #     directions = [NORTH, SOUTH, WEST, EAST]
    # else:
    #     directions = [NORTH, SOUTH, WEST, EAST, NW, NE, SW, SE]
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





# [[move, state], [mov]]

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