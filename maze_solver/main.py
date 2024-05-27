from heapq import heappush, heappop
class Maze:
	def __init__(self, id, walls, weights, start, goal, rows, cols):
		if len(weights) > 0:
			self.id = id
			self.weights = weights
			self.walls = walls
			self.start = start
			self.goal = goal
			self.rows = rows
			self.cols = cols


	def in_bounds(self, id):
		(x, y) = id
		return 0 <= x < self.cols and 0 <= y < self.rows and id not in self.walls


	def neighbors(self, id):
		(x, y) = id
		neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
		results = [(node, self.weights.get(node, 1)) for node in filter(self.in_bounds, neighbors)]
		return results


mazes = []

with open('./input.txt', 'r') as f:
	walls, start, goal, current_line, rows = [], None, None, 0, 1
	id = ''
	weights = {}
	for line in f:
		line = line.strip().replace(' ', '')
		if len(line) < 2:
			if len(line) > 0:
				id = line
			rows -= 1
			if walls != [] and (len(mazes) == 0 or len(mazes[-1].walls) > 0):
				mazes.append(Maze(id, walls, weights, start, goal, rows, current_line))
				weights = {}
				walls = []
				current_line = 0
				rows = 0
		else:
			char_idx = 0
			for char in line:
				if char == '.':
					weights[(current_line, char_idx)] = 1
				elif char == '#':
					walls.append((current_line, char_idx))	
				elif char == 'S':
					start = (current_line, char_idx)
				elif char == 'G':
					goal = (current_line, char_idx)
				char_idx += 1

			current_line += 1

		rows += 1


	mazes.append(Maze(id, walls, weights, start, goal, rows, current_line ))


class PriorityQueue:
    def __init__(self):
        self.elements = []

    empty = lambda self: not self.elements

    put = lambda self, item, priority: heappush(self.elements, (priority, item))

    get = lambda self: heappop(self.elements)[1]

def get_path(came_from, start, goal):
	current = goal
	path = ['G']
	if goal not in came_from: 
		return []

	while current != start:
		if current[0] > came_from[current][0]:	
			path.append('D')
		elif current[0] < came_from[current][0]:
			path.append('U')
		elif current[1] > came_from[current][1]:
			path.append('R')
		elif current[1] < came_from[current][1]:
			path.append('L')
		current = came_from[current]

	path.append('S')
	return ' '.join(path[::-1])

def solve_maze(graph):
	start = graph.start
	goal = graph.goal
	frontier = PriorityQueue()
	frontier.put(start, 0)
	came_from = {}
	cost_so_far = {}
	came_from[start] = None
	cost_so_far[start] = 0

	while not frontier.empty():
		current = frontier.get()
		if current == goal:
			break

		for (next, cost) in graph.neighbors(current):
			new_cost = cost_so_far[current] + cost
			if next not in cost_so_far or new_cost < cost_so_far[next]:
				cost_so_far[next] = new_cost
				priority = new_cost + abs(next[0] - goal[0]) + abs(next[1] - goal[1])
				frontier.put(next, priority)
				came_from[next] = current


	return came_from


print('\n\n'.join([maze.id + '\n' + get_path(solve_maze(maze), start=maze.start, goal=maze.goal) for maze in mazes]))