import sys, pygame

#

darkgray = 56, 53, 53
red = 180, 50, 30
white = 255, 255, 255
green = 0, 150, 20
blue = 10, 80, 190
orange = 255,165,0
lightgreen = 0, 150, 80

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

class Visualiser:
	def __init__(self, initial_grid, start, end, tilesize, background):
		self.initial_grid = initial_grid
		self.start = start
		self.end = end
		self.tilesize = tilesize
		self.background = background
		self.fps = 60
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
		#self.clock.tick(self.fps)
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

	def update(self, new_grid, new_start, new_end, path):
		self.initial_grid = new_grid
		self.start = new_start
		self.end = new_end
		self.old_path =  self.path
		self.path = path
		#self.path = astar(self.initial_grid, self.start, self.end)



	def quit(self):
		pygame.quit()
