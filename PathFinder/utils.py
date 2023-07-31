import sys, pygame

#

darkgray = 56, 53, 53
red = 180, 50, 30
white = 255, 255, 255
green = 0, 150, 20
blue = 10, 80, 190
orange = 255,165,0
lightgreen = 0, 150, 80

def search_point(queue:list, point:tuple):
	for i in queue:
		if i[0] == point:
			return True

def astar(maze:list, start:tuple, end:tuple):
	queue = [(start, [start])]

	dir_row = [-1, 1, 0, 0]
	dir_col = [0, 0, 1, -1]
	end_reach = False
	visited = []
	
	path = []

	while queue:
		q = queue.pop(0)
		r,c = q[0]
		if (r, c) == end:
			path = q[1]
			end_reach = True
			break
		
		visited.append((r,c))
		for i in range(len(dir_row)):
			curr_r = r + dir_row[i]
			curr_c = c + dir_col[i]
			if curr_r < 0 or curr_r >= len(maze): continue
			if curr_c < 0 or curr_c >= len(maze[curr_r]): continue
			if maze[curr_r][curr_c] == 1: continue
			if search_point(queue, (curr_r, curr_c)) or (curr_r, curr_c) in visited: continue
			queue.append(((curr_r, curr_c), [*q[1], (curr_r, curr_c)]))

	return path

class Visualiser:
	def __init__(self, initial_grid, start, end, tilesize, background):
		self.initial_grid = initial_grid
		self.start = start
		self.end = end
		self.tilesize = tilesize
		self.background = background
		self.fps = 165
		self.startup()

	def startup(self):
		pygame.init()

		self.clock = pygame.time.Clock()
		self.size = len(self.initial_grid[0]) * self.tilesize, len(self.initial_grid) * self.tilesize 
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption('adri712 - locator')
		self.path = astar(self.initial_grid, self.start, self.end)

		self.image = pygame.image.load(self.background).convert()
		self.image = pygame.transform.scale(self.image, self.size)
		
		print(">> pygame init")


	def run(self):
		self.clock.tick(self.fps)
		self.screen.blit(self.image, (0, 0))


		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				pygame.quit()

		for y, l in enumerate(self.initial_grid):
			for i,c in enumerate(l):
				if c == 1:
					pygame.draw.rect(self.screen, "black", (self.tilesize  * y, self.tilesize  * i , self.tilesize , self.tilesize ), 1)
				if (y,i) in self.path:
					pygame.draw.rect(self.screen, "red", (self.tilesize  * y, self.tilesize  * i , self.tilesize , self.tilesize ))
				if y == self.start[0] and i == self.start[1]:
					pygame.draw.rect(self.screen, "green", (self.tilesize  * y, self.tilesize  * i , self.tilesize , self.tilesize ), 1)
				if y == self.end[0] and i == self.end[1]:
					pygame.draw.rect(self.screen, "blue", (self.tilesize  * y, self.tilesize  * i , self.tilesize , self.tilesize ), 1)
		
		self.path = astar(self.initial_grid, self.start, self.end)
		self.old_path = self.path

		"""print(">>", self.path)
		print(">>", self.start)
		print(">>", self.end)
		print()"""

		pygame.display.flip()

	def update(self, new_grid, new_start, new_end):
		self.initial_grid = new_grid
		self.start = new_start
		self.end = new_end
		self.old_path =  self.path
		self.path = astar(self.initial_grid, self.start, self.end)



	def quit(self):
		pygame.quit()
