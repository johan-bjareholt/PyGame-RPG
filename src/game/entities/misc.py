import pygame
import globals as globs


from .baseclasses import *



class BouncyBall(CollidableEntity):
	def __init__(self, xy, radius=20):
		CollidableEntity.__init__(self, xy, (radius*2,radius*2), (255,0,255), bounce=0.8)
		self.image.set_colorkey((255,0,255))
		pygame.draw.circle(self.image, (255,0,0), (radius,radius), radius)

class SmallBouncyBall(BouncyBall):
	def __init__(self, xy):
		BouncyBall.__init__(self, xy, radius=15)

class BigBouncyBall(BouncyBall):
	def __init__(self, xy):
		BouncyBall.__init__(self, xy, radius=30)


class WoodenStairs(Entity):
	def __init__(self, xy, h):
		Entity.__init__(self, xy, (50,50*h), (255,0,255))
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
	def __init__(self, xy, wh):
		Entity.__init__(self, xy, wh, (255,0,255))
		#self.image.fill((255,255,255))
		self.draw()

	def draw(self):
		self.image.fill((255,0,255))
		self.image.set_colorkey((255,0,255))
		self.image.convert_alpha()
		tree = pygame.image.load(globs.datadir+"/png/entities/tree.png").convert_alpha()
		self.image.blit(tree, (0,0))

class DeadTree(Entity):
	def __init__(self, xy, wh):
		Entity.__init__(self, xy, wh, (255,0,255))
		#self.image.fill((255,255,255))
		self.draw()

	def draw(self):
		self.image.fill((255,0,255))
		self.image.set_colorkey((255,0,255))
		tree = pygame.image.load(globs.datadir+"/png/entities/dead_tree.png").convert_alpha()
		self.image.blit(tree, (0,0))


class Sign(Entity):
	def __init__(self, xy, text):
		Entity.__init__(self, xy, (100,100), (255,0,255))
		globs.currentgame.climbableBlocks.add(self)
		#self.image.fill((255,255,255))
		self.text = text
		self.draw()

	def draw(self):
		self.image.fill((255,0,255))
		self.image.set_colorkey((255,0,255))
		sign = pygame.image.load(globs.datadir+"/png/entities/sign.png").convert_alpha()
		self.image.blit(sign, (0,0))

		signtopleft = (7,10)
		signbottomright = (93,70)

		font = globs.getFont("calibri", 12)
		for line, linetext in enumerate(self.text.split("\n")):
			renderedtext = font.render(linetext, True, pygame.color.Color(0, 0, 0))
			self.image.blit(renderedtext, ((self.image.get_width()/2)-(renderedtext.get_width()/2),signtopleft[1]+3+(line*12)))


class TeleportationPad(Entity):
	def __init__(self, xy, location):
		Entity.__init__(self, xy, (50,100), (255,0,255))
		self.targetLocation = location

		self.updateClickPosition()
		#globs.currentgame.clickableEntities.add(self.clickSprite)

	def events(self):
		self.updateClickPosition()

	def clicked(self):
		globs.location = self.targetLocation