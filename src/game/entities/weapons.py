from .baseclasses import *

class MeleeWeapon(Entity):
	def __init__(self, parent, owner, wh, damage, speed, push):
		Entity.__init__(self, parent, (0,0), wh, add=False)

		# Stats
		self.damage = damage
		self.speed = speed
		self.push = push

		self.owner = owner
		self.r = 0
		self.is_attacking = False
		self.original_image = self.image
		self.draw()

	def blit(self):
		# Rotation
		if self.is_attacking:
			self.r -= 4
			if self.r < -90:
				self.r = 0
				self.is_attacking = False
				self.image = self.original_image

		if self.owner.facing == "left":
			xy = (self.owner.rect.x+self.owner.image.get_width(), self.owner.rect.y+(self.owner.image.get_height()/2))
			if self.r:
				self.image = pygame.transform.rotate(self.original_image, self.r)
			self.rect = self.image.get_rect(bottomleft=xy)
		elif self.owner.facing == "right":
			xy = (self.owner.rect.x, self.owner.rect.y+(self.owner.image.get_height()/2))
			if self.r:
				self.image = pygame.transform.rotate(self.original_image, -self.r)
			self.rect = self.image.get_rect(bottomright=xy)
		self.worldBlit()

	def attack(self):
		self.is_attacking = True

	def draw(self):
		pass

class Sword(MeleeWeapon):
	def __init__(self, parent, owner):
		wh = (20,60)
		damage = 10
		speed = 10
		push = 10
		MeleeWeapon.__init__(self, parent, owner, wh, damage, speed, push)

	def draw(self):
		self.image.fill((255,0,255))
		self.image.set_colorkey((255,0,255))
		weaponimg = pygame.image.load(globs.datadir+"/png/weapons/sword.png").convert_alpha()
		self.image.blit(weaponimg, (0,0))

class LongSword(MeleeWeapon):
	def __init__(self, parent, owner):
		wh = (20,90)
		damage = 10
		speed = 10
		push = 10
		MeleeWeapon.__init__(self, parent, owner, wh, damage, speed, push)

	def draw(self):
		self.image.fill((255,0,255))
		self.image.set_colorkey((255,0,255))
		weaponimg = pygame.image.load(globs.datadir+"/png/weapons/longsword.png").convert_alpha()
		self.image.blit(weaponimg, (0,0))