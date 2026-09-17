import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # x goes first, if x just went then o, then x again untill winner,lose,draw (result)
    x_count = 0
    o_count = 0

    for rows in board:
        x_count += rows.count(X)
        o_count += rows.count(O)

    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    coordinates = []
    items = []
    actions = set()
# get coordinates
    # get index for rows index_1, then get index for item within rows index_2, then append them as tupple to coordinates list
    for index_1 in range(len(board)):
        for index_2 in range(len(board[index_1])):
            coordinates.append(((index_1, index_2)))
# get items within rows
    # for X, O or EMPTY in rows taken from the board state, append it to items
    for rows in board:
        for obj in rows:
            items.append(obj)
# get coordinates for items containing empty
    # gets the iteration of coordinates which contain and EMPTY placement
    for item_index in range(len(items)):
        if items[item_index] is EMPTY:
            actions.add(coordinates[item_index])
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    possibilities = actions(board)
    if action not in possibilities:
        raise Exception("Action not valid")

    new_board = copy.deepcopy(board)

    i, j = action

    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # define case for winners
    # case 1 any row all 3
    # case 2 any column all 3
    # case 3 any diagonal all 3
    # return one of the winner chips to say that is the winner if XXX then X is winner
    # check for tie or not ended to return None

    # 3 in a row winner
    for row in board:
        if row[0] is not None and row[0] is row[1] is row[2]:
            return row[0]
    # 3 in a column winner
    for index in range(3):
        if board[0][index] is not None and board[0][index] is board[1][index] is board[2][index]:
            return board[0][index]

    # 3 in a diag winner
    if board[0][0] is not None and board[0][0] is board[1][1] is board[2][2]:
        return board[0][0]
    elif board[2][0] is not None and board[2][0] is board[1][1] is board[0][2]:
        return board[2][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game is over if there is a winner.
    if winner(board) is not None:
        return True

    # check if there are any empty cells, in which case the game is not over.. so return false
    for row in board:
        if EMPTY in row:
            return False

    # return true is all cells is taken up and there is no winner cause the game is still over
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is not None:
        # enter conditional for -1 and 1
        if winner(board) is X:
            return 1
        else:
            return -1
    # conditional for tie
    else:
        return 0


def max_value(board):
    v = float('-inf')

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    v = float('inf')

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) is X:
        best_value = float('-inf')
        best_move = None

        for action in actions(board):
            value = min_value(result(board, action))

            if value > best_value:
                best_value = value
                best_move = action

        return best_move

    else:
        best_value = float('inf')
        best_move = None

        for action in actions(board):
            value = max_value(result(board, action))

            if value < best_value:
                best_value = value
                best_move = action

        return best_move
