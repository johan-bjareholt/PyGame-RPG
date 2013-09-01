import pygame
from .baseclasses import Sprite
import globals as globs

class Character(Sprite):
	def __init__(self, parent, xy):
		Sprite.__init__(self, parent, xy, (75,100), bgColor=(255,255,255))

		self.forceX = 0
		self.forceY = 0

	def collision(self):
		# Right/left
		lastlocation = self.xy
		self.move((self.X+self.forceX, self.Y))
		if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
			#print("Collide!!! {}".format(pygame.sprite.spritecollide(self, globs.currentgame.worldBlocks, dokill=False)))
			self.move(lastlocation)

		# up/down
		lastlocation = self.xy
		self.move((self.X, self.Y+self.forceY+5))
		if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
			#print("Collide!!! {}".format(pygame.sprite.spritecollide(self, globs.currentgame.worldBlocks, dokill=False)))
			self.move(lastlocation)

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

		self.forceY = 0 
		self.forceX = 0

	def jump(self):
		pass
