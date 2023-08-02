'''
	CSAi - Master
	Author: adri711
	Language: Python
'''


import keyboard, ctypes, pymem, time, pickle, os
from constants import Addresses, Player
from utility import Aimbot, calcDistance
from PathFinder.utils import Visualiser, astar
from controller import PlayerController
from pynput.keyboard import Key, Controller
import pygame

players = []

auto_pilot = False

with open("dust2.obj", "rb") as f:
	try:
		grid=pickle.load(f)
		f.close()
		print(">> Minimap grid successfuly loaded.")
	except:
		print(">> Failed to load minimap grid.")
		exit()

minimap_pixels = 512
tile_size = minimap_pixels // len(grid)
map_scale = 8.8
x_pos = 2476
y_pos = 3239
background = "minimaps/dust2.png"

def getPlayerLocation(playerPos, map_scale, x_pos, y_pos):
	x = int( abs( playerPos[0] + x_pos ) / map_scale )
	y = int( abs( playerPos[1] - y_pos ) / map_scale )

	return x,y

def getPlayerGridIndices(playerPos):
	x=int(playerPos[0])
	y=int(playerPos[1])

	while x % tile_size != 0:
		x = x -1

	while y % tile_size != 0:
		y = y -1

	return (x // 4,y // 4)


if __name__ == "__main__":
	process = pymem.Pymem("csgo.exe")

	'''online_players = process.read_int( 
		pymem.process.module_from_name(process.process_handle, "engine.dll").lpBaseOfDll + Addresses.PlayerCount
	)'''

	clientAddr = pymem.process.module_from_name(process.process_handle, "client.dll").lpBaseOfDll
	player_ptr = process.read_int(clientAddr + Addresses.dwLocalPlayer)
	myteam = process.read_int(player_ptr + Addresses.dw_teamOffset)

	GUI = None

	engineAddr = pymem.process.module_from_name(
		process.process_handle, 
		"engine.dll"
	).lpBaseOfDll

	player = Player(player_ptr, 0, 1, 100, [])
	player.get_player_info(process)

	player_client_state = process.read_uint(engineAddr + Addresses.dwClientState)
	ViewAnglesAddress = player_client_state + Addresses.dwClientState_ViewAngles
	player_controller = PlayerController(process,ViewAnglesAddress, [])

	while True:
		try:
			if keyboard.is_pressed('f1'):
				auto_pilot = not auto_pilot
				print("Auto pilot running: ", auto_pilot)
				if auto_pilot:
					print(">> pygame starting..")
					os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)
					GUI = Visualiser(grid, (0,0), (0,0), 4, background)
				else:
					player_controller.controller.release(player_controller.move_key)
					GUI.quit()
					GUI = None
				#time.sleep(0.1)

		except Exception as error:
			print(error)

		if auto_pilot and GUI:
			# 
			player.get_player_info(process)

			players = []

			for i in range(1,32):
				curr_player = process.read_uint(clientAddr +  Addresses.dwEntityList + i * 0x10 )

				if not curr_player:
					continue

				enemy = Player(curr_player, i, None, None, None)
				enemy.get_player_info(process)

				if enemy.team == myteam or enemy.health <= 2:
					continue

				enemy.distance = calcDistance(player.position, enemy.position)

				#process.write_uchar(curr_player + Addresses.m_bSpotted, 1)
				players.append( enemy )

			print(players)

			if players:
				
				Angle = Aimbot(player , players) # has to be up here because it does the enemies sorting by distance
				
				Angle = [0,270,0]

				print('->te')
				myPlayerLocation = getPlayerLocation(
					player.position,
					map_scale, 
					x_pos, 
					y_pos
				)
				
				enemyLocation = getPlayerLocation(
					players[0].position, 
					map_scale, 
					x_pos, 
					y_pos
				)
				print('nig')
				start = getPlayerGridIndices(myPlayerLocation)
				end= getPlayerGridIndices(enemyLocation)
				print(start, end)
				path = astar(grid, start, end)
				print('fa')

				GUI.update(grid, start, end, path)

				player_controller.aimAt([0, 270,0])
				player_controller.player_position = start


				try:
					player_controller.followPath(path[1])
				except:
					print(">>error")

				try:
					if players[0].distance <= 170.0:
						Angle = [Angle[0]+6, Angle[1], Angle[2]]
						player_controller.aimAt(Angle)
						player_controller.shoot()
				except:
					print('nigger')

			else:
				print(">> No playerrs to display")

			GUI.run()
