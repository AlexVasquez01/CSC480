# N, S, E, W
MOVES = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1)
}

class VacuumState:
    def __init__(self, pos, dirty, path=None, cost=0):
        self.pos = pos
        self.dirty = frozenset(dirty)
        self.path = path or []
        self.cost = cost

    def is_goal(self):
        return len(self.dirty) == 0

    def __hash__(self):
        return hash((self.pos, self.dirty))

    def __eq__(self, other):
        return self.pos == other.pos and self.dirty == other.dirty

    def __lt__(self, other):
        return self.cost < other.cost 

def read_world(filename):
    with open(filename, 'r') as f:
        cols = int(f.readline())
        rows = int(f.readline())
        grid = [list(f.readline().strip()) for _ in range(rows)]

    start = None
    dirty = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                start = (r, c)
            elif grid[r][c] == '*':
                dirty.add((r, c))

    return grid, start, dirty