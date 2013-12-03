import pygame
from game.entities.baseclasses import CollidableEntity
from graphics.baseclasses import Sprite

import globals as globs

class Monster(CollidableEntity):
	def __init__(self, parent, xy, wh, attackArea=1600):
		CollidableEntity.__init__(self, parent, xy, wh, (0,255,0))
		self.attackArea = Sprite(parent, (0,0), (attackArea, attackArea))
		print(self.attackArea)
		self.updateAttackArea()

		self.attacking = None

	def events(self):
		self.movement()
		self.updateAttackArea()
		self.updateAttacker()
		if self.attacking:
			self.runTowardsPlayer()

	def updateAttacker(self):
		if not self.attacking:
			closePlayer = pygame.sprite.spritecollideany(self.attackArea, globs.currentgame.players)
			if closePlayer:
				self.attacking = closePlayer
		else:
			if not self.attacking in pygame.sprite.spritecollide(self.attackArea, globs.currentgame.players, False):
				self.attacking = None

	def runTowardsPlayer(self):
		pass

	def updateAttackArea(self):
		x = self.rect.x-(self.attackArea.image.get_width()/2)-(self.image.get_width()/2)
		y = self.rect.y-(self.attackArea.image.get_height()/2)-(self.image.get_height()/2)
		self.attackArea.rect.topleft = (x, y)


class Zombie(Monster):
	def __init__(self, parent, xy):
		wh = (50,90)
		Monster.__init__(self, parent, xy, wh)
		self.image.fill((0,255,0))

	def runTowardsPlayer(self):
		# X
		if self.attacking.rect.x < self.rect.x:
			self.speedX -= (globs.clock.get_time()/20.0)
		elif self.attacking.rect.x > self.rect.x:
			self.speedX += (globs.clock.get_time()/20.0)
		#print(globs.clock.get_time()/20.0)
		#print(self.speedX)

		# Y
		if self.attacking.rect.y < self.rect.y-self.attacking.image.get_height():
			if self.speedY == 0:
				self.speedY = -12
