import pygame
from .baseclasses import Sprite

class Character(Sprite):
	def __init__(self, parent, xy, wh):
		Sprite.__init__(self, parent, xy, wh, bgColor=(255,255,255))

		self.forceX = 0
		self.forceY = 0

	def collision(self):
		if self.forceX:
			pass
		if self.forceY:
			pass

	def jump(self):
		pass
