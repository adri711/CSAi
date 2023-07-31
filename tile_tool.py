# importing required library
import pygame, pickle

# activate the pygame library .
pygame.init()
X = 512
Y = 512

screen = pygame.display.set_mode((X, Y))

pygame.display.set_caption('image')
image = pygame.image.load("minimaps/dust2.png").convert()

image=pygame.transform.scale(image, (X,Y))

screen.blit(image, (0, 0))

clock = pygame.time.Clock()

TILE_SIZE = 4


# MINIMAP GRID
grid = [0] * (X // TILE_SIZE)
for i in range(len(grid)):
	grid[i] = [0] * (Y // TILE_SIZE)

try:
	with open("to_load.obj", "rb") as f:
		grid = pickle.load(f)
except:
	print(">> No save file found")

def getClosestSquare(pos):
	while pos[0] % TILE_SIZE != 0: pos[0] -= 1
	while pos[1] % TILE_SIZE != 0: pos[1] -= 1	
	return pos

# paint screen one time
status = True
mouse_hold=False
while (status):
	clock.tick(60)
	screen.blit(image, (0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			status = False
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				mouse_hold = True
			if event.button == 3:
				pos = pygame.mouse.get_pos()
				x,y=getClosestSquare([pos[0], pos[1]])
				grid[x//TILE_SIZE][y//TILE_SIZE] = 0

		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				mouse_hold = False


		if event.type == pygame.KEYDOWN:
			if event.mod & pygame.KMOD_LSHIFT:
				try:
					f=open("minimap_grid.obj", 'wb') 
					pickle.dump(grid, f)
					f.close()
					print("Successfully saved")
				except:
					print("Couldn't save the grid")

	if mouse_hold:
		pos = pygame.mouse.get_pos()
		x,y=getClosestSquare([pos[0], pos[1]])
		grid[x//TILE_SIZE][y//TILE_SIZE] = 1

	for i in range(0, len(grid)):
		for j in range(0, len(grid[i])):
			if grid[i][j] == 1:
				pygame.draw.rect(screen, "red", [i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE], 1)
	
	#pygame.draw.rect(screen, "blue", [ abs(int( (-1728.3160400390625+ 2476) / 8.8) )  , abs(int( (555.9342651367188 - 3239) / 8.8 )), 10, 10], 1)

	x,y=pygame.mouse.get_pos()
	x,y = getClosestSquare([x,y])
	pygame.draw.rect(screen, "red", [x, y, TILE_SIZE, TILE_SIZE], 1)

	pygame.display.flip()

pygame.quit()