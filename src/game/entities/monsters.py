import pygame
from game.entities.baseclasses import CollidableEntity
from graphics.baseclasses import Sprite

import globals as globs

class Monster(CollidableEntity):
	def __init__(self, parent, xy, wh, attackArea=1200):
		CollidableEntity.__init__(self, parent, xy, wh, (0,255,0))
		self.attackArea = Sprite(parent, (0,0), (attackArea, attackArea))
		print(self.attackArea)
		self.updateAttackArea()

		self.attacking = None

	def events(self):
		self.movement()
		self.updateAttackArea()
		self.runTowardsPlayer()

	def runTowardsPlayer(self):
		if not self.attacking:
			closePlayer = pygame.sprite.spritecollideany(self.attackArea, globs.currentgame.players)
			if closePlayer:
				self.attacking = closePlayer
		else:
			if self.attacking in pygame.sprite.spritecollide(self.attackArea, globs.currentgame.players, False):
				# X
				if self.attacking.xy[0] < self.xy[0]:
					self.speedX -= 1.5
				elif self.attacking.xy[0] > self.xy[0]:
					self.speedX += 1.5

				# Y
				if self.attacking.xy[1] < self.xy[1]-self.attacking.image.get_height():
					if self.speedY == 0:
						self.speedY = -12
			else:
				self.attacking = None

	def updateAttackArea(self):
		x = self.xy[0]-(self.attackArea.image.get_width()/2)-(self.image.get_width()/2)
		y = self.xy[1]-(self.attackArea.image.get_height()/2)-(self.image.get_height()/2)
		self.attackArea.move((x, y))


class Zombie(Monster):
	def __init__(self, parent, xy):
		wh = (50,90)
		Monster.__init__(self, parent, xy, wh)
		self.image.fill((0,255,0))