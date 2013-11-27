import pygame
from graphics.baseclasses import Sprite
import globals as globs
import time

import game.characters

from .monsters import *
from .baseclasses import *


class BouncyBall(CollidableEntity):
	def __init__(self, parent, xy, radius=20):
		CollidableEntity.__init__(self, parent, xy, (radius*2,radius*2), (255,0,255), bounce=0.8)
		self.image.set_colorkey((255,0,255))
		pygame.draw.circle(self.image, (255,0,0), (radius,radius), radius)

class SmallBouncyBall(BouncyBall):
	def __init__(self, parent, xy):
		BouncyBall.__init__(self, parent, xy, radius=15)

class BigBouncyBall(BouncyBall):
	def __init__(self, parent, xy):
		BouncyBall.__init__(self, parent, xy, radius=30)

class TeleportationPad(Entity):
	def __init__(self, parent, xy):
		Entity.__init__(self, parent, xy, (50,100), (255,0,255))

		self.clickSprite = Sprite(self, (0,0), (self.image.get_width(), self.image.get_height()))
		self.clickSprite.clicked = self.clicked
		self.updateClickPosition()
		globs.currentgame.clickableEntities.add(self.clickSprite)

	def events(self):
		self.updateClickPosition()

	def updateClickPosition(self):
		xy = (self.xy[0]-globs.cameraX, 
			  self.xy[1]-globs.cameraY)
		self.clickSprite.move(xy)

	def clicked(self):
		globs.location = "game.world1_House"