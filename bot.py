import sys

from random import randint
from tron_connection import TronSocket

real_key = "OTBQJ1490395694310"
test_key = "VRIGL1490395747576"

secret = real_key

'''
Print the board
@param {double array} board_state: A matrix representing the state of the board
'''
def print_board(board_state):
  for row in board_state:
    for cell in row:
      print cell,
    print ""

'''
 Return the direction you want to move your bike in
 @param  {int} grid_size:            The length of one side of the square grid
 @param  {double array} board_state: A 2D matrix of ints representing the state of the board
 @param  {int} my_player_number:     The number which represens your player on the board
 @param  {int} total_player_count:   The amount of players in this gane
 @return {String}                    The move to be played ("UP", "DOWN", "LEFT", or "RIGHT")
'''
def select_move(grid_size, board_state, my_player_number, total_player_count):
    print_board(board_state) # Print board for debugging
    print ""

    self_num = my_player_number
    evil_num = (1 if self_num == 2 else 2)

    self_pos = get_position_of_player(grid_size, board_state, self_num)

    # Return "UP", "DOWN", "LEFT", or "RIGHT"
    relevant_moves = get_moves_that_dont_kill(board_state, grid_size, self_pos)
    eval_moves = [evaluate_position(x, board_state, grid_size) for x \
        in relevant_moves]
    eval_moves = [evaluate_position_by_openness(x, board_state, grid_size) \
        for x in eval_moves]

    print eval_moves

    if len(eval_moves) == 0:
        return 'UP'
    else:
        ans = max(eval_moves, key = lambda x:x[3])
        print ans
        return ans[0]

def get_moves_that_dont_kill(board_state, grid_size, user_position):
    position_user = user_position

    x = user_position[0]
    y = user_position[1]

    list_of_options = []

    if (user_position[0] + 1) < grid_size and board_state[x + 1][y] == '0':
        list_of_options.append(("DOWN", x + 1, y))

    if (user_position[0] - 1) >= 0 and board_state[x - 1][y] == '0':
        list_of_options.append(("UP", x - 1, y))

    if (user_position[1] - 1) >= 0 and board_state[x][y - 1] == '0':
        list_of_options.append(("LEFT", x, y - 1))

    if (user_position[1] + 1) < grid_size and board_state[x][y + 1] == '0':
        list_of_options.append(("RIGHT", x, y + 1))

    print list_of_options
    return list_of_options

def evaluate_position(position, board_state, grid_size):
    _eval = 0
    _eval += evaluate_by_safety(position, board_state, grid_size)
    _eval += evaluate_start(position, board_state, grid_size)
    _eval *= evaluate_by_nearness_center(position, board_state, grid_size)

    return (position[0], position[1], position[2], _eval)

def get_position_of_player(grid_size, board_state, player_number):
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            if board_state[i][j] == player_number:
                return (i, j)

def evaluate_by_nearness_center(position, board_state, grid_size):
    half = grid_size / 2

    _mult = 1

    if (abs(position[1] - half) < (.6 * grid_size)):
        _mult *= .8
    if (abs(position[2] - half) < (.6 * grid_size)):
        _mult *= .8

    return _mult

def evaluate_by_safety(position, board_state, grid_size):
    x = position[1]
    y = position[2]

    _eval = 0

    _min_dx = max(-3, -x + 1)
    _min_dy = max(-3, -y + 1)

    for dx in xrange(_min_dx, 4):
        for dy in xrange(_min_dy, 4):
            new_x = max(x + dx, 0)
            new_y = max(y + dy, 0)

            new_x = min(new_x, grid_size - 1)
            new_y = min(new_y, grid_size - 1)

            if board_state[new_x][new_y] == '0':
                _eval += 1

            if (y + dy) == grid_size:
                break

        if (x + dx) == grid_size:
            break

    return _eval

def evaluate_start(position, board_state, grid_size):
    if (position[0] == "UP" or position[0] == "DONE") and \
        (position[2] == grid_size - 1 or position[2] == 0):
        return 4
    else:
        return 0

def evaluate_position_by_openness(position, board_state, grid_size):
    _x = position[1]
    _y = position[2]
    _eval = position[3]

    ecchi = get_moves_that_dont_kill(board_state, grid_size, (_x, _y))

    mult = {
        0: 0.0,
        1: 0.2,
        2: 0.4,
        3: 0.6,
        4: 1.0
    }.get(len(ecchi))

    return (position[0], _x, _y, _eval * mult)


#DON'T TOUCH BELOW
if len(sys.argv) > 1:
    if sys.argv[1] == '--self':
        secret = real_key
    elif sys.argv[1] == '--other':
        secret = test_key
    else:
        print 'use self or other'
        sys.exit()

socket_connection = TronSocket(select_move, secret)
#DON'T TOUCH ABOVE
