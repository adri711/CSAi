from math import sqrt,asin,atan


def calcAngle(src, dst):
	try:
		delta = [src[0]-dst[0], src[1] - dst[1], src[2] - dst[2] ]
		hyp = sqrt(delta[0]**2 + delta[1]**2)
		angle = [
			float(asin(delta[2] / hyp )) * 57.295779513082,
			float(atan(delta[1] / delta[0])) * 57.295779513082,
			0]
		if delta[0] >= 0.0: angle[1] +=180.0
		return angle
	except:
		print(">> Problem calculating angle")

def calcDistance(src, dst):
	return sqrt( (src[0]-dst[0])**2 + (src[1]-dst[1])**2 + (src[2]-dst[2])**2 )

def Aimbot(player, enemies):
	for enemy in enemies:
		enemy.distance = calcDistance(player.position, enemy.position)
	enemies.sort(key=lambda e: e.distance)
	return calcAngle(player.position, enemies[0].position)
