import pygame
import globals as globs

from game.entities.baseclasses import CollidableEntity
from game.entities.weapons import *

import game.characters as chars

class Character(CollidableEntity):
	def __init__(self, parent, xy, add):
		CollidableEntity.__init__(self, parent, xy, (40,90), (255,0,255), add=add)

		self.load_attributes()

		self.weapon = LongSword(parent, self)

		self.facing = "left"
		self.draw_body()

	def events(self):
		self.update_direction()


	'''

		Body rendering

	'''

	def draw_body(self):
		# Body
		self.basebody = pygame.image.load(globs.datadir+"png/body/base.png")
		self.basebody = self.basebody.convert_alpha()
		self.image.blit(self.basebody, (0,0))
		# Feet
		self.lfoot = pygame.image.load(globs.datadir+"png/body/foot.png")
		self.lfoot = self.basebody.convert_alpha()
		# Left foot
		#self.image.blit(self.lfoot, (5,80))
		# Right foot
		#self.rfoot = pygame.transform.flip(self.lfoot, True, False)
		#self.image.blit(self.rfoot, (40-5-12,80))

	def worldBlit(self):
		xy = (self.rect.x-globs.cameraX, self.rect.y-globs.cameraY)
		self.parent.blit(self.image, xy)

		self.weapon.blit()

	def update_direction(self):
		if self.speedX > 0:
			self.facing = "left"
		elif self.speedX < 0:
			self.facing = "right"

	'''

		Attributes

		### Stats
		# Physical attributes
		# Health, Magicka, Stamina
		#
		# Skills
		# Offensive: Swordfighting, Marksmanship, Destruction
		# Defensive: Heavy Armor, Light Armor, Restoration

	'''

	def load_attributes(self):
		self.stats = chars.load(globs.charactername)
		self.maxhealth = 100 + (10*int(self.stats['Attributes']['vitality'])-10)
		self.health = self.maxhealth
		self.maxmana = 50 + (10*int(self.stats['Attributes']['magicka'])-10)
		self.mana = self.maxmana
		print(self.stats)

	'''

		Movement

	'''

	def run(self, direction):
		force = (globs.clock.get_time()/10.0)
		if direction == "left":
			globs.character.speedX -= force
		elif direction == "right":
			globs.character.speedX += force

	def sprint(self):
		pass
		#if self.blockCollidingY(1):
		#	sprintbonus = 1.1
		#	self.speedX *= sprintbonus

	def climb(self):
		if pygame.sprite.spritecollideany(self, globs.currentgame.climbableBlocks):
			self.speedY = -10

	def jump(self):
		# If not moving in the Y-axis
		globs.currentgame.collidableEntities.remove(self)
		if self.onGround():
			self.speedY = -25
		globs.currentgame.collidableEntities.add(self)

	'''
		Actions
	'''

	def action(self):
		if pygame.spritecollideany(self, globs.currentgame.entities):
			print("Action!")

	def worldAction(self):
		collisionItem = pygame.sprite.spritecollideany(self, globs.currentgame.worldEntities)
		if collisionItem:
			collisionItem.action()