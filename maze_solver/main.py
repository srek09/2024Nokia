'''for this task, I used the A* algorithm (solve_maze function) to solve the maze.
The A* algorithm is efficient and guarantees the shortest path from the start to the goal node.
The function takes a maze object as an argument and returns the shortest path from the start to the goal node.
The get_path function is used to convert the dictionary into a string representation of the path.
The main function reads the input file, creates a list of maze objects, and solves them.
'''

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

	# checks if a node is within the bounds of the maze and not a wall
	def in_bounds(self, id):
		(x, y) = id
		return 0 <= x < self.cols and 0 <= y < self.rows and id not in self.walls

	# returns the neighbors of a node
	def neighbors(self, id):
		(x, y) = id
		neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
		results = [(node, self.weights.get(node, 1)) for node in neighbors if self.in_bounds(node)]
		return results


mazes = []

with open('./input.txt', 'r') as f:
    
	id, walls, weights, start, goal, rows, current_line = '', [], {}, None, None, 1, 0
	for line in f:
		line = line.strip().replace(' ', '')
		if len(line) < 2: # if the line is empty or contains only the maze id
			if len(line) > 0: # if the line contains the maze id we assign it to the current maze
				id = line
			rows -= 1
			# this scenario appears when it is the end of the maze
			if walls != [] and (len(mazes) == 0 or len(mazes[-1].walls) > 0):
				mazes.append(Maze(id, walls, weights, start, goal, rows, current_line))
				weights = {}
				walls = []
				current_line = 0
				rows = 0
		else: # if the line contains part of the maze
			char_idx = 0
			for char in line:
				match char: # we check the character and assign the corresponding value to the maze object
					case '.':
						weights[(current_line, char_idx)] = 1
					case '#':
						walls.append((current_line, char_idx))
					case 'S':	
						start = (current_line, char_idx)
					case 'G':
						goal = (current_line, char_idx)
				char_idx += 1

			current_line += 1

		rows += 1
	# we add the last maze to the list
	mazes.append(Maze(id, walls, weights, start, goal, rows, current_line ))


class PriorityQueue:
    def __init__(self):
        self.elements = []

    empty = lambda self: not self.elements

    put = lambda self, item, priority: heappush(self.elements, (priority, item))

    get = lambda self: heappop(self.elements)[1]


# return the directions from the start to the goal node
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


def solve_maze(maze):
	start = maze.start
	goal = maze.goal
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

		for (next, cost) in maze.neighbors(current):
			new_cost = cost_so_far[current] + cost
			if next not in cost_so_far or new_cost < cost_so_far[next]:
				cost_so_far[next] = new_cost
				priority = new_cost + abs(next[0] - goal[0]) + abs(next[1] - goal[1])
				frontier.put(next, priority)
				came_from[next] = current


	return came_from

# print the path for each maze
print('\n\n'.join([maze.id + '\n' + get_path(solve_maze(maze), start=maze.start, goal=maze.goal) for maze in mazes]))