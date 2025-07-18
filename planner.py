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

def uniform_cost_search(start_state, grid):
    frontier = []
    heapq.heappush(frontier, (0, start_state))
    visited = {}

    nodes_generated = 0
    nodes_expanded = 0

    while frontier:
        cost, state = heapq.heappop(frontier)
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost
        nodes_expanded += 1
        if state.is_goal():
            return state.path, nodes_generated, nodes_expanded
        neighbors = get_neighbors(state, grid)
        nodes_generated += len(neighbors)
        for neighbor in neighbors:
            heapq.heappush(frontier, (neighbor.cost, neighbor))

    return None, nodes_generated, nodes_expanded

def main():
    if len(sys.argv) != 3:
        print("Wrong format: python3 planner.py [uniform-cost|depth-first] [world-file]")
        return

    algorithm = sys.argv[1]
    filename = sys.argv[2]

    grid, start, dirty = read_world(filename)
    start_state = VacuumState(start, dirty)

    if algorithm == "depth-first":
        path, generated, expanded = depth_first_search(start_state, grid)
    elif algorithm == "uniform-cost":
        path, generated, expanded = uniform_cost_search(start_state, grid)
    else:
        print("use 'depth-first' or 'uniform-cost'")
        return

    if path is not None:
        for action in path:
            print(action)
        print(f"{generated} nodes generated")
        print(f"{expanded} nodes expanded")
    else:
        print("no sol found.")

if __name__ == "__main__":
    main()
