import pymem

class Addresses:
	dwLocalPlayer = (0xDEA98C)
	dw_healthOffset = (0x100)
	dw_teamOffset = (0xF4)
	dw_pos=(0x138)
	dwEntityList = (0x4DFFF7C)
	playerOffset = (0x10)
	PlayerCount = (0x7A91A0)
	
	dwClientState = (0x59F19C)
	dwClientState_ViewAngles = (0x4D90)

	m_bSpotted = 0x93D

class Player:
	def __init__(self, CLocalPlayer, id, team, health, position):
		self.CLocalPlayer = CLocalPlayer
		self.id = id
		self.team = team
		self.health = health
		self.position = position
		self.distance = 0

	def __repr__(self):
		return f"ID: {self.id} | team: {self.team} | health: {self.health} | position: {self.position} | Distance: {self.distance}"

	def get_player_info(self, process):
		self.position = [process.read_float(self.CLocalPlayer + Addresses.dw_pos),  process.read_float(self.CLocalPlayer + Addresses.dw_pos + 4), process.read_float(self.CLocalPlayer + Addresses.dw_pos + 8) ]
		#print(self.test.decode("euc_kr"))
		self.team = process.read_int(self.CLocalPlayer + Addresses.dw_teamOffset)
		self.health = process.read_int(self.CLocalPlayer + Addresses.dw_healthOffset)
