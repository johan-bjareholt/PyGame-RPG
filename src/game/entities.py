import pygame
from graphics.baseclasses import Sprite
import globals as globs

import characters

class Entity(Sprite):
	def __init__(self, parent, xy, wh, bgColor, bounce=0):
		Sprite.__init__(self, parent, xy, wh, bgColor)
		self.speedX = 0.0
		self.speedY = 0.0
		self.bounce = bounce

		self.state = "falling"


	def loop(self):
		self.collision(self)


	def collision(self):
		#
		# Horizontal
		#
		lastlocation = self.xy
		self.move((self.X+int(self.speedX), self.Y))
		if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
			#print("Collide!!! {}".format(pygame.sprite.spritecollide(self, globs.currentgame.worldBlocks, dokill=False)))
			if self.speedX > 0:
				x = pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks).xy[0]-self.image.get_width()
			elif self.speedX < 0:
				x = pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks).xy[0]+50
			else:
				print("Movement error in X")
			self.move((x, self.Y))
			self.speedX *=self.bounce
		else:
			self.speedX = self.speedX / 1.1

		#
		# Vertical
		#
		lastlocation = self.xy

		gravityequation = 1.1

		# If jumping
		if self.state == "jumping":
			self.move((self.X, self.Y+self.speedY))
			if self.speedY >= -1:
				self.state = "falling"
			if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
				self.move(lastlocation)
				self.speedY = 0
				self.state = "falling"
			else:
				self.speedY /= gravityequation

		# If on ground
		elif self.state == "ground":
			# See if block under feet
			self.move((self.X, self.Y+1))
			if not pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
				self.state = "falling"
				self.speedY = 1
			self.move(lastlocation)

		# Else fall
		if self.state == "falling":
			if self.speedY < 1:
				self.speedY = 1
			self.speedY *= gravityequation
			self.move((self.X, self.Y + self.speedY))
			if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
				while pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
					Y = pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks).xy[1]-self.image.get_height()
					self.move((self.X, Y))
				self.state = "ground"
				self.speedY = 0

		# Out of bounds Y
		if self.Y > globs.currentregion.pixelHeight-50:
			self.move((self.xy[0], globs.currentregion.pixelHeight-50))
			self.speedY = 0
		elif self.Y < 0:
			self.move((self.xy[0], 0))
			self.speedY = 0
		# Out of bounds X
		if self.X > globs.currentregion.pixelWidth-50:
			self.move((globs.currentregion.pixelWidth-50, self.xy[1]))
			self.speedX = 0
		elif self.X < 0:
			self.move((0, self.xy[1]))
			self.speedX = 0

		#print("ms since last frame:{} gravityequation: {} speedY: {}".format(globs.ticktime, gravityequation, self.speedY))
		#print(self.state)



class Character(Entity):
	def __init__(self, parent, xy):
		Entity.__init__(self, parent, xy, (50,90), (255,255,255))

		self.loadAttributes()

		self.drawBody()

	def loop(self):
		self.collision()
		self.updateBodyDirection()

	'''

		Body rendering

	'''

	def drawBody(self):
		#pygame.draw.rect(self.image, (0,0,0), bodyRect)

		self.facefacing = "right"
		self.bodyfacing = "right"
		self.legDirection = 1

		#headR = 10
		#headY = headR
		#headX = (self.image.get_width()/2)

		#pygame.draw.circle(self.image, (0,0,0), (headX, headY), headR)

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

	def blit(self, camera=(0,0)):
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

	def updateBodyDirection(self):
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

	def loadAttributes(self):
		self.attributes = characters.load(globs.charactername)
		print(self.attributes)

	'''

		Movement

	'''

	def run(self, direction):
		force = 2
		if direction == "left":
			globs.character.speedX -= force
		elif direction == "right":
			globs.character.speedX += force

	def sprint(self):
		if self.state == "ground":
			sprintbonus = 1.1
			self.speedX *= sprintbonus

	def jump(self):
		# If not going up
		if self.state == "ground":
			self.speedY = -25
			self.state = "jumping"

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