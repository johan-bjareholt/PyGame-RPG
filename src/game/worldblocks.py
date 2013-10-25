# All blocks on map

import pygame
import globals as globs

from graphics.baseclasses import Surface

class Block(pygame.sprite.Sprite):
	def __init__(self, xy, flags=[], wh=(50,50), bgColor=None, alpha=None):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface(wh)
		self.xy = xy
		self.rect = self.image.get_rect(topleft=self.xy)

		self.bgColor = bgColor

		if not 'uncollidable' in flags:
			globs.currentgame.collidableBlocks.add(self)
		if 'actionBlock' in flags:
			globs.currentgame.actionBlocks.add(self)
		if 'worldActionBlock' in flags:
			globs.currentgame.worldActionBlocks.add(self)

		if bgColor:
			self.image.fill(self.bgColor)
		if alpha:
			self.image.set_alpha(alpha)

class Block_000(Block):
	'''
	Stone
	'''
	def __init__(self, xy):
		Block.__init__(self, xy, bgColor=(150,150,150))

class Block_001(Block):
	'''
	Dirt
	'''
	def __init__(self, xy):
		Block.__init__(self, xy, bgColor=(65,55,40))

class Block_002(Block):
	'''
	Grass
	'''
	def __init__(self, xy):
		Block.__init__(self, xy, bgColor=(50,200,50))

class Block_010(Block):
	'''
	Bush
	'''
	def __init__(self, xy):
		Block.__init__(self, xy, bgColor=(30,150,30), flags=['uncollidable', 'actionBlock'])

class Block_020(Block):
	'''
	Wood
	'''
	def __init__(self, xy):
		Block.__init__(self, xy, bgColor=(90,70,55), flags=['uncollidable'])
		pygame.draw.line(self.image, (0,0,0), (0,0), (50,0))

class Block_021(Block):
	'''
	Wood Vertical
	'''
	def __init__(self, xy):
		Block.__init__(self, xy, bgColor=(70,60,48), flags=['uncollidable'])
		pygame.draw.line(self.image, (0,0,0), (0,0), (0,50))

class Block_022(Block):
	'''
	Wooden Door Top
	'''
	def __init__(self, xy):
		Block.__init__(self, xy, bgColor=(100,75,60), flags=['uncollidable'])
		pygame.draw.line(self.image, (0,0,0), (0,0), (49,0))
		pygame.draw.line(self.image, (0,0,0), (0,0), (0,49))
		pygame.draw.line(self.image, (0,0,0), (49,0), (49,49))
		pygame.draw.circle(self.image, (50,50,50), (40,40), 7)

class Block_023(Block):
	'''
	Wooden Door Bottom
	'''
	def __init__(self, xy):
		Block.__init__(self, xy, bgColor=(100,75,60), flags=['uncollidable', 'action'])
		pygame.draw.line(self.image, (0,0,0), (0,0), (0,49))
		pygame.draw.line(self.image, (0,0,0), (49,0), (49,49))


class Block_050(Block):
	'''
	Glass
	'''
	def __init__(self, xy):
		Block.__init__(self, xy, bgColor=(255,255,255), alpha=150)

class Block_150(Block):
	'''
	Background Glass
	'''
	def __init__(self, xy):
		Block.__init__(self, xy, bgColor=(255,255,255), alpha=150, flags=['uncollidable'])