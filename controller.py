from pynput.keyboard import Key, Controller
import pymem, mouse, time
"""import time

myKeyboard = Controller()

while True:
	try:
		if keyboard.is_pressed('q'):
			myKeyboard.press('w')
			time.sleep(0.5)
			myKeyboard.release('w')
			break
	except:
		break"""

keys = {
	'up':'w',
	'down':'s',
	'right':'d',
	'left': 'a'
}

class PlayerController:
	def __init__(self, process, viewAnglesAddress, player_position):
		self.controller = Controller()
		self.process = process
		self.viewAnglesAddress = viewAnglesAddress
		self.player_position = player_position
		self.move_key = None
		self.old_key = None
		
	def followPath(self, next_step):
		self.old_key = self.move_key
		if self.player_position[0] - next_step[0]: # X AXIS MOVEMENT
			if self.player_position[0] - next_step[0] > 0: # X AXIS MOVEMENT
				self.move_key = keys['right']
			else:
				self.move_key = keys['left']

		if self.player_position[1] - next_step[1]: # Y AXIS MOVEMENT
			if self.player_position[1] - next_step[1] > 0: # Y AXIS MOVEMENT
				self.move_key = keys['down']
			else:
				self.move_key = keys['up']

		if self.old_key != self.move_key and self.old_key:
			self.controller.release(self.old_key)
		
		self.controller.press(self.move_key)



	def aimAt(self, angle):
		self.process.write_float(self.viewAnglesAddress, float(angle[0]))
		self.process.write_float(self.viewAnglesAddress + 4, float(angle[1]))
		self.process.write_float(self.viewAnglesAddress + 8, float(angle[2]))


	def shoot(self):
		mouse.click('left')

	def release(self):
		self.controller.release(self.move_key)
