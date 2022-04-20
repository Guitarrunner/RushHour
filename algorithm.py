import sys
from collections import deque
from cars import Cars

redCar = Cars('X', 4, 2, 'H', True)

class RushHour(object):

    def __init__(self, vehicles, depth = 0, hvalue = 0):
        self.vehicles = vehicles
        self.depth = depth
        self.hvalue = hvalue
        self.lastmove=""

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.vehicles == other.vehicles

    def __cmp__(self, b):
        if self.hvalue+self.depth==b.hvalue+b.depth:
            return 0
        else:
            if self.depth + self.hvalue>b.depth+ b.hvalue:
                return 1
            return -1

    def __lt__(self, other):
            return self.depth + self.hvalue < other.depth + other.hvalue

    def __gt__(self, other):
        return self.depth + self.hvalue > other.depth + other.hvalue

    def __ne__(self, other):
        return not self.__eq__(other)    

    def __repr__(self):
        s = '-' * 8 + '\n'
        for line in self.get_board():
            s += '|{0}|\n'.format(''.join(line))
        s += '-' * 8 + '\n'
        return s

    def get_board(self):
        board = [[' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' ']]
        for vehicle in self.vehicles:
            x, y = vehicle.x, vehicle.y
            if vehicle.orientation == 'H':
                for i in range(vehicle.length):
                    board[y][x+i] = vehicle.id
            else:
                for i in range(vehicle.length):
                    board[y+i][x] = vehicle.id
        return board

    def solved(self):
        return redCar in self.vehicles

    def moves(self):
        board = self.get_board()
        for v in self.vehicles:
            if v.orientation == 'H':
                if v.x - 1 >= 0 and board[v.y][v.x - 1] == ' ':
                    new_v = Cars(v.id, v.x - 1, v.y, v.orientation, True)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    
                    f1 = RushHour(new_vehicles)
                    f1.lastmove=new_v.id+"L"
                    yield f1
                if v.x + v.length <= 5 and board[v.y][v.x + v.length] == ' ':
                    new_v = Cars(v.id, v.x + 1, v.y, v.orientation, True)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    
                    f1 = RushHour(new_vehicles)
                    f1.lastmove=new_v.id+"R"
                    yield f1
            else:
                if v.y - 1 >= 0 and board[v.y - 1][v.x] == ' ':
                    new_v = Cars(v.id, v.x, v.y - 1, v.orientation, True)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    
                    f1 = RushHour(new_vehicles)
                    f1.lastmove=new_v.id+"U"
                    yield f1
                if v.y + v.length <= 5 and board[v.y + v.length][v.x] == ' ':
                    new_v = Cars(v.id, v.x, v.y + 1, v.orientation, True)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(v)
                    new_vehicles.add(new_v)
                    
                    f1 = RushHour(new_vehicles)
                    f1.lastmove=new_v.id+"D"
                    yield f1

    def getTragetVehicle(self):
        for v in self.vehicles:
            if v.id =='X':
                return v
        return None

def load_file(rushhour_file):
    vehicles = []
    for line in rushhour_file:
        line = line[:-1] if line.endswith('\n') else line
        id, x, y, orientation = line
        vehicles.append(Cars(id, int(x), int(y), orientation, True))
    return RushHour(set(vehicles))

def breadth_first_search(r, max_depth=25):
    visited = set()
    solutions = list()
    depth_states = dict()

    queue = deque()
    queue.appendleft((r, tuple()))
    while len(queue) != 0:
        board, path = queue.pop()
        new_path = path + tuple([board])

        depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1

        if len(new_path) >= max_depth:
            break

        if board in visited:
            continue
        else:
            visited.add(board)

        if board.solved():
            solutions.append(new_path)
        else:
            queue.extendleft((move, new_path) for move in board.moves())

    return {'visited': visited,
            'solutions': solutions,
            'depth_states': depth_states}

def solution_steps(solution):
    steps = []
    for i in range(len(solution) - 1):
        r1, r2 = solution[i], solution[i+1]
        v1 = list(r1.vehicles - r2.vehicles)[0]
        v2 = list(r2.vehicles - r1.vehicles)[0]
        if v1.x < v2.x:
            steps.append('{0}R'.format(v1.id))
        elif v1.x > v2.x:
            steps.append('{0}L'.format(v1.id))
        elif v1.y < v2.y:
            steps.append('{0}D'.format(v1.id))
        elif v1.y > v2.y:
            steps.append('{0}U'.format(v1.id))
    return steps
