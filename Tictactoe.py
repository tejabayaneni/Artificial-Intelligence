from math import inf as infinity
from random import choice

AgentX = +1
AgentO = -1
Xchoice = 'X'
Ochoice = 'O'
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
def evaluate(state):
    if wins(state, AgentX):
        score = +1
    elif wins(state, AgentO):
        score = -1
    else:
        score = 0
    return score

def wins(state, player):
    win_state = [(0,1,2), (3,4,5), (6,7,8), (0,3,6),(1,4,7),(2,5,8), (0,4,8), (2,4,6)]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def game_over(state):
    return wins(state, AgentO) or wins(state, AgentX)
def empty_cells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0: cells.append([x, y])
    return cells

def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False
def minimax(state, depth, player):
    if player == AgentX:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y
        if player == AgentX:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value
    return best
def render(state, Xchoice, Ochoice):
    print('')
    for row in state:
        for cell in row:
            if cell == +1:
                print(Xchoice, end='')
            elif cell == -1:
                print(Ochoice, end='')
            else:
                print('*', end='')
        print('')
def ai_turn(Xchoice, Ochoice, XorO):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, XorO)
        x, y = move[0], move[1]
    set_move(x, y, XorO)
    render(board, Xchoice, Ochoice)
def start():

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        ai_turn(Xchoice, Ochoice, AgentX)
        ai_turn(Xchoice, Ochoice, AgentO)

    # Game over message
    print('')
    if wins(board, AgentO):
        print('Result: O Wins!')
    elif wins(board, AgentX):
        print('Result: X Wins!')
    else:
        print('Result: Draw Game')
if __name__ == "__main__":
	start()
