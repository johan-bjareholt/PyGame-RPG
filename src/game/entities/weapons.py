from .baseclasses import *

class MeleeWeapon(Entity):
	def __init__(self, parent, owner, xy, wh, damage, push):
		Entity.__init__(self, parent, xy, wh, add=False)

class Sword(MeleeWeapon):
	def __init__(self, parent, owner, damage, push):
		xy = (0,0)
		wh = (20,50)
		MeleeWeapon.__init__(self, parent, owner, xy, wh, damage, push)
		self.image.fill((255,100,255))
		self.owner = owner
		self.r = 0
		self.original_image = self.image

	def blit(self):
		#self.move((self.owner.xy[0]+self.owner.image.get_width(), self.owner.xy[1]), placement='midbottom')
		self.image = pygame.transform.rotate(self.original_image, self.r)
		self.r -= 1
		if self.r < -90:
			self.r = 0
		self.rect.midbottom = (self.owner.rect.x+self.owner.image.get_width(), self.owner.rect.y+(self.owner.image.get_height()/2))
		self.worldBlit()