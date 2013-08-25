# All blocks on map

import pygame

from .baseclasses import Surface

class Block(Surface):
	def __init__(self, layer, wh=(50,50), bgColor=None, alpha=None):
		Surface.__init__(self, wh)
		# Layer
		# When the blocks are being blitted, 
		# layer 0-9   = world background
		# layer 10-19 = world
		# layer 20-29 = foreground world
		# layer 30-39 = UI
		# layer 40-49 = UI foreground
		self.layer = layer

		if bgColor:
			self.fill(bgColor)
		if alpha:
			self.set_alpha(alpha)

class Block_00(Block):
	'''
	Stone
	'''
	def __init__(self):
		layer = 2
		Block.__init__(self, layer, bgColor=(150,150,150))

class Block_01(Block):
	'''
	Dirt
	'''
	def __init__(self):
		layer = 3
		Block.__init__(self, layer, bgColor=(65,55,40))

class Block_02(Block):
	'''
	Dirt with grass
	'''
	def __init__(self):
		layer = 4
		Block.__init__(self, layer, bgColor=(50,200,50))

class Block_10(Block):
	'''
	Glass
	'''
	def __init__(self):
		layer = 5
		Block.__init__(self, layer, bgColor=(0,0,0), alpha=2)