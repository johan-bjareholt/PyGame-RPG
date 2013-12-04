import pygame
import globals as globs


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


class WoodenStairs(Entity):
	def __init__(self, parent, xy, h):
		Entity.__init__(self, parent, xy, (50,50*h), (255,0,255))
		self.h = h
		globs.currentgame.climbableBlocks.add(self)
		#self.image.fill((255,255,255))
		self.draw()

	def draw(self):
		self.stairs = pygame.image.load(globs.datadir+"/png/entities/stairs.png")
		self.stairs.convert()
		self.stairs.convert_alpha()

		for h in range(self.h):
			self.image.blit(self.stairs, (0,h*50))


class Tree(Entity):
	def __init__(self, parent, xy, wh):
		Entity.__init__(self, parent, xy, wh, (255,0,255))
		globs.currentgame.climbableBlocks.add(self)
		#self.image.fill((255,255,255))
		self.draw()

	def draw(self):
		self.image.fill((255,0,255))
		self.image.set_colorkey((255,0,255))
		self.image.convert_alpha()
		tree = pygame.image.load(globs.datadir+"/png/entities/tree.png").convert_alpha()
		self.image.blit(tree, (0,0))

class DeadTree(Entity):
	def __init__(self, parent, xy, wh):
		Entity.__init__(self, parent, xy, wh, (255,0,255))
		globs.currentgame.climbableBlocks.add(self)
		#self.image.fill((255,255,255))
		self.draw()

	def draw(self):
		self.image.fill((255,0,255))
		self.image.set_colorkey((255,0,255))
		tree = pygame.image.load(globs.datadir+"/png/entities/dead_tree.png").convert_alpha()
		self.image.blit(tree, (0,0))


class TeleportationPad(Entity):
	def __init__(self, parent, xy, location):
		Entity.__init__(self, parent, xy, (50,100), (255,0,255))
		self.targetLocation = location

		self.clickSprite = Sprite(self, (0,0), (self.image.get_width(), self.image.get_height()))
		self.clickSprite.clicked = self.clicked
		self.updateClickPosition()
		globs.currentgame.clickableEntities.add(self.clickSprite)

	def events(self):
		self.updateClickPosition()

	def updateClickPosition(self):
		x = self.rect.x-globs.cameraX
		y = self.rect.y-globs.cameraY
		self.clickSprite.rect.topleft = (x, y)

	def clicked(self):
		globs.location = self.targetLocation