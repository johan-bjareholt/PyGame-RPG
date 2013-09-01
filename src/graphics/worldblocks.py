# All blocks on map

import pygame
import globals as globs

from .baseclasses import Surface

class Block(pygame.sprite.Sprite):
	def __init__(self, layer, xy, flags=[], wh=(50,50), bgColor=None, alpha=None):
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

		if not 'uncollidable' in flags:
			globs.currentgame.collidableBlocks.add(self)

		if bgColor:
			self.image.fill(bgColor)
		if alpha:
			self.image.set_alpha(alpha)

class Block_000(Block):
	'''
	Stone
	'''
	def __init__(self, xy):
		layer = 2
		Block.__init__(self, layer, xy, bgColor=(150,150,150))

class Block_001(Block):
	'''
	Dirt
	'''
	def __init__(self, xy):
		layer = 3
		Block.__init__(self, layer, xy, bgColor=(65,55,40))

class Block_002(Block):
	'''
	Grass
	'''
	def __init__(self, xy):
		layer = 4
		Block.__init__(self, layer, xy, bgColor=(50,200,50))

class Block_020(Block):
	'''
	Wood
	'''
	def __init__(self, xy):
		layer = 3
		Block.__init__(self, layer, xy, bgColor=(90,70,55), flags=['uncollidable'])
		pygame.draw.line(self.image, (0,0,0), (0,0), (50,0))

class Block_021(Block):
	'''
	Wood Vertical
	'''
	def __init__(self, xy):
		layer = 3
		Block.__init__(self, layer, xy, bgColor=(70,60,48), flags=['uncollidable'])
		pygame.draw.line(self.image, (0,0,0), (0,0), (0,50))

class Block_022(Block):
	'''
	Wooden Door Top
	'''
	def __init__(self, xy):
		layer = 3
		Block.__init__(self, layer, xy, bgColor=(100,75,60), flags=['uncollidable'])
		pygame.draw.line(self.image, (0,0,0), (0,0), (49,0))
		pygame.draw.line(self.image, (0,0,0), (0,0), (0,49))
		pygame.draw.line(self.image, (0,0,0), (49,0), (49,49))
		pygame.draw.circle(self.image, (50,50,50), (40,40), 7)

class Block_023(Block):
	'''
	Wooden Door Bottom
	'''
	def __init__(self, xy):
		layer = 3
		Block.__init__(self, layer, xy, bgColor=(100,75,60), flags=['uncollidable'])
		pygame.draw.line(self.image, (0,0,0), (0,0), (0,49))
		pygame.draw.line(self.image, (0,0,0), (49,0), (49,49))


class Block_050(Block):
	'''
	Glass
	'''
	def __init__(self, xy):
		layer = 5
		Block.__init__(self, layer, xy, bgColor=(255,255,255), alpha=150)

class Block_150(Block):
	'''
	Background Glass
	'''
	def __init__(self, xy):
		layer = 5
		Block.__init__(self, layer, xy, bgColor=(255,255,255), alpha=150, flags=['uncollidable'])