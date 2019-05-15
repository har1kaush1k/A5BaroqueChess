import random
import BC_state_etc as bC

""" A mapping of zobrist hash values for a specific piece at a specific 
coordinate location on the board to a tuple representing the same information 
in the form (y-coord, z-coord, piece ) """
PIECE_TO_Z_HASH_MAP = {}

""" The main dictionary used by the zobrist hash which maps the unique hashes 
to their corresponding boards in the format of board[y-coord][x-coord] = 
piece type as a number """
HASH_TO_BOARD_MAP = {}

""" The secondary dictionary used by the zobrist hash which maps the unique 
hashes to an integer for the "score" given by a static evaluation of that 
given board. This dictionary is used to prevent and avoid recalculating 
identical states reached by different move paths """
HASH_TO_SCORE_MAP = {}

""" A hash of the initial board, set to an arbitrary random number if z_hashing 
is not being used"""
INITIAL_BOARD_HASH = random.getrandbits(64)


def prepare_z_hash():
    """
    Populates maps of random 64 bits to piece tuples (y, x, piece type) and a
    reverse map starting from those piece tuples to the associated hashes.
    """
    for y in range(8):
        for x in range(8):
            for piece in range(16):
                piece_tuple = (y, x, piece)
                z_hash = random.getrandbits(64)
                PIECE_TO_Z_HASH_MAP[piece_tuple] = z_hash
    """ Hashes the initial board """
    global INITIAL_BOARD_HASH
    INITIAL_BOARD_HASH = z_hash_board(bC.INITIAL)


def z_hash_board(board):
    """
    Generates and returns the Zobrist hash for a given board by XORing all
    the hashes of pieces on the board.
    :param board: a matrix of lists in the form of board[y-coordinate][
    x-coordinate] storing the piece type on those locations.
    :return: the Zobrist hash for the board
    """
    z_hash = 0
    for y in range(8):
        for x in range(8):
            piece_tuple = (y, x, board[y][x])
            z_hash = z_hash ^ get_z_hash_from_piece(piece_tuple)
            HASH_TO_BOARD_MAP[z_hash] = board
    return z_hash


def get_z_hash_from_piece(piece_tuple):
    """
    finds and returns the zobrist hash for the given piece/location tuple
    :param piece_tuple in the form (y-coord, x-coord, piece)
    :return: the zobrist hash for that piece
    """
    return PIECE_TO_Z_HASH_MAP[piece_tuple]


def change_hash_by_piece(z_hash, outcome_board, piece_tuple):
    """
    Takes a hash and a piece/location combo that is either added or removed
    and returns the hash of the board after that change.

    :param z_hash: the zobrist hash for the board before the change
    :param outcome_board the board that corresponds to output z_hash
    :param piece_tuple: in the form (y-coord, x-coord, piece)
    :return: A zobrist hash for the new board state after the given change
    """
    z_hash = z_hash ^ get_z_hash_from_piece(piece_tuple)
    return z_hash

# def z_hash_all_boards():
#     from itertools import combinations
#     from itertools import permutations
#
#     """ A list of the pieces used in the game for use in creating the zobrist
#     hashes"""
#     LIST_OF_PIECES = [4, 6, 8, 10, 12, 8, 6, 14,
#                       2, 2, 2, 2, 2, 2, 2, 2,
#                       3, 3, 3, 3, 3, 3, 3, 3,
#                       15, 7, 9, 11, 13, 9, 7, 5, ]
#
#     """ A mask of the board in the empty state to create complete boards that
#     include empty spaces when generating zobrist hashes """
#     BOARD_MASK = [0, 0, 0, 0, 0, 0, 0, 0,
#                   0, 0, 0, 0, 0, 0, 0, 0,
#                   0, 0, 0, 0, 0, 0, 0, 0,
#                   0, 0, 0, 0, 0, 0, 0, 0,
#                   0, 0, 0, 0, 0, 0, 0, 0,
#                   0, 0, 0, 0, 0, 0, 0, 0,
#                   0, 0, 0, 0, 0, 0, 0, 0,
#                   0, 0, 0, 0, 0, 0, 0, 0]
#
#     # GET ALL POSSIBLE SETS OF REMAINING PIECES
#     all_combos = [[]]  # list of piece lists
#     num_pieces = 32  # 16 per side
#     for pieces_left in range(1, num_pieces + 1):  # for all # remaining
#         piece_combinations = combinations(LIST_OF_PIECES, pieces_left)
#         # ADD EMPTY SPACES TO GET 64 space lists
#         print("Printing piece combos")
#         combo_counter = 0
#         for piece_combo in piece_combinations:
#             combo_counter += 1
#             # add zeros to 64 items long
#             piece_combos_64 = BOARD_MASK[pieces_left:]
#             piece_combos_64.extend(piece_combo)  # add the pieces
#             all_combos.append(piece_combos_64)  # make list of lists
#         print(combo_counter)
#
#     # CREATE AND COMBINE ALL UNIQUE PERMUTATIONS OF ALL OF THE PIECE COMBOS
#     for piece_combo_64 in all_combos:  # for all combinations
#         board_permutations = permutations(piece_combo_64)
#         # CREATE A BOARD MATRIX (LIST OF LISTS) FOR EACH PERMUTATION
#         for board_perm in board_permutations:
#             board_matrix = [board_perm[i:i + 8] for i in range(0, 64, 8)]
#             z_hash = z_hash_board(board_matrix)
#             # MAP TO ZOBRIST HASH VALUE
#             HASH_TO_BOARD_MAP[z_hash] = board_matrix
#             print("Printing piece combos")
#             print(board_perm)
