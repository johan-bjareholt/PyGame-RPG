import world1

from graphics.baseclasses import Sprite


class Region(list):
	def __init__(self, name, spawn, world, entities):
		self.spawnCoordinates = spawn
		self.name = name
		self[:] = world
		self.entities = entities

		self.pixelHeight = len(self)*50
		self.pixelWidth   = len(self[0])*50

		self.blockHeight = len(self)
		self.blockWidth   = len(self[0])

	def loadBlocks(self):
		rowcount = 1
		for row in self.region:
			tilecount = 1
			for tile in row:
				if tile != "   ":
					self.append([self.loadedTiles[tile], self.blockPixel(tilecount, rowcount)])
					self.worldSurface.blit(self.loadedTiles[tile], (self.blockPixel(tilecount, rowcount)))
			tilecount += 1
		rowcount += 1



class WorldEntity(Sprite):
	def __init__(self, parent, xy, wh, bgColor=None):
		Sprite.__init__(self, parent, xy, wh, bgColor)

	def action(self):
		pass

class ExampleEntity(WorldEntity):
	def __init__(self, parent, xy):
		WorldEntity.__init__(self, parent, xy, (50,50), bgColor=(30,150,30))

	def action(self):
		pass