'''Pablo_BC_state_etc.py
Varun Venkatesh and Nikhil Singh

This file contains the AI playing agent for Baroque Chess.

'''
import random, sys
Side = None
K = 4
isMax = True
USE_CUSTOM_STATIC_EVAL_FUNCTION = True
iterative = True
use_time = True
prune = True
maxOverallDepth = 0
timeLim = 1.0
cutoffs = 0
expanded = 0
oppMon = None
turn = 1
res_count = 0

z_values = [[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] for i in range(8)]\
              for j in range(8)]
dict_z_val = {}

responses = ["Welcome to the matrix, you aren't going to know what hit you",
             "I will defeat your best moves, there is nothing you can do",
             "I have been practicing for a long time, nothing will suprise me",
             "Why don't you practice some more after I defeat you",
             "I have experience that will help me defeat you",
             "That move is how we do it in the big leagues",
             "BAM, welcome to the Pablo show",
             "Is that all you got, I will destroy you",
             "Nice try, but I know what you are thinking",
             "You can always give up if you need to",
             "That was a terrible mistake, get ready for some thunder"]

import BC_state_etc as BC
import time, sys

piece_vals = {0: 0.0, 2: -12.0, 3: 12.0, 4: -75.0, 5: 75.0, 6: -100.0, 7: 100.0, 8: -100.0, 9: 100.0, 10: -35.0, 11: 35.0,
              12: -2000.0, 13: 2000.0, 14: -75.0, 15: 75.0}
edge_vals = [[8, 7, 7, 7, 7, 7, 7, 8],
             [7, 4, 4, 4, 4, 4, 4, 7],
             [7, 4, 3, 3, 3, 3, 4, 7],
             [7, 4, 3, 2, 2, 3, 4, 7],
             [7, 4, 3, 2, 2, 3, 4, 7],
             [7, 4, 3, 3, 3, 3, 4, 7],
             [7, 4, 4, 4, 4, 4, 4, 7],
             [8, 7, 7, 7, 7, 7, 7, 8]]

midd_vals = [[2, 2, 2, 2, 2, 2, 2, 2],
             [3, 3, 3, 3, 3, 3, 3, 3],
             [4, 4, 4, 4, 4, 4, 4, 4],
             [5, 5, 5, 5, 5, 5, 5, 5],
             [5, 5, 5, 5, 5, 5, 5, 5],
             [4, 4, 4, 4, 4, 4, 4, 4],
             [3, 3, 3, 3, 3, 3, 3, 3],
             [2, 2, 2, 2, 2, 2, 2, 2]]


#  Initialize the values for the Zobrist Hash Table
def init_values():
    global z_values

    for row in range(8):
        for col in range(8):
            for piece in range(16):
                z_values[row][col][piece] = random.randint(0,sys.maxsize)


#  Creates the Hash Function for the Zobrist Hash Table
def hash_function(state):
    global z_values, dict_z_val
    b = state.board

    hash_value = 0

    for row in range(8):
        for col in range(8):
            piece = b[row][col]
            if piece is not 0:
                temp = z_values[row][col][piece]
                hash_value ^= temp

    return hash_value


#  Takes in input state and returns  the best possible next state, the move that was made and a remark
def makeMove(current_state, currentRemark, time_limit=10):
    new_state = BC.BC_state(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_move
    new_who = 0
    if who == 0: new_who = 1
    new_state.whose_turn = new_who
    global prune, use_time, responses, res_count
    prune = True
    use_time = True
    startTime = time.perf_counter()
    state = None
    for i in range(1, 4):
        if time.perf_counter() - startTime < time_limit - float(.1):
            curr_state = miniHelper(current_state, isMax, -sys.maxsize, sys.maxsize, 0, i, startTime, time_limit)
            if curr_state[0] is not None:
                state = curr_state
    move = findDifference(current_state, state[0])
    utter = responses[res_count % 11]
    res_count += 1

    return [[move, state[0]], utter]


#  Finds the difference between two states. Returns the old position and the new position
def findDifference(currentState, newState):
    b1 = currentState.board
    b2 = newState.board
    turn = currentState.whose_move
    start = []
    end = []
    for row in range(8):
        for col in range(8):
            if b1[row][col] != b2[row][col]:
                if b1[row][col] != 0 and turn == b1[row][col] % 2:
                    start.append(row)
                    start.append(col)
                if b2[row][col] != 0 and turn == b2[row][col] % 2:
                    end.append(row)
                    end.append(col)
    return [start, end]


#  Returns the nickname for the player
def nickname():
    return "Pablo"


#  Returns a string with a player introduction
def introduce():
    return "Hi, My name is Pablo and I am student training to become the best Baroque Chess player in the entire world"


def prepare(playerNickName):
    oppMon = playerNickName
    init_values()


# Does all of the minimax functionality, has ways to turn on and off certain features
# Returns the best move based on the inputs given and the search itself as well as the eval value
# of the best state it hopes to reach
def miniHelper(state, maxPl, alpha, beta, depth, maxDepth, startTime, timeLimit):
    global cutoffs, maxOverallDepth, prune, expanded, use_time
    if depth > maxOverallDepth:
        maxOverallDepth = depth
    state.__class__ = BC.BC_state
    timeNew = time.perf_counter() - startTime > timeLimit - float(.1)
    #if time.perf_counter() - startTime > timeLimit - float(.2) and use_time:
    staticEval = 0
    z = hash_function(state)
    if z in dict_z_val.keys():
        staticEval = dict_z_val[z]
    else:
        staticEval = static_eval(state)
        dict_z_val[z] = staticEval

    if timeNew and use_time:
        return [state, staticEval]
    successors = getSuccessors(state)
    if depth >= maxDepth:
        return [state, staticEval]
    if len(successors) == 0:
        return [state, staticEval]

    if maxPl == True:
        best = -sys.maxsize
        bestState = None
        for tempState in successors:
            expanded = expanded + 1
            if time.perf_counter() - startTime > timeLimit - float(.1) and use_time:
                if depth == 0:
                    return [bestState, best]
                return [state, best]
            evalValue = miniHelper(tempState, False, alpha, beta, depth + 1, maxDepth, startTime, timeLimit)
            if depth == 0:
                if evalValue[1] > best:
                    bestState = tempState
            best = max(best, evalValue[1])
            alpha = max(alpha, best)
            if prune:
                if beta <= alpha:
                    break
        if depth == 0:
            return [bestState, best]
        return [state, best]
    else:
        best = sys.maxsize
        bestState = None
        for tempState in successors:
            expanded = expanded + 1
            if time.perf_counter() - startTime > timeLimit - float(.1) and use_time:
                if depth == 0:
                    return [bestState, best]
                return [state, best]
            evalValue = miniHelper(tempState, True, alpha, beta, depth + 1, maxDepth, startTime, timeLimit)
            if depth == 0:
                if evalValue[1] < best:
                    bestState = tempState
            best = min(best, evalValue[1])
            beta = min(beta, best)
            if prune:
                if beta <= alpha:
                    break
        if depth == 0:
            return [bestState, best]
        return [state, best]


#  Static eval - takes in a state and returns a score based on the state. Higher Scores are better for White player and
#  lower scores are better for black
def static_eval(state):
    global piece_vals, edge_vals, midd_vals
    b = state.board
    score = 0.0
    # white_row, white_col, black_row, black_col
    location = find_Kings(state)
    for row in range(8):
        for col in range(8):
            piece = b[row][col]
            score += piece_vals.get(piece)

            if piece is 12 or piece is 13 or piece is 8 or piece is 9:  # King
                if piece is 12:
                    score -= (2 * edge_vals[row][col])
                elif piece is 13:
                    score += (2 * edge_vals[row][col])
                elif piece is 8:
                    score -= (0.5 * edge_vals[row][col])
                else:
                    score += (0.5 * edge_vals[row][col])

            # PUT LEAPER IN HERE IF NEEDED
            elif piece is 4 or piece is 5 or piece is 8 or piece is 9: # Coordinator
                if (piece is 4 or piece is 8) and row is not location[0] and col is not location[1]:
                    score -= 5

                elif (piece is 5 or piece is 9) and row is not location[2] and col is not location[3]:
                    score += 5

            elif piece is 14 or piece is 15 or piece is 8 or piece is 9: #Freezer
                if piece is 14 or piece is 8:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            temp_row = row + i
                            temp_col = col + j
                            if 0 <= temp_row < 8 and 0 <= temp_col < 8:
                                temp_piece = b[temp_row][temp_col]
                                if temp_piece % 2 is 1:
                                    score += (piece_vals.get(b[temp_row][temp_col]) / 100)
                    score -= (5 * midd_vals[row][col])
                else:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            temp_row = row + i
                            temp_col = col + j
                            if 0 <= temp_row < 8 and 0 <= temp_col < 8:
                                temp_piece = b[temp_row][temp_col]
                                if temp_piece % 2 is 0:
                                    score -= (piece_vals.get(b[temp_row][temp_col]) / 100)
                    score += (5 * midd_vals[row][col])
            elif piece is 10 or piece is 11 or piece is 8 or piece is 9: # withdraw
                extreme = 0
                if piece is 10 or piece is 8:
                    for i in range(-1,2):
                        for j in range(-1,2):
                            temp_row = row + i
                            temp_col = col + j
                            if 0 <= temp_row < 8 and 0 <= temp_col < 8:
                                temp_piece = b[temp_row][temp_col]
                                if temp_piece % 2 is 1 and piece_vals.get(b[temp_row][temp_col]) < extreme \
                                        and 0 <= row - i < 8 and 0 <= col - j < 8:
                                    extreme = piece_vals.get(b[temp_row][temp_col])
                    score += extreme / 25
                else:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            temp_row = row + i
                            temp_col = col + j
                            if 0 <= temp_row < 8 and 0 <= temp_col < 8:
                                temp_piece = b[temp_row][temp_col]
                                if temp_piece % 2 is 0 and piece_vals.get(b[temp_row][temp_col]) > extreme \
                                        and 0 <= row - i < 8 and 0 <= col - j < 8:
                                    extreme = piece_vals.get(b[temp_row][temp_col])
                    score -= extreme / 25
            elif piece is 2 or piece is 3 or piece is 8 or piece is 9: # pincher
                for i in range(-2, 3, 4):
                    if 0 <= row + i < 8:
                        row_temp = b[row + i][col]
                        if row_temp is piece:
                            score += piece_vals.get(row_temp) / 4
                    if 0 <= col + i < 8:
                        col_temp = b[row][col + i]
                        if col_temp is piece:
                            score += piece_vals.get(col_temp) / 4
                if piece is 2 or piece is 8:
                    score -= (8 - (abs(row - location[0]) + abs(col - location[1])))
                if piece is 3 or piece is 9:
                    score += (8 - (abs(row - location[2]) + abs(col - location[3])))


    return score


#  Returns the positions of the two kings
def find_Kings(state):
    global piece_vals
    b = state.board
    location = [-1, -1, -1, -1]
    for row in range(8):
        for col in range(8):
            piece = b[row][col]
            if piece is 13:
                location[0] = row
                location[1] = col
            elif piece is 12:
                location[2] = row
                location[3] = col
            if location[0] is not -1 and location[2] is not -1:
                return location

    return location


#  Returns a list of successors based on an input state. In the list, potential states that capture are placed before states that dont.
def getSuccessors(state):
    global turn
    success = []
    b = state.board
    if state.whose_move == 0:
        turn = 1
    else:
        turn = 0
    for row in range(8):
        for col in range(8):
            piece = b[row][col]
            freeze = False
            imitate = False
            if piece % 2 == state.whose_move and piece != 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (i != 0 and j != 0) and isValidPosition(row + i, col + j):
                            if b[row + i][col + j] is 15 or b[row + i][col + j] is 14:
                                if b[row + i][col + j] % 2 != piece % 2:
                                    freeze = True
                            if b[row + i][col + j] is 8 or b[row + i][col + j] is 9:
                                if b[row + i][col + j] % 2 != piece % 2:
                                    imitate = True
                if not freeze or not imitate:
                    if piece is 2 or piece is 3:
                        capture, states = move_Pinch(state, row, col)
                        success = capture + success + states
                    elif piece is 12 or piece is 13:
                        capture, states = move_King(state, row, col)
                        success = capture + success + states
                    elif piece is 8 or piece is 9:
                        capture, states = move_Pinch(state, row, col)
                        success = capture + success + states
                        capture, states = move_King(state, row, col)
                        success = capture + success + states
                        capture, states = move_Queen(state, row, col)
                        success = capture + success + states
                    elif (piece is 14 or piece is 15) and not imitate:
                        capture, states = move_Queen(state, row, col)
                        success = capture + success + states
                    else:
                        capture, states = move_Queen(state, row, col)
                        success = capture + success + states
    for successor in success:
        successor.whose_move = turn
    return success


#  Creates potential states for the pieces that move similar to an orthodox queen
def move_Queen(state, row, col):
    piece = state.board[row][col]
    side = piece % 2
    newState = BC.BC_state(state.board)
    states = []
    capture = []
    kings = find_Kings(state)
    kingRow = kings[0]
    kingCol = kings[1]
    if side is 0:
        kingRow = kings[2]
        kingCol = kings[3]


    if 6 <= piece <= 9:
        for i in range(-1,2):
            for j in range(-1,2):
                if isValidPosition(row + i, col + j) and not(i is 0 and j is 0):
                    tempState = BC.BC_state(state.board)
                    if (tempState.board[row+i][col+j] % 2 != tempState.board[row][col] % 2) and isValidPosition(row+i+i, col+j+j) and tempState.board[row+i+i][col+j+j] is 0:
                        if tempState.board[row+i][col+j] != 0:
                            tempState.board[row+i][col+j] = 0
                            tempState.board[row+i+i][col+j+j] = tempState.board[row][col]
                            tempState.board[row][col] = 0
                            capture.append(BC.BC_state(tempState.board, tempState.whose_move))
    cont = True
    move = 1
    while cont:
        kill = False
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row + move, col) or newState.board[row + move][col] != 0:
            break
        tempState.board[row + move][col] = tempState.board[row][col]
        tempState.board[row][col] = 0
        if piece is 4 or piece is 5 or piece is 8 or piece is 9:  # Coordinator
            hold1 = -1
            hold2 = -1
            if (tempState.board[kingRow][col] % 2 != tempState.board[row+move][col] % 2)\
                    and tempState.board[kingRow][col] != 0 and\
                    ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[kingRow][col] is 4 or tempState.board[kingRow][col] is 5))):
                hold1 = tempState.board[kingRow][col]
                tempState.board[kingRow][col] = 0
                kill = True

            if (tempState.board[row+move][kingCol] % 2 != tempState.board[row+move][col] % 2) \
                    and tempState.board[row+move][kingCol] != 0 and \
                    ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[row + move][kingCol] is 4 or tempState.board[row+move][kingCol] is 5))):
                hold2 = tempState.board[row + move][kingCol]
                tempState.board[row + move][kingCol] = 0
                kill = True

            if kill:
                capture.append(BC.BC_state(tempState.board, tempState.whose_move))
                if hold1 != -1:
                    tempState.board[kingRow][col] = hold1
                if hold2 != -1:
                    tempState.board[row + move][kingCol] = hold2

        if piece is 10 or piece is 11 or piece is 8 or piece is 9:  # Withdraw
            if isValidPosition(row-1, col) and (tempState.board[row-1][col] % 2 != tempState.board[row+move][col] % 2)\
                    and tempState.board[row-1][col] != 0 and ((piece is 10 or piece is 11) or ((piece is 8 or piece is 9) and (tempState.board[row-1][col] is 10 or tempState.board[row-1][col] is 11))):
                kill = True
                hold = tempState.board[row - 1][col]
                tempState.board[row - 1][col] = 0
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                tempState.board[row - 1][col] = hold

        if piece is 6 or piece is 7 or piece is 8 or piece is 9:  # Leaper
            if isValidPosition(row + move + 1, col) and (tempState.board[row + move + 1][col] % 2 != tempState.board[row + move][col] % 2) and tempState.board[row + move + 1][col] != 0:
                if isValidPosition(row + move + 2, col) and tempState.board[row + move + 2][col] == 0:
                    if (piece is 6 or piece is 7) or ((piece is 8 or piece is 9) and (tempState.board[row + move + 1][col] is 6 or tempState.board[row + move + 1][col] is 7)):
                        capture_hold = tempState.board[row + move + 1][col]
                        curr_hold = tempState.board[row + move][col]
                        tempState.board[row + move + 2][col] = tempState.board[row + move][col]
                        tempState.board[row + move + 1][col] = 0
                        tempState.board[row + move][col] = 0
                        capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                        kill = True
                        tempState.board[row + move + 2][col] = 0
                        tempState.board[row + move + 1][col] = capture_hold
                        tempState.board[row + move][col] = curr_hold

        if not kill:
            states.append(tempState)
        move += 1
    move = 1
    while cont:
        kill = False
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row - move, col) or newState.board[row - move][col] != 0:
            break
        tempState.board[row - move][col] = tempState.board[row][col]
        tempState.board[row][col] = 0
        if piece is 4 or piece is 5 or piece is 8 or piece is 9:
            hold1 = -1
            hold2 = -1
            if (tempState.board[kingRow][col] % 2 != tempState.board[row-move][col] % 2) and \
                    tempState.board[kingRow][col] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[kingRow][col] is 4 or tempState.board[kingRow][col] is 5))):
                hold1 = tempState.board[kingRow][col]
                tempState.board[kingRow][col] = 0
                kill = True

            if (tempState.board[row-move][kingCol] % 2 != tempState.board[row-move][col] % 2)\
                    and tempState.board[row-move][kingCol] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[row - move][kingCol] is 4 or tempState.board[row-move][kingCol] is 5))):
                hold2 = tempState.board[row - move][kingCol]
                tempState.board[row - move][kingCol] = 0
                kill = True

            if kill:
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                if hold1 != -1:
                    tempState.board[kingRow][col] = hold1
                if hold2 != -1:
                    tempState.board[row - move][kingCol] = hold2

        if piece is 10 or piece is 11 or piece is 8 or piece is 9:
            if isValidPosition(row+1, col) and (tempState.board[row+1][col] % 2 != tempState.board[row-move][col] % 2)\
                    and tempState.board[row+1][col] != 0  and ((piece is 10 or piece is 11) or ((piece is 8 or piece is 9) and (tempState.board[row+1][col] is 10 or tempState.board[row+1][col] is 11))):
                kill = True
                hold = tempState.board[row + 1][col]
                tempState.board[row + 1][col] = 0
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                tempState.board[row + 1][col] = hold

        if piece is 6 or piece is 7 or piece is 8 or piece is 9:
            if isValidPosition(row - move - 1, col) and\
                    (tempState.board[row - move - 1][col] % 2 != tempState.board[row-move][col] % 2)\
                    and tempState.board[row - move - 1][col] != 0:
                if isValidPosition(row - move - 2, col) and tempState.board[row - move - 2][col] == 0:
                    if (piece is 6 or piece is 7) or ((piece is 8 or piece is 9) and (
                            tempState.board[row - move - 1][col] is 6 or tempState.board[row - move - 1][col] is 7)):
                        capture_hold = tempState.board[row - move - 1][col]
                        curr_hold = tempState.board[row - move][col]
                        tempState.board[row - move - 2][col] = tempState.board[row - move][col]
                        tempState.board[row - move - 1][col] = 0
                        tempState.board[row - move][col] = 0
                        capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                        kill = True
                        tempState.board[row - move - 2][col] = 0
                        tempState.board[row - move - 1][col] = capture_hold
                        tempState.board[row - move][col] = curr_hold

        if not kill:
            states.append(tempState)
        move += 1
    move = 1
    while cont:
        kill = False
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row, col + move) or newState.board[row][col + move] != 0:
            break
        tempState.board[row][col + move] = tempState.board[row][col]
        tempState.board[row][col] = 0
        if piece is 4 or piece is 5 or piece is 8 or piece is 9:
            hold1 = -1
            hold2 = -1
            if (tempState.board[kingRow][col] % 2 != tempState.board[row][col + move] % 2) and \
                    tempState.board[kingRow][col + move] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[kingRow][col + move] is 4 or tempState.board[kingRow][col + move] is 5))):
                hold1 = tempState.board[kingRow][col + move]
                tempState.board[kingRow][col + move] = 0
                kill = True

            if (tempState.board[row][kingCol] % 2 != tempState.board[row][col + move] % 2)\
                    and tempState.board[row][kingCol] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[row][kingCol] is 4 or tempState.board[row][kingCol] is 5))):
                hold2 = tempState.board[row][kingCol]
                tempState.board[row][kingCol] = 0
                kill = True

            if kill:
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                if hold1 != -1:
                    tempState.board[kingRow][col + move] = hold1
                if hold2 != -1:
                    tempState.board[row][kingCol] = hold2

        if piece is 10 or piece is 11 or piece is 8 or piece is 9:
            if isValidPosition(row, col - 1) and (tempState.board[row][col - 1] % 2 != tempState.board[row][col + move] % 2)\
                    and tempState.board[row][col-1] != 0 and ((piece is 10 or piece is 11) or ((piece is 8 or piece is 9) and (tempState.board[row][col-1] is 10 or tempState.board[row][col-1] is 11))):
                kill = True
                hold = tempState.board[row][col-1]
                tempState.board[row][col-1] = 0
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                tempState.board[row][col-1] = hold

        if piece is 6 or piece is 7 or piece is 8 or piece is 9:
            if isValidPosition(row, col + move + 1) and\
                    (tempState.board[row][col + move + 1] % 2 != tempState.board[row][col + move] % 2)\
                    and tempState.board[row][col + move + 1] != 0:
                if isValidPosition(row, col + move + 2) and tempState.board[row][col + move + 2] == 0:
                    if (piece is 6 or piece is 7) or ((piece is 8 or piece is 9) and (
                            tempState.board[row][col + move + 1] is 6 or tempState.board[row][col + move + 1] is 7)):
                        capture_hold = tempState.board[row][col + move + 1]
                        curr_hold = tempState.board[row][col + move]
                        tempState.board[row][col + move + 2] = tempState.board[row][col + move]
                        tempState.board[row][col + move + 1] = 0
                        tempState.board[row][col + move] = 0
                        capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                        kill = True
                        tempState.board[row][col + move + 2] = 0
                        tempState.board[row][col + move + 1] = capture_hold
                        tempState.board[row][col + move] = curr_hold

        if not kill:
            states.append(tempState)
        move += 1
    move = 1
    while cont:
        kill = False
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row, col - move) or newState.board[row][col - move] != 0:
            break
        tempState.board[row][col - move] = tempState.board[row][col]
        tempState.board[row][col] = 0
        if piece is 4 or piece is 5 or piece is 8 or piece is 9:
            hold1 = -1
            hold2 = -1
            if (tempState.board[kingRow][col-move] % 2 != tempState.board[row][col - move] % 2) and \
                    tempState.board[kingRow][col - move] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[kingRow][col - move] is 4 or tempState.board[kingRow][col-move] is 5))):
                hold1 = tempState.board[kingRow][col - move]
                tempState.board[kingRow][col - move] = 0
                kill = True

            if (tempState.board[row][kingCol] % 2 != tempState.board[row][col - move] % 2)\
                    and tempState.board[row][kingCol] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[row][kingCol] is 4 or tempState.board[row][kingCol] is 5))):
                hold2 = tempState.board[row][kingCol]
                tempState.board[row][kingCol] = 0
                kill = True

            if kill:
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                if hold1 != -1:
                    tempState.board[kingRow][col - move] = hold1
                if hold2 != -1:
                    tempState.board[row][kingCol] = hold2

        if piece is 10 or piece is 11 or piece is 8 or piece is 9:
            if isValidPosition(row, col + 1) and (tempState.board[row][col + 1] % 2 != tempState.board[row][col-move] % 2)\
                    and tempState.board[row][col+1] != 0 and ((piece is 10 or piece is 11) or ((piece is 8 or piece is 9) and (tempState.board[row][col+1] is 10 or tempState.board[row][col+1] is 11))):
                kill = True
                hold = tempState.board[row][col+1]
                tempState.board[row][col+1] = 0
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                tempState.board[row][col+1] = hold

        if piece is 6 or piece is 7 or piece is 8 or piece is 9:
            if isValidPosition(row, col - move - 1) and\
                    (tempState.board[row][col - move - 1] % 2 != tempState.board[row][col - move] % 2)\
                    and tempState.board[row][col - move - 1] != 0:
                if isValidPosition(row, col - move - 2) and tempState.board[row][col - move - 2] == 0:
                    if (piece is 6 or piece is 7) or ((piece is 8 or piece is 9) and (
                            tempState.board[row][col - move - 1] is 6 or tempState.board[row][col - move - 1] is 7)):
                        capture_hold = tempState.board[row][col - move - 1]
                        curr_hold = tempState.board[row][col - move]
                        tempState.board[row][col - move - 2] = tempState.board[row][col - move]
                        tempState.board[row][col - move - 1] = 0
                        tempState.board[row][col - move] = 0
                        capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                        kill = True
                        tempState.board[row][col - move - 2] = 0
                        tempState.board[row][col - move - 1] = capture_hold
                        tempState.board[row][col - move] = curr_hold

        if not kill:
            states.append(tempState)
        move += 1
    move = 1
    while cont:
        kill = False
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row + move, col + move) or newState.board[row + move][col + move] != 0:
            break
        tempState.board[row + move][col + move] = tempState.board[row][col]
        tempState.board[row][col] = 0
        if piece is 4 or piece is 5 or piece is 8 or piece is 9:
            hold1 = -1
            hold2 = -1
            if (tempState.board[kingRow][col + move] % 2 != tempState.board[row + move][col + move] % 2) and \
                    tempState.board[kingRow][col + move] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[kingRow][col + move] is 4 or tempState.board[kingRow][col + move] is 5))):
                hold1 = tempState.board[kingRow][col + move]
                tempState.board[kingRow][col + move] = 0
                kill = True

            if (tempState.board[row + move][kingCol] % 2 != tempState.board[row + move][col + move] % 2)\
                    and tempState.board[row + move][kingCol] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[row + move][kingCol] is 4 or tempState.board[row+move][kingCol] is 5))):
                hold2 = tempState.board[row + move][kingCol]
                tempState.board[row + move][kingCol] = 0
                kill = True

            if kill:
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                if hold1 != -1:
                    tempState.board[kingRow][col + move] = hold1
                if hold2 != -1:
                    tempState.board[row + move][kingCol] = hold2

        if piece is 10 or piece is 11 or piece is 8 or piece is 9:
            if isValidPosition(row - 1, col - 1) and (tempState.board[row - 1][col - 1] % 2 != tempState.board[row+move][col+move] % 2)\
                    and tempState.board[row-1][col-1] != 0 and ((piece is 10 or piece is 11) or ((piece is 8 or piece is 9) and (tempState.board[row-1][col-1] is 10 or tempState.board[row-1][col-1] is 11))):
                kill = True
                hold = tempState.board[row-1][col-1]
                tempState.board[row-1][col-1] = 0
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                tempState.board[row-1][col-1] = hold

        if piece is 6 or piece is 7 or piece is 8 or piece is 9:
            if isValidPosition(row + move + 1, col + move + 1) and\
                    (tempState.board[row + move + 1][col + move + 1] % 2 != tempState.board[row + move][col + move] % 2)\
                    and tempState.board[row + move + 1][col + move + 1] != 0:
                if isValidPosition(row + move + 2, col + move + 2) and tempState.board[row + move + 2][col + move + 2] == 0:
                    if (piece is 6 or piece is 7) or ((piece is 8 or piece is 9) and (
                            tempState.board[row + move + 1][col + move + 1] is 6 or tempState.board[row + move + 1][col + move + 1] is 7)):
                        capture_hold = tempState.board[row + move + 1][col + move + 1]
                        curr_hold = tempState.board[row + move][col + move]
                        tempState.board[row + move + 2][col + move + 2] = tempState.board[row + move][col + move]
                        tempState.board[row + move + 1][col + move + 1] = 0
                        tempState.board[row + move][col + move] = 0
                        capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                        kill = True
                        tempState.board[row + move + 2][col + move + 2] = 0
                        tempState.board[row + move + 1][col + move + 1] = capture_hold
                        tempState.board[row + move][col + move] = curr_hold

        if not kill:
            states.append(tempState)
        move += 1
    move = 1
    while cont:
        kill = False
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row + move, col - move) or newState.board[row + move][col - move] != 0:
            break
        tempState.board[row + move][col - move] = tempState.board[row][col]
        tempState.board[row][col] = 0
        if piece is 4 or piece is 5 or piece is 8 or piece is 9:
            hold1 = -1
            hold2 = -1
            if (tempState.board[kingRow][col - move] % 2 != tempState.board[row + move][col - move] % 2) and \
                    tempState.board[kingRow][col - move] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[kingRow][col - move] is 4 or tempState.board[kingRow][col-move] is 5))):
                hold1 = tempState.board[kingRow][col - move]
                tempState.board[kingRow][col - move] = 0
                kill = True

            if (tempState.board[row + move][kingCol] % 2 != tempState.board[row + move][col - move] % 2)\
                    and tempState.board[row + move][kingCol] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[row + move][kingCol] is 4 or tempState.board[row+move][kingCol] is 5))):
                hold2 = tempState.board[row + move][kingCol]
                tempState.board[row + move][kingCol] = 0
                kill = True

            if kill:
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                if hold1 != -1:
                    tempState.board[kingRow][col - move] = hold1
                if hold2 != -1:
                    tempState.board[row + move][kingCol] = hold2

        if piece is 10 or piece is 11 or piece is 8 or piece is 9:
            if isValidPosition(row - 1, col + 1) and (tempState.board[row - 1][col + 1] % 2 != tempState.board[row+move][col-move] % 2)\
                    and tempState.board[row-1][col+1] != 0 and ((piece is 10 or piece is 11) or ((piece is 8 or piece is 9) and (tempState.board[row-1][col+1] is 10 or tempState.board[row-1][col+1] is 11))):
                kill = True
                hold = tempState.board[row-1][col+1]
                tempState.board[row-1][col+1] = 0
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                tempState.board[row-1][col+1] = hold

        if piece is 6 or piece is 7 or piece is 8 or piece is 9:
            if isValidPosition(row + move + 1, col - move - 1) and\
                    (tempState.board[row + move + 1][col - move - 1] % 2 != tempState.board[row + move][col - move] % 2)\
                    and tempState.board[row + move + 1][col - move - 1] != 0:
                if isValidPosition(row + move + 2, col - move - 2) and tempState.board[row + move + 2][col - move - 2] == 0:
                    if (piece is 6 or piece is 7) or ((piece is 8 or piece is 9) and (
                            tempState.board[row + move + 1][col - move - 1] is 6 or tempState.board[row + move + 1][col - move - 1] is 7)):
                        capture_hold = tempState.board[row + move + 1][col - move - 1]
                        curr_hold = tempState.board[row + move][col - move]
                        tempState.board[row + move + 2][col - move - 2] = tempState.board[row + move][col - move]
                        tempState.board[row + move + 1][col - move - 1] = 0
                        tempState.board[row + move][col - move] = 0
                        capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                        kill = True
                        tempState.board[row + move + 2][col - move - 2] = 0
                        tempState.board[row + move + 1][col - move - 1] = capture_hold
                        tempState.board[row + move][col - move] = curr_hold

        if not kill:
            states.append(tempState)
        move += 1
    move = 1
    while cont:
        kill = False
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row - move, col + move) or newState.board[row - move][col + move] != 0:
            break
        tempState.board[row - move][col + move] = tempState.board[row][col]
        tempState.board[row][col] = 0
        if piece is 4 or piece is 5 or piece is 8 or piece is 9:
            hold1 = -1
            hold2 = -1
            if (tempState.board[kingRow][col + move] % 2 != tempState.board[row - move][col + move] % 2) and \
                    tempState.board[kingRow][col + move] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[kingRow][col + move] is 4 or tempState.board[kingRow][col + move] is 5))):
                hold1 = tempState.board[kingRow][col + move]
                tempState.board[kingRow][col + move] = 0
                kill = True

            if (tempState.board[row - move][kingCol] % 2 != tempState.board[row - move][col + move] % 2) \
                    and tempState.board[row - move][kingCol] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[row - move][kingCol] is 4 or tempState.board[row-move][kingCol] is 5))):
                hold2 = tempState.board[row - move][kingCol]
                tempState.board[row - move][kingCol] = 0
                kill = True

            if kill:
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                if hold1 != -1:
                    tempState.board[kingRow][col + move] = hold1
                if hold2 != -1:
                    tempState.board[row - move][kingCol] = hold2

        if piece is 10 or piece is 11 or piece is 8 or piece is 9:
            if isValidPosition(row + 1, col - 1) and (tempState.board[row + 1][col - 1] % 2 != tempState.board[row-move][col+move] % 2)\
                    and tempState.board[row+1][col-1] != 0 and ((piece is 10 or piece is 11) or ((piece is 8 or piece is 9) and (tempState.board[row+1][col-1] is 10 or tempState.board[row+1][col-1] is 11))):
                kill = True
                hold = tempState.board[row+1][col-1]
                tempState.board[row+1][col-1] = 0
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                tempState.board[row+1][col-1] = hold

        if piece is 6 or piece is 7 or piece is 8 or piece is 9:
            if isValidPosition(row - move - 1, col + move + 1) and\
                    (tempState.board[row - move - 1][col + move + 1] % 2 != tempState.board[row - move][col + move] % 2)\
                    and tempState.board[row - move - 1][col + move + 1] != 0:
                if isValidPosition(row - move - 2, col + move + 2) and tempState.board[row - move - 2][col + move + 2] == 0:
                    if (piece is 6 or piece is 7) or ((piece is 8 or piece is 9) and (
                            tempState.board[row - move - 1][col + move + 1] is 6 or tempState.board[row - move - 1][col + move + 1] is 7)):
                        capture_hold = tempState.board[row - move - 1][col + move + 1]
                        curr_hold = tempState.board[row - move][col + move]
                        tempState.board[row - move - 2][col + move + 2] = tempState.board[row - move][col + move]
                        tempState.board[row - move - 1][col + move + 1] = 0
                        tempState.board[row - move][col + move] = 0
                        capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                        kill = True
                        tempState.board[row - move - 2][col + move + 2] = 0
                        tempState.board[row - move - 1][col + move + 1] = capture_hold
                        tempState.board[row - move][col + move] = curr_hold

        if not kill:
            states.append(tempState)
        move += 1
    move = 1
    while cont:
        kill = False
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row - move, col - move) or newState.board[row - move][col - move] != 0:
            break
        tempState.board[row - move][col - move] = tempState.board[row][col]
        tempState.board[row][col] = 0
        if piece is 4 or piece is 5 or piece is 8 or piece is 9:
            hold1 = -1
            hold2 = -1
            if (tempState.board[kingRow][col - move] % 2 != tempState.board[row - move][col - move] % 2) and \
                    tempState.board[kingRow][col - move] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[kingRow][col - move] is 4 or tempState.board[kingRow][col - move] is 5))):
                hold1 = tempState.board[kingRow][col - move]
                tempState.board[kingRow][col - move] = 0
                kill = True

            if (tempState.board[row - move][kingCol] % 2 != tempState.board[row - move][col - move] % 2)\
                    and tempState.board[row - move][kingCol] != 0 and ((piece is 4 or piece is 5) or ((piece is 8 or piece is 9) and (tempState.board[row - move][kingCol] is 4 or tempState.board[row-move][kingCol] is 5))):
                hold2 = tempState.board[row - move][kingCol]
                tempState.board[row - move][kingCol] = 0
                kill = True

            if kill:
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                if hold1 != -1:
                    tempState.board[kingRow][col - move] = hold1
                if hold2 != -1:
                    tempState.board[row - move][kingCol] = hold2

        if piece is 10 or piece is 11 or piece is 8 or piece is 9:
            if isValidPosition(row + 1, col + 1) and (tempState.board[row + 1][col + 1] % 2 != tempState.board[row-move][col-move] % 2)\
                    and tempState.board[row+1][col+1] != 0 and ((piece is 10 or piece is 11) or ((piece is 8 or piece is 9) and (tempState.board[row+1][col+1] is 10 or tempState.board[row+1][col+1] is 11))):
                kill = True
                hold = tempState.board[row+1][col+1]
                tempState.board[row+1][col+1] = 0
                capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                tempState.board[row+1][col+1] = hold

        if piece is 6 or piece is 7 or piece is 8 or piece is 9:
            if isValidPosition(row - move - 1, col - move - 1) and\
                    (tempState.board[row - move - 1][col - move - 1] % 2 != tempState.board[row - move][col - move] % 2)\
                    and tempState.board[row - move - 1][col - move - 1] != 0:
                if isValidPosition(row - move - 2, col - move - 2) and tempState.board[row - move - 2][col - move - 2] == 0:
                    if (piece is 6 or piece is 7) or ((piece is 8 or piece is 9) and (
                            tempState.board[row - move - 1][col - move - 1] is 6 or tempState.board[row - move - 1][col - move - 1] is 7)):
                        capture_hold = tempState.board[row - move - 1][col - move - 1]
                        curr_hold = tempState.board[row - move][col - move]
                        tempState.board[row - move - 2][col - move - 2] = tempState.board[row - move][col - move]
                        tempState.board[row - move - 1][col - move - 1] = 0
                        tempState.board[row - move][col - move] = 0
                        capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
                        kill = True
                        tempState.board[row - move - 2][col - move - 2] = 0
                        tempState.board[row - move - 1][col - move - 1] = capture_hold
                        tempState.board[row - move][col - move] = curr_hold

        if not kill:
            states.append(tempState)
        move += 1
    return capture, states


#  Creates potential states for the Pincher or the Imitator
def move_Pinch(state, row, col):
    newState = BC.BC_state(state.board)
    piece = state.board[row][col]
    states = []
    capture = []
    cont = True
    move = 1
    while cont:
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row + move, col) or newState.board[row + move][col] != 0:
            break
        tempState.board[row + move][col] = tempState.board[row][col]
        tempState.board[row][col] = 0
        kill = False
        for i in range(-2, 3, 4):
            if 0 <= row + move + i < 8:
                row_temp = tempState.board[row + move + i][col]
                if row_temp is tempState.board[row + move][col] and (row_temp % 2 != tempState.board[row + move + int(i/2)][col] % 2):
                    tempState.board[row + move + int(i / 2)][col] = 0
                    kill = True
                elif ((piece is 8 or piece is 9) and (row_temp is 2 or row_temp is 3)) and (row_temp % 2 != tempState.board[row + move + int(i/2)][col] % 2) \
                        and (row_temp % 2 is piece % 2):
                    if tempState.board[row + move + int(i/2)][col] is 2 or tempState.board[row + move + int(i/2)][col] is 3:
                        tempState.board[row + move + int(i / 2)][col] = 0
                        kill = True
                elif ((piece is 2 or piece is 3) and (row_temp is 8 or row_temp is 9)) and (row_temp % 2 != tempState.board[row + move + int(i/2)][col] % 2) and (row_temp % 2 is piece % 2):
                    if tempState.board[row + move + int(i/2)][col] is 2 or tempState.board[row + move + int(i/2)][col] is 3:
                        tempState.board[row + move + int(i / 2)][col] = 0
                        kill = True
            if 0 <= col + i < 8:
                col_temp = tempState.board[row + move][col + i]
                if col_temp is tempState.board[row + move][col] and (col_temp % 2 != tempState.board[row + move][col + int(i / 2)] % 2):
                    tempState.board[row + move][col + int(i / 2)] = 0
                    kill = True
                elif ((piece is 8 or piece is 9) and (col_temp is 2 or col_temp is 3)) and (col_temp % 2 != tempState.board[row + move][col + int(i/2)] % 2) and (col_temp % 2 is piece % 2):
                    if tempState.board[row + move][col + int(i/2)] is 2 or tempState.board[row + move][col + int(i/2)] is 3:
                        tempState.board[row + move][col + int(i / 2)] = 0
                        kill = True
                elif ((piece is 2 or piece is 3) and (col_temp is 8 or col_temp is 9)) and (col_temp % 2 != tempState.board[row + move][col + int(i/2)] % 2) and (col_temp % 2 is piece % 2):
                    if tempState.board[row + move][col + int(i/2)] is 2 or tempState.board[row + move][col + int(i/2)] is 3:
                        tempState.board[row + move][col + int(i / 2)] = 0
                        kill = True
        if kill:
            capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
        else:
            states.append(tempState)
        move += 1
    while cont:
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row - move, col) or newState.board[row - move][col] != 0:
            break
        tempState.board[row - move][col] = tempState.board[row][col]
        tempState.board[row][col] = 0
        kill = False
        for i in range(-2, 3, 4):
            if 0 <= row - move + i < 8:
                row_temp = tempState.board[row - move + i][col]
                if row_temp is tempState.board[row - move][col] and (
                        row_temp % 2 != tempState.board[row - move + int(i / 2)][col] % 2):
                    tempState.board[row - move + int(i / 2)][col] = 0
                    kill = True
                elif ((piece is 8 or piece is 9) and (row_temp is 2 or row_temp is 3)) and (row_temp % 2 != tempState.board[row - move + int(i/2)][col] % 2) and (row_temp % 2 is piece % 2):
                    if tempState.board[row - move + int(i/2)][col] is 2 or tempState.board[row - move + int(i/2)][col] is 3:
                        tempState.board[row - move + int(i / 2)][col] = 0
                        kill = True
                elif ((piece is 2 or piece is 3) and (row_temp is 8 or row_temp is 9)) and (row_temp % 2 != tempState.board[row - move + int(i/2)][col] % 2) and (row_temp % 2 is piece % 2):
                    if tempState.board[row - move + int(i/2)][col] is 2 or tempState.board[row - move + int(i/2)][col] is 3:
                        tempState.board[row - move + int(i / 2)][col] = 0
                        kill = True
            if 0 <= col + i < 8:
                col_temp = tempState.board[row - move][col + i]
                if col_temp is tempState.board[row - move][col] and (
                        col_temp % 2 != tempState.board[row - move][col + int(i / 2)] % 2):
                    tempState.board[row - move][col + int(i / 2)] = 0
                    kill = True
                elif ((piece is 8 or piece is 9) and (col_temp is 2 or col_temp is 3)) and (col_temp % 2 != tempState.board[row - move][col + int(i/2)] % 2) and (col_temp % 2 is piece % 2):
                    if tempState.board[row - move][col + int(i/2)] is 2 or tempState.board[row - move][col + int(i/2)] is 3:
                        tempState.board[row - move][col + int(i / 2)] = 0
                        kill = True
                elif ((piece is 2 or piece is 3) and (col_temp is 8 or col_temp is 9)) and (col_temp % 2 != tempState.board[row - move][col + int(i/2)] % 2) and (col_temp % 2 is piece % 2):
                    if tempState.board[row - move][col + int(i/2)] is 2 or tempState.board[row - move][col + int(i/2)] is 3:
                        tempState.board[row - move][col + int(i / 2)] = 0
                        kill = True
        if kill:
            capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
        else:
            states.append(tempState)
        move += 1
    move = 1
    while cont:
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row, col + move) or newState.board[row][col + move] != 0:
            break
        tempState.board[row][col + move] = tempState.board[row][col]
        tempState.board[row][col] = 0
        kill = False
        for i in range(-2, 3, 4):
            if 0 <= row + i < 8:
                row_temp = tempState.board[row + i][col + move]
                if row_temp is tempState.board[row][col + move] and (
                        row_temp % 2 != tempState.board[row+int(i / 2)][col+move] % 2):
                    tempState.board[row + int(i / 2)][col + move] = 0
                    kill = True
                elif ((piece is 8 or piece is 9) and (row_temp is 2 or row_temp is 3)) and (row_temp % 2 != tempState.board[row + int(i/2)][col + move] % 2) and (row_temp % 2 is piece % 2):
                    if tempState.board[row + int(i/2)][col + move] is 2 or tempState.board[row + int(i/2)][col + move] is 3:
                        tempState.board[row + int(i / 2)][col + move] = 0
                        kill = True
                elif ((piece is 2 or piece is 3) and (row_temp is 8 or row_temp is 9)) and (row_temp % 2 != tempState.board[row + int(i/2)][col + move] % 2) and (row_temp % 2 is piece % 2):
                    if tempState.board[row + int(i/2)][col + move] is 2 or tempState.board[row + int(i/2)][col + move] is 3:
                        tempState.board[row + int(i / 2)][col + move] = 0
                        kill = True
            if 0 <= col + move + i < 8:
                col_temp = tempState.board[row][col + move + i]
                if col_temp is tempState.board[row][col + move] and (
                        col_temp % 2 != tempState.board[row][col + move + int(i / 2)] % 2):
                    tempState.board[row][col + move + int(i / 2)] = 0
                    kill = True
                elif ((piece is 8 or piece is 9) and (col_temp is 2 or col_temp is 3)) and (col_temp % 2 != tempState.board[row][col + move + int(i/2)] % 2) and (col_temp % 2 is piece % 2):
                    if tempState.board[row][col + move + int(i/2)] is 2 or tempState.board[row][col + move + int(i/2)] is 3:
                        tempState.board[row][col + move + int(i / 2)] = 0
                        kill = True
                elif ((piece is 2 or piece is 3) and (col_temp is 8 or col_temp is 9)) and (col_temp % 2 != tempState.board[row][col + move + int(i/2)] % 2) and (col_temp % 2 is piece % 2):
                    if tempState.board[row][col + move + int(i/2)] is 2 or tempState.board[row][col + move + int(i/2)] is 3:
                        tempState.board[row][col + move + int(i / 2)] = 0
                        kill = True
        if kill:
            capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
        else:
            states.append(tempState)
        move += 1
    move = 1
    while cont:
        tempState = BC.BC_state(state.board)
        if not isValidPosition(row, col - move) or newState.board[row][col - move] != 0:
            break
        tempState.board[row][col - move] = tempState.board[row][col]
        tempState.board[row][col] = 0
        kill = False
        for i in range(-2, 3, 4):
            if 0 <= row + i < 8:
                row_temp = tempState.board[row + i][col - move]
                if row_temp is tempState.board[row][col - move] and (
                        row_temp % 2 != tempState.board[row + int(i / 2)][col - move] % 2):
                    tempState.board[row + int(i / 2)][col - move] = 0
                    kill = True
                elif ((piece is 8 or piece is 9) and (row_temp is 2 or row_temp is 3)) and (row_temp % 2 != tempState.board[row + int(i/2)][col - move] % 2) and (row_temp % 2 is piece % 2):
                    if tempState.board[row + int(i/2)][col - move] is 2 or tempState.board[row + int(i/2)][col - move] is 3:
                        tempState.board[row + int(i / 2)][col - move] = 0
                        kill = True
                elif ((piece is 2 or piece is 3) and (row_temp is 8 or row_temp is 9)) and (row_temp % 2 != tempState.board[row + int(i/2)][col - move] % 2) and (row_temp % 2 is piece % 2):
                    if tempState.board[row + int(i/2)][col - move] is 2 or tempState.board[row + int(i/2)][col - move] is 3:
                        tempState.board[row + int(i / 2)][col - move] = 0
                        kill = True
            if 0 <= col - move + i < 8:
                col_temp = tempState.board[row][col - move + i]
                if col_temp is tempState.board[row][col - move] and (col_temp % 2 != tempState.board[row][col - move + int((i / 2))] % 2):
                    tempState.board[row][col - move + int(i / 2)] = 0
                    kill = True
                elif ((piece is 8 or piece is 9) and (col_temp is 2 or col_temp is 3)) and (col_temp % 2 != tempState.board[row][col - move + int(i/2)] % 2) and (col_temp % 2 is piece % 2):
                    if tempState.board[row][col - move + int(i/2)] is 2 or tempState.board[row][col - move + int(i/2)] is 3:
                        tempState.board[row][col - move + int(i / 2)] = 0
                        kill = True
                elif ((piece is 2 or piece is 3) and (col_temp is 8 or col_temp is 9)) and (col_temp % 2 != tempState.board[row][col - move + int(i/2)] % 2) and (col_temp % 2 is piece % 2):
                    if tempState.board[row][col - move + int(i/2)] is 2 or tempState.board[row][col - move + int(i/2)] is 3:
                        tempState.board[row][col - move + int(i / 2)] = 0
                        kill = True
        if kill:
            capture.insert(0, BC.BC_state(tempState.board, tempState.whose_move))
        else:
            states.append(tempState)
        move += 1
    return capture, states


#  Creates potential states for the King
def move_King(state, row, col):
    newState = BC.BC_state(state.board)
    piece = state.board[row][col]
    states = []
    capture = []
    for i in range (-1, 2):
        for j in range(-1, 2):
            if i != 0 and j != 0:
                newRow = row + i
                newCol = col + j
                if isValidPosition(newRow, newCol) and (newState.board[newRow][newCol] == 0 or newState.board[newRow][newCol] % 2 != newState.board[row][col] % 2):
                    tempState = BC.BC_state(state.board)
                    if newState.board[newRow][newCol] != 0:
                        if (piece is 8 or piece is 9) and (newState.board[newRow][newCol] is 13 or newState.board[newRow][newCol] is 14):
                            tempState.board[newRow][newCol] = tempState.board[row][col]
                            tempState.board[row][col] = 0
                            capture.insert(0, tempState)
                        elif piece is 13 or piece is 14:
                            tempState.board[newRow][newCol] = tempState.board[row][col]
                            tempState.board[row][col] = 0
                            capture.insert(0, tempState)
                    else:
                        tempState.board[newRow][newCol] = tempState.board[row][col]
                        tempState.board[row][col] = 0
                        states.append(tempState)
    return capture, states


def isValidPosition(row, col):
    if 0 <= row < 8 and 0 <= col < 8:
        return True
    return False


