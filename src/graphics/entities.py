import pygame
from .baseclasses import Sprite
import globals as globs

class Character(Sprite):
	def __init__(self, parent, xy):
		Sprite.__init__(self, parent, xy, (50,75), bgColor=(255,255,255))

		self.forceX = 0
		self.forceY = 0

	def collision(self):
		# Right/left
		lastlocation = self.xy
		self.move((self.X+self.forceX, self.Y))
		if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
			#print("Collide!!! {}".format(pygame.sprite.spritecollide(self, globs.currentgame.worldBlocks, dokill=False)))
			self.move(lastlocation)
		self.forceX = 0

		# up/down
		lastlocation = self.xy
		self.move((self.X, self.Y+2))
		# If jumping up
		if self.forceY > 0:
			print("Jumping")
			self.forceY = self.forceY / 0.95
			self.move((self.X, self.Y-self.forceY))
			# If collide with something
			if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
				self.forceY = 0
				self.move(lastlocation)

		# If on ground
		elif pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
			print("On ground")
			print(pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks))
			self.move(lastlocation)
			# If stuck
			while pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
				collidedSprite = pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks)a
				self.move((self.X, ))
		# Else fall		
		else:
			print("Falling")
			if self.forceY == 0:
				self.forceY = -2
			else:
				self.forceY = self.forceY*1.2
				if self.forceY > -25:
					self.forceY = -25
			self.move((self.X, self.Y-self.forceY))
		print(self.forceY)

		#self.move((self.X, self.Y+self.forceY+5))
		#if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
		#	#print("Collide!!! {}".format(pygame.sprite.spritecollide(self, globs.currentgame.worldBlocks, dokill=False)))
		#	self.move(lastlocation)

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

	def jump(self):
		# If not going up
		if not self.forceY < 0:
			self.forceY = 25
