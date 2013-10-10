import pygame
from .baseclasses import Sprite
import globals as globs

class Character(Sprite):
	def __init__(self, parent, xy):
		Sprite.__init__(self, parent, xy, (40,80), bgColor=(255,255,255))

		self.speedX = 0.0
		self.speedY = 0.0

		self.facefacing = "front"
		self.bodyfacing = "right"

		self.state = "falling"

		headR = 10
		headY = headR
		headX = (self.image.get_width()/2)

		pygame.draw.circle(self.image, (0,0,0), (headX, headY), headR)


		bodyH = 35
		bodyW = 15
		bodyY = 40
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
		self.move((self.X+int(self.speedX), self.Y))
		if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
			#print("Collide!!! {}".format(pygame.sprite.spritecollide(self, globs.currentgame.worldBlocks, dokill=False)))
			if self.speedX > 0:
				x = pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks).xy[0]-self.image.get_width()
			elif self.speedX < 0:
				x = pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks).xy[0]+50
			self.move((x, self.Y))
			self.speedX = 0
		self.speedX = self.speedX / 1.2

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
				self.speedY /= globs.clock.get_fps()/52

		# If on ground
		elif self.state == "ground":
			# See if block under feet
			self.move((self.X, self.Y+1))
			if not pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
				self.state = "falling"
			self.move(lastlocation)

		# Else fall
		if self.state == "falling":
			if self.speedY < 1:
				self.speedY = 1
			self.speedY *= globs.clock.get_fps()/52
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
		if self.state == "ground":
			sprintbonus = globs.clock.get_fps()/58
			self.speedX *= sprintbonus

	def jump(self):
		# If not going up
		if self.state == "ground":
			self.speedY = -15
			self.state = "jumping"

	def run(self, direction):
		force = 2
		if direction == "left":
			globs.character.speedX -= force
		elif direction == "right":
			globs.character.speedX += force

	def action(self):
		if pygame.sprite.spritecollideany(self, globs.currentgame.entities):
			print("Action!")

	def worldAction(self):
		collisionItem = pygame.sprite.spritecollideany(self, globs.currentgame.worldEntities)
		if collisionItem:
			collisionItem.action()