import BC_state_etc as bC
from DeepPurple_BC_Node import Node
import DeepPurple_BC_ZHash as zHash
import copy

""" Constants to convert a piece name to the number associated with the 
piece. Identical to the mapping in BC_state_etc, but *with* the color 
designation"""
BLACK_PINCER = 2
BLACK_COORDINATOR = 4
BLACK_LEAPER = 6
BLACK_IMITATOR = 8
BLACK_WITHDRAWER = 10
BLACK_KING = 12
BLACK_FREEZER = 14

WHITE_PINCER = 3
WHITE_COORDINATOR = 5
WHITE_LEAPER = 7
WHITE_IMITATOR = 9
WHITE_WITHDRAWER = 11
WHITE_KING = 13
WHITE_FREEZER = 15

""" A dictionary mapping the names for cardinal directions with the 
left handed cartesian directions as the values where 1 represents a positive 
direction (right for x-axis and down for y axis) and -1 represents the 
negative direction. Ordered (y, x) """
CARDINAL_DIRECTIONS = {"N":  (-1,  0),
                       "E":  (0,   1),
                       "S":  (1,   0),
                       "W":  (0,  -1),
                       "NE": (-1,  1),
                       "SE": (1,   1),
                       "SW": (1,  -1),
                       "NW": (-1, -1)}

""" A dictionary mapping the names for only manhattan directions with the 
left handed cartesian directions as the values where 1 represents a positive 
direction (right for x-axis and down for y axis) and -1 represents the 
negative direction. Ordered (y, x) """
MANHATTAN_DIRECTIONS = {"N":  (-1,  0),
                        "E":  (0,   1),
                        "S":  (1,   0),
                        "W":  (0,  -1)}

"""
Directions currently allowed for exploration: N, E, S, W, NE, SE, SW, NW
"""
directions_allowed = {"N":  True,
                      "E":  True,
                      "S":  True,
                      "W":  True,
                      "NE": True,
                      "SE": True,
                      "SW": True,
                      "NW": True}

use_zobrist_hashing = False


def generate_successors(curr_node, zobrist_hashing=False):
    """
    Returns an ordered list of nodes for each state that could arise from all
    legal moves from a given state. The list will be ordered first by the
    location of the pieces origin (x then y) and second by the pieces end-point
    (x then y).
    :param curr_node:       the node for the state before the move is made
    :param zobrist_hashing  True if Zobrist hashing should bve used
    :return:                the list of new nodes
    """
    global use_zobrist_hashing
    use_zobrist_hashing = zobrist_hashing
    board = curr_node.board
    whose_move = curr_node.whose_move
    successor_nodes = []
    for y in range(8):
        for x in range(8):
            piece = (y, x, board[y][x])
            if is_piece(piece[2]) and whose_move == (piece[2] % 2):
                successor_nodes.extend(
                    get_piece_successors(curr_node, piece))
    return successor_nodes


def get_piece_successors(curr_node, piece):
    """
    Returns an ordered list of nodes for each state that could arise from a
    single piece's action. The list will be ordered first by the pieces
    end-point (x then y). If the piece is frozen, this will return an empty
    list.
    :param curr_node: the node for the board before the move is made
    :param piece:    the piece to be moved
    :return:         the list of new nodes
    """
    board = curr_node.board
    successor_nodes = []
    if not is_frozen(board, piece):
        if is_pincer(piece):
            piece_moves = get_moves(board, piece, MANHATTAN_DIRECTIONS)
        elif is_king(piece):
            piece_moves = get_adjacent_moves(board, piece)
        elif is_imitator(piece):
            piece_moves = get_moves(board, piece, CARDINAL_DIRECTIONS)
            piece_moves.extend(get_adjacent_moves(board, piece))
        else:  # all other piece types besides pincers and kings
            piece_moves = get_moves(board, piece, CARDINAL_DIRECTIONS)
        # print("Current piece: " + bC.CODE_TO_INIT[piece[2]])
        # print(piece_moves)
        successor_nodes = [get_attack_outcome(curr_node, piece, move)
                           for move in piece_moves]
    return successor_nodes


def get_adjacent_moves(board, piece):
    """
    Finds and returns all adjacent moves for the piece that are on the board
    and not on a piece of the same color.
    :param board: the pre-move state of the board
    :param piece: the piece to move (starting y, starting x, piece-type)
    :return:      an ordered list of tuples (y-coordinate, x-coordinate, piece)
        where the coordinates represent the endpoint of the move, the piece is
        the piece that is moved, and the order is done by first increasing x the
        increasing y coordinate of the endpoint.
    """
    moves = []
    adj_spaces = get_adjacent((piece[0], piece[1]))
    for adjacent in adj_spaces:
        target_piece = board[adjacent[0]][adjacent[1]]
        target = (adjacent[0], adjacent[1], target_piece)
        if is_imitator(piece) and is_king(target) and is_enemy(piece, target):
            moves.append((adjacent[0], adjacent[1], piece[2]))
        if (is_king(piece) and
                (is_enemy(piece, target) or not is_piece(target_piece))):
            moves.append((adjacent[0], adjacent[1], piece[2]))
    moves.sort(key=lambda move: (move[1], move[0]))  # sort by x,y
    return moves


def get_adjacent(origin):
    """
    returns a list of coordinates for the spaces adjacent to the origin which
    are in the bounds of the game board
    :param origin: the coordinates of the origin to be searched
    :return:       a list of coordinates (y, x) for the adjacent spaces
    """
    adjacent_list = []
    for direction in CARDINAL_DIRECTIONS.values():
        y = origin[0] - direction[0]
        x = origin[1] - direction[1]
        if is_coordinate_in_board(y, x):
            adjacent_list.append((y, x))
    return adjacent_list


def get_moves(board, piece, directions):
    """
    Finds all potential spaces a given piece could move in the cardinal
    directions (Chess "queen-like" movement).
    :param board: the pre-move state of the board
    :param piece: the piece to move (starting y, starting x, piece-type)
    :param directions: the dictionary of all directions the piece is allowed
        to move.
    :return: an ordered list of tuples (y-coordinate, x-coordinate, piece)
        where the coordinates represent the endpoint of the move, the piece is
        the piece that is moved, and the order is done by first increasing x the
        increasing y coordinate of the endpoint.
    """

    # global directions_allowed

    moves = []
    if len(directions.keys()) > 8:
        raise Exception("length = %i" % directions.keys())
    for direction in directions.keys():  # in all cardinal directions

        # Direction could be banned if it's already determined to be blocked
        # if directions_allowed[direction]:
        dir_tuple = directions[direction]
        moves.extend(find_open_spaces_in_direction(
                     board, piece, dir_tuple))

    moves.sort(key=lambda move: (move[1], move[0]))  # sort by x,y
    return moves


def find_open_spaces_in_direction(board, piece, dir_tuple):
    """
    Finds the number of open spaces in a single direction from the given
    start location.
    :param board: the list of lists containing the mapping of coordinates to
        pieces where the first list's indices represent the y-coordinate and the
        second list the x-coordinate.
    :param piece: a tuple containing (y-coordinate of start location,
        x-coordinate of start location, piece) for the piece to be moved
    :param dir_tuple: a tuple containing (y-increment, x-increment) to move a
        piece in the desired direction.
    :return: an unordered list of tuples (y-coordinate, x-coordinate, piece)
        where the coordinates represent the endpoint of the move, and the
        piece is the piece that is moved.
    """

    # global directions_allowed
    moves = []
    open_space = True
    move_y = piece[0]
    move_x = piece[1]
    while open_space:
        move_y += dir_tuple[0]
        move_x += dir_tuple[1]
        # print(move_y, move_x) # DEBUG
        if not is_coordinate_in_board(move_y, move_x):
            open_space = False
        else:
            target = (move_y, move_x, board[move_y][move_x])
            if not is_piece(target[2]):
                moves.append((target[0], target[1], piece[2]))
            else:  # if square is on a unit
                # special case : Imitator Leaping a leaper
                # special case : Leaper
                is_leap_target = False
                if is_imitator(piece):
                    is_leap_target = (is_leaper(target) and
                                      is_enemy(piece, target))
                if is_leaper(piece):
                    is_leap_target = is_enemy(piece, target)

                if is_leap_target:
                    landing_y = move_y + dir_tuple[0]
                    landing_x = move_x + dir_tuple[1]
                    if is_coordinate_in_board(landing_y, landing_x):
                        landing_sq = (landing_y, landing_x, board[landing_y][
                            landing_x])
                        if not is_piece(landing_sq[2]):
                            moves.append((landing_sq[0],
                                          landing_sq[1],
                                          piece[2]))
                open_space = False
                # directions_allowed[direction] = False
                # print("direction banned: " + direction)
    return moves


def get_attack_outcome(curr_node, piece, move):
    pre_board = curr_node.board
    # deep copy board
    outcome_board = copy.deepcopy(pre_board)
    outcome_hash = copy.deepcopy(curr_node.zobrist_hash)
    pieces_taken = []
    witty_responce = ""
    # print(piece[0], piece[1])
    # print(move[0], move[1])
    if is_pincer(piece):
        pieces_taken, witty_responce = get_pincer_attack(
            pre_board, piece, move, pieces_taken)
    elif is_coordinator(piece):
        pieces_taken, witty_responce = get_coordinator_attack(
            pre_board, piece, move, pieces_taken)
    elif is_leaper(piece):
        pieces_taken, witty_responce = get_leaper_attack(
            pre_board, piece, move, pieces_taken)
    elif is_imitator(piece):
        pieces_taken, witty_responce = get_imitator_attack(
            pre_board, piece, move, pieces_taken)
    elif is_withdrawer(piece):
        pieces_taken, witty_responce = get_withdrawer_attack(
            pre_board, piece, move, pieces_taken)
    elif is_king(piece):
        pieces_taken, witty_responce = get_king_attack(
            pre_board, move, pieces_taken)
    elif is_freezer(piece):
        witty_responce = get_freezer_attack(
            pre_board, move)
    pieces_taken.append(piece)  # the piece moved is taken from its start loc
    for target in pieces_taken:  # remove pieces taken
        if is_piece(outcome_board[target[0]][target[1]]):
            outcome_board[target[0]][target[1]] = 0
        # else:
        #     print("pieces taken:")
        #     print(pieces_taken)
        #     print("there should not be duplicate squares being taken by an "
        #           "attack")
        #     print("Piece at (%i,%i) is a %i and was taken by a %i" % (
        #         target[0], target[1], outcome_board[target[0]][target[1]],
        #         piece[2]))
        #     raise Exception("blank square taken in piece attack (see below)")
        if use_zobrist_hashing:
            outcome_hash = zHash.change_hash_by_piece(outcome_hash,
                                                      outcome_board,
                                                      target)

    outcome_board[move[0]][move[1]] = move[2]
    if use_zobrist_hashing:
        outcome_hash = zHash.change_hash_by_piece(outcome_hash,
                                                  outcome_board,
                                                  move)
    if use_zobrist_hashing:
        zHash.HASH_TO_BOARD_MAP[outcome_hash] = outcome_board
    output_move = ((piece[0], piece[1]), (move[0], move[1]))
    outcome_node = Node(outcome_board,
                        outcome_hash,         # zobrist hash
                        curr_node,            # predecessor
                        None,                 # Score
                        output_move,          # ((from_y, from_x), (to_y, to_x))
                        not curr_node.whose_move,   # whose_move
                        witty_responce)             # response

    return outcome_node


def get_pincer_attack(board, piece, move, pieces_taken):
    witty_response = "I'm gonna pince you!"
    piece_is_imitator = is_imitator(piece)
    manhattan_movement = True
    if piece_is_imitator and 0 not in (move[0], move[1]):
        manhattan_movement = False
    if manhattan_movement:
        # Could be optimized to avoid fourth direction
        for direction in MANHATTAN_DIRECTIONS.values():
            partner_y = move[0] + (2 * direction[0])
            partner_x = move[1] + (2 * direction[1])
            # don't check on edge of board
            if is_coordinate_in_board(partner_y, partner_x):
                partner = (partner_y, partner_x, board[partner_y][partner_x])
                # don't check if partner not present
                if is_piece(partner[2]) and not is_enemy(piece, partner):
                    enemy_y = move[0] + direction[0]
                    enemy_x = move[1] + direction[1]
                    enemy = (enemy_y, enemy_x, board[enemy_y][enemy_x])
                    if is_piece(enemy[2]) and is_enemy(piece, enemy):
                        piece_is_pincer = is_pincer(piece)
                        target_is_pincer = is_pincer(enemy)
                        if piece_is_pincer or (piece_is_imitator and
                                               target_is_pincer):
                            pieces_taken.append(enemy)
                            witty_response = "Give 'em the clamps!"
                            # print("Pincer has taken a piece!")
                            # print("Partner = (%i, %i, %s)" % (
                            #     partner[0], partner[1],
                            #     bC.CODE_TO_INIT[partner[2]]))
                            # print("Enemy = (%i, %i, %s)" % (
                            #     enemy[0], enemy[1],
                            #     bC.CODE_TO_INIT[enemy[2]]))
                            # print("Pincer = (%i, %i, %s)" % (
                            #     move[0], move[1],
                            #     bC.CODE_TO_INIT[move[2]]))
                            # END DEBUG SECTION
    return pieces_taken, witty_response


def get_coordinator_attack(board, piece, move, pieces_taken):
    witty_response = "The secret to my success is good coordination."
    king = where_is_the_king(board, get_piece_color(piece))
    targets = []
    if king is not None:
        targets.append((move[0], king[1], board[move[0]][king[1]]))
        targets.append((king[0], move[1], board[king[0]][move[1]]))
    for target in targets:
        if is_enemy(piece, target):
            if is_coordinator(piece) or (is_imitator(piece) and
                                         is_coordinator(target)):
                pieces_taken.append(target)
                witty_response = "Watch me coordinate your defeat!"
                # print("Coordinator has taken a piece!")
                # print("Coordinator = (%i, %i, %s)" % (move[0], move[1],
                #                                       bC.CODE_TO_INIT[move[2]]))
                # print("King = (%i, %i, %s)" % (king[0], king[1],
                #                                bC.CODE_TO_INIT[king[2]]))
                # print("Enemy = (%i, %i, %s)" % (target[0], target[1],
                #                                 bC.CODE_TO_INIT[target[2]]))
    return pieces_taken, witty_response


def get_leaper_attack(board, piece, move, pieces_taken):
    witty_response = "Time for me to leap in to action."
    dir_y = sign(move[0] - piece[0])  # get sign of delta y
    dir_x = sign(move[1] - piece[1])  # get sign of delta x
    target_y = move[0] - dir_y
    target_x = move[1] - dir_x
    target_piece = board[target_y][target_x]
    target = (target_y, target_x, target_piece)
    if is_piece(target[2]):  # a leaped piece will always be an enemy
        pieces_taken.append(target)
        witty_response = "Looks like this is going to be a leap year!"
    return pieces_taken, witty_response


def get_imitator_attack(board, piece, move, pieces_taken):
    witty_response = "They say that imitation is the most sincere from of " \
                     "flattery"
    # handles restriction to only taken withdrawn withdrawers
    get_withdrawer_attack(board, piece, move, pieces_taken)
    # A leaped target will always be valid for imitator
    get_leaper_attack(board, piece, move, pieces_taken)
    # handles manhattan restriction and limitation to pincing pincers
    get_pincer_attack(board, piece, move, pieces_taken)
    # handles restriction to only coordinating coordinators
    get_coordinator_attack(board, piece, move, pieces_taken)
    # An imitator will only be in the square of a king with a valid move
    get_king_attack(board, move, pieces_taken)

    for victim in pieces_taken:
        if is_withdrawer(victim):
            witty_response = "Don't mind me, just a normal withdrawer..."
        elif is_coordinator(victim):
            witty_response = "Don't mind me, just a normal coordinator..."
        elif is_leaper(victim):
            witty_response = "Don't mind me, just a normal leaper..."
        elif is_pincer(victim):
            witty_response = "Don't mind me, just a normal pincer..."
        elif is_king(victim):
            witty_response = "Don't mind me, just a normal king.."
    return pieces_taken, witty_response


def get_withdrawer_attack(board, piece, move, pieces_taken):
    witty_response = "I think it's time for you to withdraw from this match."
    dir_y = sign(move[0] - piece[0])  # get sign of delta y
    dir_x = sign(move[1] - piece[1])  # get sign of delta x
    target_y = piece[0] - dir_y
    target_x = piece[1] - dir_x
    if is_coordinate_in_board(target_y, target_x):
        target_piece = board[target_y][target_x]
        if is_piece(target_piece):
            target = (target_y, target_x, target_piece)
            if is_enemy(piece, target):
                # SPECIAL CASE: Imitator imitating a withdrawer
                if is_withdrawer(piece) or (
                        is_imitator(piece) and is_withdrawer(target)):
                    pieces_taken.append(target)
                    witty_response = ("Please withdraw your piece from the "
                                      "board.")
    return pieces_taken, witty_response


def get_king_attack(board, move, pieces_taken):
    witty_response = "Let me just get this out of the way..."
    target = (move[0], move[1], board[move[0]][move[1]])
    if is_piece(target[2]):  # if occupying the same square as a piece
        pieces_taken.append(target)
        witty_response = "BOW BEFORE YOUR KING!"
    return pieces_taken, witty_response


def get_freezer_attack(board, move):
    witty_response = "Playing it cool..."
    num_targets = does_freezer_freeze(board, move)
    if num_targets >= 1:
        witty_response = "FREEZE!"
    return witty_response


def does_freezer_freeze(board, piece):
    adjacent_spaces = get_adjacent((piece[0], piece[1]))
    enemy = 1 - (piece[2] % 2)
    targets = 0
    for space in adjacent_spaces:
        target = board[space[0]][space[1]]
        if target % 2 == enemy:
            targets += 1
    return targets


def is_coordinate_in_board(y, x):
    """
    Returns true if the coordinates are in the bounds of the game board.
    :param y: the y coordinate to check
    :param x: the x coordinate to check
    :return: true if in and false if outside the range 0-8
    """
    return (0 <= y < 8) and (0 <= x < 8)


def sign(x):
    """ takes a signed integer and returns the sign """
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


def where_is_the_king(board, player):
    """
    Returns the coordinates of the current players king
    :param board:  the game board to be searched
    :param player: the side number for the player's king to be searched
    :return:       the coordinates of the king
    """
    players_king = 12 + player
    for y in range(8):
        for x in range(8):
            if board[y][x] == players_king:
                king_tuple = (y, x, board[y][x])
                return king_tuple
    return None
    # raise Exception("GAME STATE ERROR: THE KING IS DEAD!")


def proximity_to_king(board, coord, king_color):
    """
    Return the Manhattan distance from a piece to a king of the given color
    """
    curr_piece_y = coord[0]
    curr_piece_x = coord[1]
    # 0 is black, 1 is white
    king = where_is_the_king(board, king_color)
    if king is not None:
        return abs(king[0] - curr_piece_y) + abs(king[1] - curr_piece_x)
    else:
        return None


def get_piece_color(piece):
    return piece[2] % 2


def is_imitator(piece):
    return piece[2] in (BLACK_IMITATOR, WHITE_IMITATOR)


def is_withdrawer(piece):
    return piece[2] in (BLACK_WITHDRAWER, WHITE_WITHDRAWER)


def is_coordinator(piece):
    return piece[2] in (BLACK_COORDINATOR, WHITE_COORDINATOR)


def is_king(piece):
    return piece[2] in (BLACK_KING, WHITE_KING)


def is_freezer(piece):
    return piece[2] in (BLACK_FREEZER, WHITE_FREEZER)


def is_leaper(piece):
    return piece[2] in (BLACK_LEAPER, WHITE_LEAPER)


def is_pincer(piece):
    return piece[2] in (BLACK_PINCER, WHITE_PINCER)


def is_piece(piece_type):
    """
    returns if the piece type is for an empty space
    :param piece_type: the integer value for the piece type
    :return:           true if the given value represents a piece, false if
                       the space is empty
    """
    return piece_type != 0


def is_enemy(piece, target):
    """
    Takes a tuple of the piece and the target and returns true if the target
    is on the opposing side of the piece, false otherwise
    :param piece:   the piece to be checked against
    :param target:  the piece to be checked
    :return:        true if the target piece is not on the same side
    """
    piece_side = piece[2] % 2
    target_side = target[2] % 2
    return piece_side != target_side


def is_frozen(board, piece):
    """
    Checks both if the given piece is adjacent to an enemy freezer and
    if the given piece is adjacent to an opposing imitator which is adjacent to
    a friendly freezer

    :param board:   the game board to be checked
    :param piece:   the piece to be checked to see if it is frozen
    :return:        True if the piece is frozen, false otherwise
    """
    adj_spaces = get_adjacent((piece[0], piece[1]))
    for adjacent in adj_spaces:
        target = (adjacent[0], adjacent[1], board[adjacent[0]][adjacent[1]])
        if is_enemy(target, piece):
            if (is_freezer(target) or
               (is_imitator(target) and is_freezer(piece))):
                return True
    return False


def is_white(piece_type):
    """
    Precond: Piece passed in has to be a piece, and not an empty square
    Returns whether a piece is white (or black)
    """
    if piece_type == 0 or piece_type == 1:
        raise Exception("Piece passed in is actually a square/1, fix your code")

    # If piece is even number: BLACK
    if piece_type % 2 == 0:
        return False

    # WHITE
    return True
