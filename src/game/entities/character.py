import pygame
import globals as globs

from game.entities.baseclasses import CollidableEntity, Entity
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
		self.lfoot = pygame.image.load(globs.datadir+"png/body/foot.png").convert_alpha()
		self.rfoot = pygame.transform.flip(self.lfoot, True, False)
		# Left foot
		#self.image.blit(self.lfoot, (5,80))
		# Left foot right
		#self.image.blit(self.rfoot, (5+6,80))
		# Right foot
		#self.image.blit(self.rfoot, (40-5-12,80))
		# Right foot left
		#self.image.blit(self.lfoot, (40-5-12-6,80))

		# Pants
		self.pants = pygame.image.load(globs.datadir+"/png/equipment/briefs.png").convert_alpha()
		self.image.blit(self.pants, (8,52))

		#Hair
		self.hair = Entity(self.parent, (self.rect.x, self.rect.y-10), (10,10), add=False)
		self.hair.image = pygame.image.load(globs.datadir+"/png/body/hair/hair1.png").convert_alpha()
		pixelarray = pygame.PixelArray(self.hair.image)
		color = (160,100,80)
		darkercolor = (color[0]-40, color[1]-40, color[2]-40)
		pixelarray.replace((0,0,0),darkercolor) # Outerpixels
		pixelarray.replace((255,255,255), color) # Innerpixels
		self.hair.image = pixelarray.make_surface()
		self.hairr = self.hair
		self.hairr = pygame.transform.flip(self.hairr.image, True, False)

	def worldBlit(self):
		xy = (self.rect.x-globs.cameraX, self.rect.y-globs.cameraY)

		# Weapon 
		self.weapon.blit()

		# Body
		self.parent.blit(self.image, xy)

		# Hair
		self.hair.rect = self.hair.image.get_rect(topleft=(self.rect.x, self.rect.y-10))
		self.hair.worldBlit()

		# Feet

		# Left foot
		#globs.screen.blit(self.lfoot, (self.rect.x+5,self.rect.y+80))
		# Left foot right
		#globs.screen.blit(self.rfoot, (self.rect.x+5+6,self.rect.y+80))
		# Right foot
		#globs.screen.blit(self.rfoot, (self.rect.x+40-5-12,self.rect.y+80))
		# Right foot left
		#globs.screen.blit(self.lfoot, (self.rect.x+40-5-12-6,self.rect.y+80))

		if self.speedX > 0:
			# Right foot
			globs.screen.blit(self.rfoot, (self.rect.x+40-5-12-globs.cameraX,
										   self.rect.y+80-globs.cameraY))
			# Left foot right
			globs.screen.blit(self.rfoot, (self.rect.x+5+5-globs.cameraX,
										   self.rect.y+80-globs.cameraY))
		elif self.speedX < 0:
			# Left foot
			globs.screen.blit(self.lfoot, (self.rect.x+5-globs.cameraX,
										   self.rect.y+80-globs.cameraY))
			# Right foot left
			globs.screen.blit(self.lfoot, (self.rect.x+40-5-12-5-globs.cameraX,
										   self.rect.y+80-globs.cameraY))
		else:
			# Right foot
			globs.screen.blit(self.rfoot, (self.rect.x+40-5-12-globs.cameraX,
										   self.rect.y+80-globs.cameraY))
			# Left foot
			globs.screen.blit(self.lfoot, (self.rect.x+5-globs.cameraX,
										   self.rect.y+80-globs.cameraY))

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