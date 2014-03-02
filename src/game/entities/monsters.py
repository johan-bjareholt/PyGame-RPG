import pygame
from game.entities.baseclasses import LivingEntity, Entity
from graphics.baseclasses import Sprite
from game.entities.weapons import Sword

import globals as globs

class Monster(LivingEntity):
	def __init__(self, xy, wh, health, attackArea=2000):
		LivingEntity.__init__(self, xy, wh, (0,255,0), health)

		self.attackArea = Sprite((0,0), (attackArea, attackArea))
		#print(self.attackArea)
		self.updateAttackArea()

		globs.currentgame.monsters.add(self)

		self.maxhealth = 100
		self.health = self.maxhealth
		self.lasthealth = None
		self.owner = None
		self.hitted = []

		self.attacking = None

		# Initialize healthbar
		self.healthbar = Entity((0,0), (self.image.get_width(), 5), add=False)

	def blit(self):
		if self.weapon:
			self.weapon.blit()
		self.worldBlit()

	def events(self):
		self.movement()
		self.checkHurt()
		self.weapon.isHurting()
		if not self.isAlive():
			self.die()
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
		x = self.rect.x-(self.attackArea.image.get_width()/2)+(self.image.get_width()/2)
		y = self.rect.y-(self.attackArea.image.get_height()/2)+(self.image.get_height()/2)
		self.attackArea.rect.topleft = (x, y)


class Zombie(Monster):
	def __init__(self, xy):
		wh = (50,90)
		health = 100
		Monster.__init__(self, xy, wh, health)
		self.image.fill((0,255,0))
		self.facing = "right"

		self.weapon = Sword(self)

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
