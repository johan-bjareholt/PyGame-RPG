import pygame
from .baseclasses import Sprite

class Character(Sprite):
	def __init__(self, parent, xy, wh):
		Sprite.__init__(self, parent, xy, wh, bgColor=(255,255,255))