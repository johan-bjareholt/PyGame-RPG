import pygame
import globals as globs

from game.entities.baseclasses import CollidableEntity

import game.characters as chars

class Character(CollidableEntity):
	def __init__(self, parent, xy, add):
		CollidableEntity.__init__(self, parent, xy, (50,90), (255,255,255), add=add)

		self.load_attributes()

		self.draw_body()

	def events(self):
		self.update_direction()

	'''

		Body rendering

	'''

	def draw_body(self):
		#pygame.draw.rect(self.image, (0,0,0), bodyRect)

		self.facefacing = "right"
		self.bodyfacing = "right"
		self.legDirection = 1

		headR = 10
		headY = headR
		headX = (self.image.get_width()/2)

		pygame.draw.circle(self.image, (0,0,0), (headX, headY), headR)

		self.bodyH = 35
		self.bodyW = 30
		self.bodyY = (self.image.get_height()/2)-(self.bodyH/2)
		self.bodyX = (self.image.get_width()-self.bodyW)/2#(self.image.get_width()/2)-(bodyW/2)
		bodyColor = (0,0,255)

		self.body = pygame.surface.Surface((self.bodyW, self.bodyH))
		bodyRect = pygame.Rect((self.bodyX, self.bodyY), (self.bodyW, self.bodyH))
		self.body.fill(bodyColor)

		self.legsW = 15
		self.legsH = 20
		self.legsY = self.bodyY+self.bodyH
		extrainwards = 2
		self.legsX1 = self.bodyX+extrainwards
		self.legsX2 = self.bodyX+self.bodyW-self.legsW-extrainwards

		self.legs = pygame.surface.Surface((self.legsW, self.legsH))
		#bodyRect = pygame.Rect((self.bodyX, self.bodyY), (self.legsW, self.legsH))
		self.legsColor = (255,180,140)
		self.legsColorDark = pygame.color.Color(210,140,100)
		self.legs.fill(self.legsColor)
		pygame.draw.rect(self.legs, self.legsColorDark, pygame.Rect((0,0),(self.legsW, self.legsH)), 3)

	def blit(self):
		camera = (globs.cameraX, globs.cameraY)
		self.parent.blit(self.image, (self.xy[0]-camera[0], self.xy[1]-camera[1]))
		#Body
		self.parent.blit(self.body, (self.xy[0]+self.bodyX-camera[0], self.xy[1]+self.bodyY-camera[1]))
		# Legs
		if self.speedX != 0:
			# Leg 1
			self.parent.blit(self.legs, (self.xy[0]+self.legsX1-camera[0], self.xy[1]+self.legsY-camera[1]))
			# Leg 2
			self.parent.blit(self.legs, (self.xy[0]+self.legsX2-camera[0], self.xy[1]+self.legsY-camera[1]))
		else:
			# Leg 1
			self.parent.blit(self.legs, (self.xy[0]+self.legsX1-camera[0], self.xy[1]+self.legsY-camera[1]))
			# Leg 2
			self.parent.blit(self.legs, (self.xy[0]+self.legsX2-camera[0], self.xy[1]+self.legsY-camera[1]))

	def update_direction(self):
		if self.speedX > 0:
			self.facefacing = "left"
			self.bodyfacing = "left"
		elif self.speedX < 0:
			self.facefacing = "right"
			self.bodyfacing = "left"
		else:
			self.facefacing = "front"

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
		if pygame.sprite.spritecollideany(self, globs.currentgame.entities):
			print("Action!")

	def worldAction(self):
		collisionItem = pygame.sprite.spritecollideany(self, globs.currentgame.worldEntities)
		if collisionItem:
			collisionItem.action()