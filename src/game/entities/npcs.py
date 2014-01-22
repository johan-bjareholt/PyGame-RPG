from game.entities.character import NPC

class Shopkeeper(NPC):
	def __init__(self, xy):
		NPC.__init__(self, xy)