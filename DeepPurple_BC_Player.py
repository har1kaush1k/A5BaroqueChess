"""DeepPurple_BC_Player.py
 by Isaac Boger and Eddy Liang
 iboger@uw.edu, eddylzx@uw.edu
 Version 1.0, May 03, 2019.
 Assignment 5, in CSE 415, Spring 2019.

This file Includes a basic structure for the agent by
 S. Tanimoto, Univ. of Washington.
Paul G. Allen School of Computer Science and Engineering

Intended USAGE:
 TODO: Add useage

 TODO: add file description
"""
import time
import BC_state_etc as bC
from DeepPurple_BC_Node import Node
import DeepPurple_BC_ZHash as zHash
import DeepPurple_BC_Rules as Rules


# TODO: Comment describing what these are for
""" """
TAKE = 0
CHECK = 1
CHECKMATE = 2

""" the time remaining in number of minutes at which the agent should abort 
its current search and return the last computed best move to avoid going over 
the time limit """
TIME_CRITICAL = 1

""" A global variable which stores the opposing team's nickname"""
opposing_team_nickname = ""

""" 
Each Key is StateParam
Each value is list of successors (Each element is an instance of StateParams)
"""
node_map = {}


"""
Parameterized Minimax Data
"""
N_STATES_EXPANDED = 0
N_STATIC_EVALS = 0
N_CUTOFFS = 0
CURRENT_STATE_STATIC_VAL = 0


""" 
Stores the initial positions of the  pieces
"""
INITIAL_POSITIONS = {}

""" 
Black White Toggle
"""
our_color = 1

""" Default setting is for zobrist hashing on"""
use_zobrist_hashing = True

""" Default setting is for alpha-beta pruning on"""
use_alpha_beta_pruning = True

""" Default setting is for basic static evals is off"""
use_basic_static_eval = False

""" Start time: System time (in seconds )at which makeMove is called
    Time limit: Time (in seconds) after start time makeMove must make a decision by"""
START_TIME = None
TIME_LIMIT = None

""" IF TREE TRAVERSAL WAS INCOMPLETE """
INCOMPLETE_TRAVERSAL = False


def prepare(player_two_nickname="DumbBot4000", play_white=True):
    """ Here the game master will give your agent the nickname of
    the opponent agent, in case your agent can use it in some of
    the dialog responses.  Other than that, this function can be
    used for initializing data structures, if needed."""
    global opposing_team_nickname, our_color
    opposing_team_nickname = player_two_nickname
    our_color = play_white
    # Find initial board positions
    find_initial_positions()

    if use_zobrist_hashing:
        zHash.prepare_z_hash()


def parameterized_minimax(current_state, alpha_beta=False, ply=3,
                          basic_static_eval=True, zobrist_hashing=False):

    global node_map, \
        N_STATES_EXPANDED, \
        N_STATIC_EVALS, \
        N_CUTOFFS, \
        CURRENT_STATE_STATIC_VAL, \
        use_zobrist_hashing, \
        use_alpha_beta_pruning, \
        use_basic_static_eval

    use_zobrist_hashing = zobrist_hashing
    use_alpha_beta_pruning = alpha_beta
    use_basic_static_eval = basic_static_eval

    """ The return value of parameterized_minimax should be a dict object with 
        the following attributes:

    'CURRENT_STATE_STATIC_VAL': The static eval value of the current_state as
                                    determined by your minimax search
    'N_STATES_EXPANDED'       : The number of states expanded as part of your 
                                    minimax search
    'N_STATIC_EVALS'          : The number of static evals performed as part of 
                                    minimax
                                search (0 if alpha-beta was not enabled)
    """
    root_board = current_state.board
    # Root state
    root_node = Node(root_board, zHash.z_hash_board(root_board))

    # Build tree to ply depth with no time limit
    build_tree(root_node,               # current root node
               ply,                     # target depth for leaf nodes
               0,                       # current depth
               float('inf'))            # time left before timeout

    # Minimax
    minimax(root_node,                  # current root node
            ply,                        # target depth for leaf nodes
            0,                          # current depth
            True,                       # whether the current node is a max node
            -float("inf"),              # alpha value
            float("inf"),               # beta value
            False)                      # ab pruning (T/F)

    # Numbers to return in a dict
    minimax_params = {'CURRENT_STATE_STATIC_VAL': root_node.score,
                      'N_STATES_EXPANDED': N_STATES_EXPANDED,
                      'N_STATIC_EVALS': N_STATIC_EVALS, 'N_CUTOFFS': N_CUTOFFS}

    # Reset Graph and counts
    node_map.clear()
    N_STATES_EXPANDED = 0
    N_STATIC_EVALS = 0
    N_CUTOFFS = 0

    return minimax_params


#  Returns time left in seconds
def time_elapsed():
    global START_TIME
    return time.time() - START_TIME


def introduce():
    return "I'm sure you've heard of my older brother, DeepBlue. I may not be" \
           " good at chess like he is, but but what I lack in skill I make " \
           "up for in witty one-liners! I'm thinking of a good one... " \
           "give me a second... just you wait... it's going to be good..."


def nickname():
    return "DeepPurple"


def basicStaticEval(current_board):
    """Use the simple method for state evaluation described in the spec.
    This is typically used in parameterized_minimax calls to verify
    that minimax and alpha-beta pruning work correctly.
    """
    total_score = 0
    for y in range(8):
        for x in range(8):
            piece = current_board[y][x]
            if piece != 0:
                if piece is bC.WHITE_PINCER:
                    total_score += 1
                elif piece is bC.WHITE_KING:
                    total_score += 100
                elif piece is bC.BLACK_PINCER:
                    total_score -= 1
                elif piece is bC.BLACK_KING:
                    total_score -= 100
                elif piece % 2 == 0:
                    total_score += 2
                elif piece % 2 == 1:
                    total_score -= 2
    if total_score is None:
        raise Exception("SCORING ERROR: Total_score is None!")
    else:
        return total_score


def staticEval(current_board):
    """Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games."""
    if use_basic_static_eval:
        return basicStaticEval(current_board)
    else:
        global our_color
        total_score = 0
        white_king_is_dead = (Rules.where_is_the_king(current_board, bC.WHITE)
                              is None)
        black_king_is_dead = (Rules.where_is_the_king(current_board, bC.BLACK)
                              is None)
        for y in range(8):
            for x in range(8):
                piece = current_board[y][x]
                if piece != 0 and piece != 1:  # Piece should never be 1 anyway
                    if piece is bC.WHITE_PINCER:
                        total_score += 40
                        total_score += enemy_count(current_board, (y, x, piece)) * 10
                    elif piece is bC.BLACK_PINCER:
                        total_score -= 40
                        total_score -= enemy_count(current_board, (y, x, piece)) * 10

                    elif piece is bC.WHITE_KING:
                        total_score += 10000
                        total_score += enemy_count(current_board, (y, x, piece)) * -50
                    elif piece is bC.BLACK_KING:
                        total_score -= 10000
                        total_score -= enemy_count(current_board, (y, x, piece)) * 50

                    elif piece is bC.WHITE_COORDINATOR:
                        total_score += 5
                        total_score += enemy_count(current_board, (y, x, piece)) * -10
                    elif piece is bC.BLACK_COORDINATOR:
                        total_score -= 5
                        total_score -= enemy_count(current_board, (y, x, piece)) * 10

                    elif piece is bC.WHITE_LEAPER:
                        total_score += 35
                        total_score += enemy_count(current_board, (y, x, piece)) * -5
                    elif piece is bC.BLACK_LEAPER:
                        total_score -= 35
                        total_score -= enemy_count(current_board, (y, x, piece)) * 5

                    elif piece is bC.WHITE_IMITATOR:
                        total_score += 20
                        total_score += enemy_count(current_board, (y, x, piece)) * 20
                    elif piece is bC.BLACK_IMITATOR:
                        total_score -= 20
                        total_score -= enemy_count(current_board, (y, x, piece)) * 20

                    elif piece is bC.WHITE_WITHDRAWER:
                        total_score += 25
                        total_score += enemy_count(current_board, (y, x, piece)) * 30
                    elif piece is bC.BLACK_WITHDRAWER:
                        total_score -= 25
                        total_score -= enemy_count(current_board, (y, x, piece)) * 30

                    elif piece is bC.WHITE_FREEZER:
                        total_score += 15
                        total_score += enemy_count(current_board, (y, x, piece)) * 50
                    elif piece is bC.BLACK_FREEZER:
                        total_score -= 15
                        total_score -= enemy_count(current_board, (y, x, piece)) * 50

                    if Rules.is_white(piece):
                        if not black_king_is_dead and piece != bC.WHITE_KING:
                            prox_to_king = Rules.proximity_to_king(
                                current_board, (y, x), bC.BLACK)
                            total_score += (1.0 / prox_to_king) * 10
                    else:
                        if not white_king_is_dead and piece != bC.BLACK_KING:
                            prox_to_king = Rules.proximity_to_king(
                                current_board, (y, x), bC.WHITE)
                            total_score += (1.0 / prox_to_king) * 10

        total_score += development_scores(current_board) * 100

        if total_score is None:
            raise Exception("SCORING ERROR: Total_score is None!")
        else:
            return total_score


def enemy_count(board, piece_pos):
    """ Checks for the number of enemies next to the current piece """
    enemy_count = 0
    y = piece_pos[0]
    x = piece_pos[1]
    piece = board[y][x]
    # Check East
    if Rules.is_coordinate_in_board(y, x + 1):
        if Rules.is_enemy((x, y, piece), (y, x + 1, board[y][x + 1])):
            enemy_count += 1

    # Check Northeast
    if Rules.is_coordinate_in_board(y + 1, x + 1):
        if Rules.is_enemy((x, y, piece), (y + 1, x + 1, board[y + 1][x + 1])):
            enemy_count += 1

    # Check North
    if Rules.is_coordinate_in_board(y + 1, x):
        if Rules.is_enemy((x, y, piece), (y + 1, x, board[y + 1][x])):
            enemy_count += 1

    # Check Northwest
    if Rules.is_coordinate_in_board(y + 1, x - 1):
        if Rules.is_enemy((x, y, piece), (y + 1, x - 1, board[y + 1][x - 1])):
            enemy_count += 1

    # Check West
    if Rules.is_coordinate_in_board(y, x - 1):
        if Rules.is_enemy((x, y, piece), (y, x - 1, board[y][x - 1])):
            enemy_count += 1

    # Check Southwest
    if Rules.is_coordinate_in_board(y - 1, x - 1):
        if Rules.is_enemy((x, y, piece), (y - 1, x - 1, board[y - 1][x - 1])):
            enemy_count += 1

    # Check South
    if Rules.is_coordinate_in_board(y - 1, x):
        if Rules.is_enemy((x, y, piece), (y - 1, x, board[y - 1][x])):
            enemy_count += 1

    # Check Southeast
    if Rules.is_coordinate_in_board(y - 1, x + 1):
        if Rules.is_enemy((x, y, piece), (y - 1, x + 1, board[y - 1][x + 1])):
            enemy_count += 1

    return enemy_count


def find_initial_positions():
    """
    Populates the INITIAL_POSITIONS map with each piece's position
    (in (y,x) tuples) except the pincers, which are just defined by their rows.
    """
    global INITIAL_POSITIONS
    current_board = bC.INITIAL
    for y in range(8):
        for x in range(8):
            piece = current_board[y][x]
            if piece != 0 and piece != 2 and piece != 3:
                INITIAL_POSITIONS[piece] = (y, x)


def development_scores(current_board):
    """
    Returns the difference in board development for both colors
    :param current_board: contains board
    :return: POSITIVE score for more white development, negative score for more
             black development
    """
    development_count = 0
    for y in range(8):
        for x in range(8):
            piece = current_board[y][x]
            if Rules.is_piece(piece):
                if piece == Rules.WHITE_PINCER:
                    if y < 6:
                        development_count += 4

                elif piece == Rules.BLACK_PINCER:
                    if y > 1:
                        development_count -= 4

                elif piece in (Rules.WHITE_FREEZER, Rules.WHITE_WITHDRAWER,
                               Rules.WHITE_IMITATOR, Rules.WHITE_KING,
                               Rules.WHITE_COORDINATOR, Rules.WHITE_LEAPER):
                    if y < 7:
                        development_count += 5
                elif piece in (Rules.BLACK_FREEZER, Rules.BLACK_WITHDRAWER,
                               Rules.BLACK_IMITATOR, Rules.BLACK_KING,
                               Rules.BLACK_COORDINATOR, Rules.BLACK_LEAPER):
                    if y > 0:
                        development_count -= 5

    return development_count


def makeMove(current_state, current_remark, time_limit=10):
    global node_map, START_TIME, TIME_LIMIT, our_color, INCOMPLETE_TRAVERSAL
    curr_board = current_state.board
    START_TIME = time.time()                # Start timer
    TIME_LIMIT = time_limit                 # the time limit for our move
    whose_move = current_state.whose_move    # we will only be passed our turn

    if use_zobrist_hashing:
        root_z_hash = zHash.z_hash_board(curr_board)
        zHash.HASH_TO_BOARD_MAP[root_z_hash] = curr_board
    else:
        root_z_hash = None

    # Root state
    # self.zobrist_hash = zobrist  # Type: Zobrist hash
    # self.BC_state = bc_state  # Type: BC_state
    # self.predecessor = predecessor  # Type: StateParams
    # self.score = score  # Type: Int
    # self.move = move  # Type:(From Pos, To Pos, Action)
    # self.whose_move = whose_move
    root_node = Node(curr_board,
                     root_z_hash,
                     None,
                     None,
                     None,
                     whose_move)

    # Initialize Optimal Successor
    best_successor = Node(curr_board,
                          None,
                          None,
                          -float('inf'),
                          ((None, None), (None, None)),
                          whose_move)

    latest_best_successor_list = []

    iddfs_depth = 0  # IDDFS starting search depth

    # node_map[root_node] = []

    # Tree building/pruning
    while time_elapsed() < TIME_LIMIT * 9.0/10:

        INCOMPLETE_TRAVERSAL = False

        # INCOMPLETE_TRAVERSAL = False
        node_map.clear()
        node_map[root_node] = []

        # Build tree to a depth of iddfs_depth
        # whose_turn:
        #       0 = your turn
        #       1 = opponent turn
        build_tree(root_node, iddfs_depth, 0, False)
        # print("Time elapsed at end of build tree: " + str(time_elapsed()))

        if not INCOMPLETE_TRAVERSAL:
            # Minimax + AB Pruning
            minimax(root_node,
                    iddfs_depth,
                    0,
                    whose_move,
                    -float("inf"),
                    float("inf"),
                    True)

        #  Get current best successor at the end of current IDDFS depth
        node_successors = node_map[root_node]

        if not INCOMPLETE_TRAVERSAL:
            # print("Complete traversal at DEPTH: " + str(iddfs_depth) +
            # ", getting new best successor.")
            # IF CURR TURN IS BLACK: Choose most negative
            if whose_move == bC.BLACK:
                best_score = float('inf')
                for each_successor in node_successors:
                    if each_successor.score is not None:
                        successor_score = each_successor.score
                        if successor_score < best_score:
                            best_successor = each_successor
                            best_score = successor_score

            # IF CURR TURN IS WHITE: Choose most positive
            else:
                best_score = -float('inf')
                for each_successor in node_successors:
                    if each_successor.score is not None:
                        successor_score = each_successor.score
                        if successor_score > best_score:
                            best_successor = each_successor
                            best_score = successor_score
            latest_best_successor_list = node_successors

            iddfs_depth += 1

    # print("Root node score is: " + str(root_node.score))
    # print("Best Successor Score Test: " + str(best_successor.score))
    # i = 0
    # for each_node in latest_best_successor_list:
    #     print("Last good successor score " + str(i) +
    #     ": " + str(each_node.score))
    #     i += 1
    # print("")

    # move =((6,4),(3,4))
    move = best_successor.move
    # print("Best move is: " + str(move))
    new_board = best_successor.board
    new_state = bC.BC_state(new_board, best_successor.whose_move)
    print(new_state.__repr__())

    # Make up a new remark
    new_remark = best_successor.remark
    print(new_remark)
    print("Number of states expanded: " + str(N_STATES_EXPANDED))
    print("Time elapsed             : " + str(time_elapsed()))

    return [[move, new_state], new_remark]


def build_tree(current_node, iddfs_depth, curr_depth, basic_static_eval):
    """ Tree Building
    curr_state_params: current root node
    iddfs_depth      : target depth for leaf nodes
    curr_depth       : current depth
    time_left        : time left before timeout
    """
    global N_STATIC_EVALS, TIME_LIMIT, INCOMPLETE_TRAVERSAL
    # print("Current depth: " + str(curr_depth))
    # print("IDDFS target : " + str(iddfs_depth))

    # At leaf node, calculate node value with StaticEval
    if curr_depth == iddfs_depth:
        return

    #  List of all successor StateParams
    successor_nodes = Rules.generate_successors(current_node,
                                                use_zobrist_hashing)

    # Update Nodes graph
    node_map[current_node] = successor_nodes

    for each_successor in successor_nodes:
        if time_elapsed() >= TIME_LIMIT / 2:    # Time check
            # print("Time out at build tree 1")
            INCOMPLETE_TRAVERSAL = True
            return

        build_tree(each_successor,
                   iddfs_depth,
                   curr_depth + 1,
                   basic_static_eval)


def minimax(curr_node,          # current root node
            iddfs_depth,        # target depth for leaf nodes
            curr_depth,         # current depth of recursion
            is_max_player,      # whether the current node is a max node
            alpha, beta,        # alpha value, beta value
            ab_pruning=True):
    """ AB Pruning/Minimax"""
    global N_STATES_EXPANDED, N_CUTOFFS, TIME_LIMIT
    global INCOMPLETE_TRAVERSAL, N_STATIC_EVALS
    board = curr_node.board
    N_STATES_EXPANDED += 1
    #  print("Current depth is: " + str(curr_depth))

    if time_elapsed() >= TIME_LIMIT * 9.0/10:  # Time check
        print("Time out at minimax 1")
        INCOMPLETE_TRAVERSAL = True
        print("Broken traversal: " + str(INCOMPLETE_TRAVERSAL))
        return

    if curr_depth == iddfs_depth:       # depth check
        board_zhashed = curr_node.zobrist_hash in zHash.HASH_TO_SCORE_MAP
        if use_zobrist_hashing and board_zhashed:
            state_score = zHash.HASH_TO_SCORE_MAP[curr_node.zobrist_hash]
        else:
            state_score = staticEval(board)

            zHash.HASH_TO_SCORE_MAP[curr_node.zobrist_hash] = state_score
            # print(current_node.BC_state.__repr__())
            # print("Board Score: " + str(state_score))
            # print("---------------------------------")
            # print("")
        curr_node.score = state_score
        best_val = curr_node.score
    else:
        if is_max_player:  # If current node is a max node
            best_val = -float('inf')
        else:  # If current node is a min node
            best_val = float('inf')

        for each_child in node_map[curr_node]:

            value = minimax(each_child,
                            iddfs_depth,
                            curr_depth + 1,
                            not is_max_player,
                            alpha,
                            beta)

            if time_elapsed() >= TIME_LIMIT * 9.0/10:  # Time check
                print("Time out at minimax 2")
                INCOMPLETE_TRAVERSAL = True
                print("Broken traversal: " + str(INCOMPLETE_TRAVERSAL))
                return

            # print("best_val= %f" % best_val)
            # print("value= %f" % value)
            if value is None:
                raise Exception('MINIMAX ERROR: Value is None!')
            elif best_val is None:
                raise Exception('MINIMAX ERROR: best_value is None!')

            if is_max_player:
                best_val = max(best_val, value)
                alpha = max(alpha, best_val)
            else:
                best_val = min(best_val, value)
                beta = min(beta, best_val)

            curr_node.score = best_val
            if ab_pruning:
                if beta <= alpha:
                    N_CUTOFFS += 1
                    # print("MAX/MIN PRUNED")
                    # print("Cut off count: " + str(N_CUTOFFS))
                    break
    if best_val is None:
        raise Exception('MINIMAX ERROR: best_value is None!')
    else:
        return best_val
