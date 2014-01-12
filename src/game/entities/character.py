import pygame
import globals as globs

from game.entities.baseclasses import LivingEntity, Entity
from game.entities.weapons import *

import game.characters as chars

class Character(LivingEntity):
	def __init__(self, xy, add, custom_appearance=None):
		health = 0
		LivingEntity.__init__(self, xy, (40,90), health, add=add)

		if globs.charactername:
			self.load()
		else:
			self.weapon = None
		if custom_appearance:
			self.set_appearance(**custom_appearance)
		self.facing = "left"
		self.draw_body()

	def load(self):
		self.load_attributes()
		self.load_appearance()
		self.health = 50

		self.weapon = Bow(self)

	def events(self):
		self.update_direction()

		self.checkHurt()
		self.weapon.isHurting()
		if not self.isAlive():
			self.die()

		globs.currentgame.healthbar.update(self.health, self.maxhealth)
		globs.currentgame.manabar.update(self.mana, self.maxmana)


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

		# Pants
		self.pants = pygame.image.load(globs.datadir+"/png/equipment/briefs.png").convert_alpha()
		self.image.blit(self.pants, (8,52))

		#Hair
		hairstyle = self.appearance["hairstyle"]
		haircolor = self.appearance["haircolor"]
		self.hair = pygame.image.load(globs.datadir+"/png/body/hair/"+hairstyle+".png").convert_alpha()
		pixelarray = pygame.PixelArray(self.hair)
		darkercolor = (haircolor[0]-30, haircolor[1]-30, haircolor[2]-30)
		pixelarray.replace((0,0,0),darkercolor) # Outerpixels
		pixelarray.replace((255,255,255), haircolor) # Innerpixels
		self.hair = pixelarray.make_surface()
		self.hairr = self.hair
		self.hairr = pygame.transform.flip(self.hairr, True, False)

	def blit(self, camera=(0,0), blitsurface=None):
		if not blitsurface:
			blitsurface = globs.screen
		xy = (self.rect.x-camera[0], self.rect.y-camera[1])

		# Weapon 
		if self.weapon:
			self.weapon.blit()

		# Body
		blitsurface.blit(self.image, xy)

		# Hair
		blitsurface.blit(self.hair, (xy[0], xy[1]-10))

		# Feet
		if self.speedX > 0:
			# Right foot
			blitsurface.blit(self.rfoot, (xy[0]+40-5-12,
										   xy[1]+80))
			# Left foot right
			blitsurface.blit(self.rfoot, (xy[0]+5+5,
										   xy[1]+80))
		elif self.speedX < 0:
			# Left foot
			blitsurface.blit(self.lfoot, (xy[0]+5,
										   xy[1]+80))
			# Right foot left
			blitsurface.blit(self.lfoot, (xy[0]+40-5-12-5,
										   xy[1]+80))
		else:
			# Right foot
			blitsurface.blit(self.rfoot, (xy[0]+40-5-12,
										   xy[1]+80))
			# Left foot
			blitsurface.blit(self.lfoot, (xy[0]+5,
										   xy[1]+80))	

	def worldBlit(self):
		#print(globs.cameraX, globs.cameraY)
		self.blit(camera=(globs.cameraX, globs.cameraY))


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

	def load_appearance(self):
		hairstyle = "hair1"
		haircolor = (160,100,80)
		eyecolor = (0,0,0)
		self.set_appearance(hairstyle, haircolor, eyecolor)

	def set_appearance(self, hairstyle, haircolor, eyecolor):
		self.appearance = {"hairstyle": hairstyle,
						   "haircolor": haircolor,
						   "eyecolor": eyecolor}

	'''

		Movement

	'''

	def run(self, direction):
		force = (globs.clock.get_time()/10.0)
		#print(force)
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