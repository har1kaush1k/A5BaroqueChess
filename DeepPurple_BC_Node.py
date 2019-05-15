class Node:

    def __init__(self, board,
                 z_hash=None,
                 predecessor=None,
                 score=None,
                 move=((None, None), (None, None)),
                 whose_move=1,
                 witty_responce="uh... give me a second...",
                 debug_id=0):  # BLACK == 0, WHITE == 1

        self.board = board        # Type: Board[y][x]
        self.zobrist_hash = z_hash     # Type: Zobrist hash
        self.predecessor = predecessor  # Type: Node
        self.score = score              # Type: Int
        self.move = move                # Type:((from_y, from_x), (to_y, to_x))
        self.whose_move = whose_move    # Type: Int (0=Black, 1=White)
        self.remark = witty_responce    # Type: String
        self.ID = debug_id              # TODO: FOR DEBUG ONLY

    def __eq__(self, other):
        if not (type(other) == type(self)):
            return False
        if not (self.score == other.score):
            return False
        if not (self.move == other.move):
            return False
        return True

    # TODO Maybe use Zobrist hashing here?
    # Hash depends on current board state + predecessor board state + move
    def __hash__(self):
        if self.predecessor is None:
            predecessor_hash = 445832
        else:
            predecessor_hash = self.board.__repr__().__hash__()

        return ((self.board.__repr__().__hash__() ** 2) +
                predecessor_hash ** 2 +
                self.move.__hash__())
