import sys
import heapq

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

def get_neighbors(state, grid):
    neighbors = []
    r, c = state.pos
    rows, cols = len(grid), len(grid[0])

    # vacuum curr cell if dirty
    if (r, c) in state.dirty:
        new_dirt = set(state.dirty)
        new_dirt.remove((r, c))
        neighbors.append(VacuumState((r, c), new_dirt, state.path + ['V'], state.cost + 1))

    # try to move in each dir
    for action, (dr, dc) in MOVES.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            neighbors.append(VacuumState((nr, nc), state.dirty, state.path + [action], state.cost + 1))

    return neighbors

def depth_first_search(start_state, grid):
    stack = [start_state]
    visited = set()
    nodes_generated = 0
    nodes_expanded = 0

    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1
        if state.is_goal():
            return state.path, nodes_generated, nodes_expanded
        neighbors = get_neighbors(state, grid)
        nodes_generated += len(neighbors)
        stack.extend(neighbors)

    return None, nodes_generated, nodes_expanded