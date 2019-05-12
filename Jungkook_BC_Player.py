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

def generate_successors(state):
    successors = []
    for row in range(8):
        for col in range(8):
            piece = state.board[i][j]
            # if who(sq) == currentState.whose_move and sq > 0:
            if who(piece) == state.whose_move and piece > 0 and not is_frozen(state, row, col):
                if piece == WHITE_PINCER or piece == BLACK_PINCER:
                    successors = successors + move_pincer(state, row, col)
                if piece == WHITE_KING or piece == BLACK_KING:
                    successors = move_king(state, row, col)
                if piece > 3 and piece != 8 and piece != 9 and piece != 12 and piece != 13:
                    successors = move_like_queen(state, row, col)


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

def is_frozen(state, row, col):
    piece = state.board[row][col]
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i != 0 and j != 0) and is_valid(row + i, col + j):
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
	'''Use the simple method for state evaluation described in the spec. This is typically
	used in parameterized_minimax calls to verify that minimax and alpha-beta pruning work
	correctly.'''

	# The value of the function is the sum of the values of the pieces on the board in the given state
	total = 0
	for row in state:
		for col in row:
			total = total + pieceVal(col)


def pieceVal(piece):
	# black pieces
    if piece == 'p':
		return -1
	elif piece == '‘k':
		return -100
	elif piece.isLowerCase():
		return -2

	# white pieces
	elif piece == ‘P’:
		return 1
	elif piece == ‘K’:
		return 100
	elif piece.isUpperCase():
		return 2

    # empty spaces
	else:
		return 0

def staticEval(state):
    '''Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.'''
    pass

def checkImmobilized(state, row, col, piece):
    if state[row][col] is 14 or 15:
        # checking if the piece is immobilized
        if who(state[row][col]) != who(piece) :
            return True
    return False

# King
# does not return captured list
# returns legal moves and new state resulting from move
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
                # checking imitator capturing king
                if king == 8 and currentState.board[row+i][col+j] == 13 or
                        king == 9 and currentState.board[row+i][col+j] == 14:
                    move = ((row, col), (row+i, col+j))
                    return [[move, newState]]                      
                # move king if empty spot next to it or the opposing teams occupying it
                if king == 13 or king == 14 or currentState.board[row+i][col+j] == 0 or \
                        who(king) != who(currentState.board[row+i][col+j])):
                    # update new position with king and remove the original
                    newState.board[row+i][col+j] = king
                    newState.board[row][col] = 0
                    move = ((row, col), (row+i, col+j))
                    possibleStates = possibleStates + [move, newState]
    return possibleStates

# Pincer
# does not return captured list
# returns legal moves and new state resulting from move
# removes captured pieces from the board
# does not include imitator

def move_pincer(currentState, row, col):
    pincer = currentState.board[row][col]
    possibleStates = []

    for i in range(-7, 8):
        for j in range(-7, 8):
            # pincer only can move vertically and horizontally like a rook in chess
            if (i != 0 and j= 0 or i = 0 and j!= 0) and 0 <= row + i < 8 and 0 <= col + j < 8:
                if checkImmobilized(currentState.board, row + i, col + j, pincer):
                    return []
                newState = BC_state(currentState.board)
                # check imitator capturing pincer
                if pincer == 8 and currentState.board[row+i][col+j] == 3 
                        or pincer == 9 and currentState.board[row+i][col+j] == 2:
                    move = ((row, col), (row+i, col+j))
                    return [[move, pincer_capture(newState, row+i, col+j)]] 
                if currentState.board[row+i][col+j] == 0:
                    # update new position with pincer and remove the original
                    newState.board[row+i][col+j] = pincer
                    newState.board[row][col] = 0
                    # store the move made
                    move = ((row, col), (row+i, col+j))
                    # remove the captured pieces on the board with pincer at new location
                    newState = pincer_capture(newState, row+i, col+j)
                    # add [move, new state] to possible states for that piece
                    possibleStates = possibleStates + [move, newState]
    # return all possible states for the board
    return possibleStates

def pincer_capture(newState, row, col):
    updatedBoard = BC_state(newState.board)
    for i in range (-1, 2):
        for j in range (-1, 2):
            # only can capture vertically and horizontally
            if i != 0 and j = 0 or i = 0 and j!= 0:
                if 0 <= row + 2*i < 8 and 0 <= col + 2*j < 8:
                    if updatedBoard.board[row+i][col+j] != 0 and 
                            who(updatedBoard.board[row+2*i][col+2*j]) == 
                                    who(updatedBoard.board[row][col]):
                        # captured
                        updatedBoard.board[row+i][col+j] = 0
    # return same board if no captures
    # or new board with all the captured pieces removed 
    return updatedBoard