import pygame
from .baseclasses import Sprite
import globals as globs

class Character(Sprite):
	def __init__(self, parent, xy):
		Sprite.__init__(self, parent, xy, (50,75), bgColor=(255,255,255))

		self.speedX = 0.0
		self.speedY = 0.0

		self.facefacing = "front"
		self.bodyfacing = "right"

		self.state = "falling"

		headR = 10
		headY = headR
		headX = (self.image.get_width()/2)

		pygame.draw.circle(self.image, (0,0,0), (headX, headY), headR)


		bodyH = 15
		bodyW = 15
		bodyY = 50
		bodyX = (self.image.get_width()/2)-(bodyW/2)

		bodyRect = pygame.Rect((bodyX, bodyY), (bodyW, bodyH))

		pygame.draw.rect(self.image, (0,0,0), bodyRect)

		### Stats
		# Physical attributes
		# Health, Magicka, Stamina
		#
		# Skills
		# Swordfighting, Marksmanship, Arcane

	def collision(self):
		#
		# Horizontal
		#
		lastlocation = self.xy
		self.speedX = self.speedX / 2
		self.move((self.X+int(self.speedX), self.Y))
		if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
			#print("Collide!!! {}".format(pygame.sprite.spritecollide(self, globs.currentgame.worldBlocks, dokill=False)))
			self.move(lastlocation)
			self.speedX = 0

		if self.speedX > 0:
			self.facefacing = "left"
			self.bodyfacing = "left"
		elif self.speedX < 0:
			self.facefacing = "right"
			self.bodyfacing = "left"
		else:
			self.facefacing = "front"

		#
		# Vertical
		#
		lastlocation = self.xy

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
				self.speedY = self.speedY/1.8

		# If on ground
		elif self.state == "ground":
			# See if block under feet
			self.move((self.X, self.Y+1))
			if not pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
				self.state = "falling"
			self.move(lastlocation)

		# Else fall
		if self.state == "falling":
			if self.speedY < 3:
				self.speedY = 5
			self.speedY = self.speedY * 1.2
			self.move((self.X, self.Y + self.speedY))
			if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
				self.state = "ground"
				Y = pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks).xy[1]-self.image.get_height()
				self.move((self.X, Y))
				self.speedY = 0
				


		# Out of bounds Y
		if self.Y > globs.currentregion.pixelHeight:
			self.move((self.xy[0], globs.currentregion.pixelHeight))
		elif self.Y < 0:
			self.move((self.xy[0], 0))
		# Out of bounds X
		if self.X > globs.currentregion.pixelWidth:
			self.move((globs.currentregion.pixelWidth, self.xy[1]))
		elif self.X < 0:
			self.move((0, self.xy[1]))

	def sprint(self):
		sprintbonus = 1.20
		self.speedX *= sprintbonus

	def jump(self):
		# If not going up
		if self.state == "ground":
			self.speedY = -55
			self.state = "jumping"

	def action(self):
		if pygame.sprite.spritecollideany(self, globs.currentgame.entities):
			print("Action!")

	def worldAction(self):
		collisionItem = pygame.sprite.spritecollideany(self, globs.currentgame.worldEntities)
		if collisionItem:
			collisionItem.action()