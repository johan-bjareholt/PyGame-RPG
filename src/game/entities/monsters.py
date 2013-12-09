import pygame
from game.entities.baseclasses import CollidableEntity, Entity
from graphics.baseclasses import Sprite

import globals as globs

class Monster(CollidableEntity):
	def __init__(self, parent, xy, wh, attackArea=1600):
		CollidableEntity.__init__(self, parent, xy, wh, (0,255,0))

		self.attackArea = Sprite(parent, (0,0), (attackArea, attackArea))
		print(self.attackArea)
		self.updateAttackArea()

		self.maxhealth = 100
		self.health = self.maxhealth
		self.lasthealth = None
		self.hitted = []

		self.attacking = None

		# Initialize healthbar
		self.healthbar = Entity(self.parent, (0,0), (self.image.get_width(), 5), add=False)

	def drawHealthbar(self):
		self.healthbar.image.fill((0,0,0))

		healthpercentage = float(self.health)/self.maxhealth

		w = self.healthbar.rect.w * healthpercentage
		newrect = pygame.Rect(0, 0, w, self.healthbar.rect.h)
		self.healthbar.image.fill((255,0,0), newrect)


	def blitHealthbar(self):
		xy = (self.rect.x, self.rect.y-10)

		if self.health != self.lasthealth:
			self.drawHealthbar()
		self.lasthealth = self.health

		self.healthbar.rect = self.healthbar.image.get_rect(topleft=xy)
		self.healthbar.worldBlit()

	def worldBlit(self):
		CollidableEntity.worldBlit(self)
		self.blitHealthbar()


	def events(self):
		self.movement()
		self.updateAttackArea()
		self.checkHurt()
		if not self.isAlive():
			self.die()
		self.updateAttacker()
		if self.attacking:
			self.runTowardsPlayer()

	def isAlive(self):
		if self.health <= 0:
			return False
		return True

	def die(self):
		self.kill()

	def checkHurt(self):
		collidedItem = pygame.sprite.spritecollideany(self, globs.currentgame.lethals)
		if collidedItem:
			if not collidedItem.owner in self.hitted:
				print("hitted!")
				# Push
				speedX = collidedItem.push
				if collidedItem.owner.facing == "right":
					speedX = -speedX
				self.speedX += speedX

				# Remove health
				self.health -= collidedItem.damage

				# Needed so he is not hurt every frame the player is colliding with the lethal item
				self.hitted.append(collidedItem.owner)
				collidedItem.hitting.append(self)

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
