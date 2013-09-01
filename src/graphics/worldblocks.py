# All blocks on map

import pygame

from .baseclasses import Surface

class Block(pygame.sprite.Sprite):
	def __init__(self, layer, xy, wh=(50,50), bgColor=None, alpha=None):
		#Surface.__init__(self, wh)
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface(wh)
		self.xy = xy
		self.rect = self.image.get_rect(topleft=self.xy)
		# Layer
		# When the blocks are being blitted, 
		# layer 0-9   = world background
		# layer 10-19 = world
		# layer 20-29 = foreground world
		# layer 30-39 = UI
		# layer 40-49 = UI foreground
		self.layer = layer

		if bgColor:
			self.image.fill(bgColor)
		if alpha:
			self.image.set_alpha(alpha)

class Block_00(Block):
	'''
	Stone
	'''
	def __init__(self, xy):
		layer = 2
		Block.__init__(self, layer, xy, bgColor=(150,150,150))

class Block_01(Block):
	'''
	Dirt
	'''
	def __init__(self, xy):
		layer = 3
		Block.__init__(self, layer, xy, bgColor=(65,55,40))

class Block_02(Block):
	'''
	Dirt with grass
	'''
	def __init__(self, xy):
		layer = 4
		Block.__init__(self, layer, xy, bgColor=(50,200,50))

class Block_10(Block):
	'''
	Glass
	'''
	def __init__(self, xy):
		layer = 5
		Block.__init__(self, layer, xy, bgColor=(0,0,0), alpha=2)