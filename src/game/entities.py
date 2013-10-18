import pygame
from graphics.baseclasses import Sprite
import globals as globs

import characters

class Character(Sprite):
	def __init__(self, parent, xy):
		Sprite.__init__(self, parent, xy, (40,80), bgColor=(255,255,255))

		self.attributes = characters.load(globs.charactername)
		print(self.attributes)

		self.speedX = 0.0
		self.speedY = 0.0

		self.forceY = 0.0

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
		# Offensive: Swordfighting, Marksmanship, Destruction
		# Defensive: Heavy Armor, Light Armor, Restoration

	def loop(self):
		self.collision()

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
			self.speedX = 0
		else:
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
		if self.Y > globs.currentregion.pixelHeight:
			self.move((self.xy[0], globs.currentregion.pixelHeight))
			self.speedY = 0
		elif self.Y < 0:
			self.move((self.xy[0], 0))
			self.speedY = 0
		# Out of bounds X
		if self.X > globs.currentregion.pixelWidth:
			self.move((globs.currentregion.pixelWidth, self.xy[1]))
			self.speedX = 0
		elif self.X < 0:
			self.move((0, self.xy[1]))
			self.speedX = 0

		#print("ms since last frame:{} gravityequation: {} speedY: {}".format(globs.ticktime, gravityequation, self.speedY))
		#print(self.state)


	def sprint(self):
		if self.state == "ground":
			sprintbonus = 1.1
			self.speedX *= sprintbonus

	def jump(self):
		# If not going up
		if self.state == "ground":
			self.speedY = -25
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