#The following variable must be used in the You can change the location values for testing purposes
stoneLocation=[2, 8]  #[row, column]
positiveTerminalLocation = [0,10,2]  #[row, column, utility value]
nagativeTerminalLocation = [1,10, -2]  #[row, column, utility value]
iteration=20
noise=0.15
discount=0.91
import random
import itertools
from operator import itemgetter
INITIAL_STATE = (0,0)
ACTIONS = ['North', 'South', 'East', 'West', 'End']
r1,c1,v1 =positiveTerminalLocation
r2,c2,v2 =nagativeTerminalLocation
postiveT=(r1,c1)

nagativeT=(r2,c2)
def move_able(s, dx, dy):

    if s=="DEAD" or s in [postiveT, nagativeT]: return False
    x, y = s
    if x+dx < 0 or x+dx > 10:
        return False
    if y+dy < 0 or y+dy > 10:
        return False
    if [x+dx, y+dy] in stoneLocation:
        return False
    return True

def move(s, dx, dy):
    x, y = s
    return (x+dx, y+dy)

normal = 0.75

class motion:
    def __init__(self, name, permiss, state_move):
        self.name=name
        self.permiss=permiss
        self.state_move=state_move
    def is_able(self,a):
        return self.permiss(a)
    def apply (self,a):
        return self.state_move(a)
Nmo=motion("North",
           lambda a: move_able(a,0,1),
           lambda a: move(a, 0,1))
Smo=motion("South",
           lambda a: move_able(a,0,-1),
           lambda a: move(a, 0,-1))
Wmo=motion("Weat",
           lambda a: move_able(a,-1,0),
           lambda a: move(a, -1,0))
Emo=motion("East",
           lambda a: move_able(a,1,0),
           lambda a: move(a, 1,0))
Endmo=motion("DEAD",
             lambda a: a==postiveT or a==nagativeT,
             lambda a: "DEAD")
OPERATORS = [Nmo, Smo, Wmo, Emo, Endmo]
ActionOps = {'North': [Nmo, Wmo, Emo],
             'South': [Smo, Emo, Wmo],
             'East':  [Emo, Smo, Nmo],
             'West':  [Wmo, Nmo, Smo]}


def Transition(s, a, sp):
    if s == "DEAD": return 0
    if sp == "DEAD":
        if s == postiveT or s == nagativeT:
            return 1
        else:
            return 0
    if a == "End" and s == sp:
        return 0
    if s == postiveT or s == nagativeT and a != "End": return 0
    sx, sy = s
    spx, spy = sp
    if sx == spx and sy == spy - 1:
        if a == "North":
            return normal
        if a == "East" or a == "West":
            return noise
    if sx == spx and sy == spy + 1:
        if a == "South":
            return normal
        if a == "East" or a == "West":
            return noise
    if sx == spx - 1 and sy == spy:
        if a == "East":
            return normal
        if a == "North" or a == "South":
            return noise
    if sx == spx + 1 and sy == spy:
        if a == "West":
            return normal
        if a == "North" or a == "South":
            return noise
    if s == sp:
        ops = ActionOps[a]
        prob = 0.0
        if not ops[0].is_able(s): prob += normal
        if not ops[1].is_able(s): prob += noise
        if not ops[2].is_able(s): prob += noise
        return prob
    return 0.0


def Score(s, a, sp):
    if s == 'DEAD': return 0
    if s == postiveT:
        return 1.0
    if s == nagativeT: return -1.0
    return 0.0


class Grid:
    def __init__(self):
        self.noise = noise
        self.kstate = set()
        self.hash = {}

    def begin(self):
        self.start_state = INITIAL_STATE
        self.kstate.add(INITIAL_STATE)
        self.actions = ACTIONS
        self.operators = OPERATORS
        self.transitions = Transition
        self.score = Score

    def state_neighbors(self, state):
        neighbors = self.hash.get(state, False)
        if neighbors == False:
            neighbors = [op.apply(state) for op in self.operators if op.is_able(state)]
            self.hash[state] = neighbors
            self.kstate.update(neighbors)
        return neighbors

    def generate(self):

        unex = []
        unex += self.kstate

        while unex:
            S = unex[0]
            del unex[0]
            self.kstate.add(S)
            current_known = set()
            current_known.update(self.kstate)

            neighbors = self.state_neighbors(S)
            for neighbor in neighbors:

                if not (neighbor in unex) and not (neighbor in current_known):
                    unex.append(neighbor)
            self.kstate.update(current_known)

    def valueIteration(self, discount, iterations):
        self.generate()
        self.V = {s: 0 for s in self.kstate}
        new_V = {}

        for i in range(iterations):
            new_V = {}

            if i == 10:
                print("Number of 10 interation:")

                print(Print_function(self.V))

            for s in self.V:

                max_q = -10

                neighbors = []
                neighbors += self.state_neighbors(s);

                neighbors.append(s)

                for a in self.actions:
                    q = 0
                    for sp in neighbors:
                        probability = self.transitions(s, a, sp)

                        if probability == 0:
                            continue
                        reward = self.score(s, a, sp)

                        sp_val = probability * (reward + (discount * self.V[sp]))
                        q += sp_val

                    max_q = max(q, max_q)

                new_V[s] = max_q

            self.V = {}
            self.V = new_V


def Print_function(V_dict):
    t = {}
    t.update(V_dict)
    del t["DEAD"]

    grid = []
    s = "["
    rowl = []

    for i in range(11):
        for j in range(11):
            rowl.append(s)

        grid.append(rowl)
        rowl = []

    for state in t:
        row = state[1]
        col = state[0]
        val = "%.2f" % t[state]
        grid[row][col] += val

    grid[2][8] = "[STONE"
    s = ""
    for row in grid:
        for val in row:
            s += val + "]\t"

        s += "\n\n"

    return s


def start():
    g = Grid()
    g.begin()
    g.valueIteration(0.9, 30)
    print(len(g.V))
    print("Follow the sampel:")
    print(g.V)
    print("Number of 30 interation:")
    print(Print_function(g.V))