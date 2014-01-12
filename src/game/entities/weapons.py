from .baseclasses import *
import math

class Weapon(Entity):
	def __init__(self, owner, wh, inhand, damage=0, push=0):
		self.owner = owner

		self.equipped = True
		self.attacking = False
		self.owner = owner

		Entity.__init__(self, (0,0), wh, add=not inhand)
		if not inhand:
			globs.currentgame.lethals.add(self)

		self.hitting = []

		# Stats
		self.damage = damage
		self.push = push

	def attack(self):
		pass

	def unattack(self):
		pass

class MeleeWeapon(Weapon):
	def __init__(self, owner, wh, damage, speed, push):
		Weapon.__init__(self, owner, wh, True, damage, push)

		self.speed = speed
		#self.direction =

		self.equipped = False
		self.r = 0
		self.attacking = False
		self.original_image = self.image
		self.draw()

	def events(self):
		isHurting()

	def hit(self, target):
		# Push
		speedX = self.push
		if self.owner.facing == "right":
			speedX = -speedX
		target.speedX += speedX

		# Remove health
		target.health -= self.damage

	def isHurting(self):
		collidedItems = pygame.sprite.spritecollide(self, globs.currentgame.living_entities, False)
		for collidedItem in collidedItems:
			if collidedItem and collidedItem != self.owner:
				#print(str(self) + " and " + str(collidedItem))
				self.hit(collidedItem)
				globs.currentgame.lethals.remove(self)

	def blit(self):
		# Rotation
		if self.equipped:
			if self.attacking:
				self.r -= self.speed
				if self.r < -90:
					self.r = 0
					self.attacking = False
					self.image = self.original_image
					for entity in self.hitting:
						entity.hitted.remove(self.owner)
					self.hitting = []
					globs.currentgame.lethals.remove(self)

			if self.owner.facing == "left":
				xy = (self.owner.rect.x+self.owner.image.get_width(), self.owner.rect.y+(self.owner.image.get_height()/2))
				self.image = pygame.transform.rotate(self.original_image, self.r)
				self.rect = self.image.get_rect(bottomleft=xy)
			elif self.owner.facing == "right":
				xy = (self.owner.rect.x, self.owner.rect.y+(self.owner.image.get_height()/2))
				self.image = pygame.transform.rotate(self.original_image, -self.r)
				self.rect = self.image.get_rect(bottomright=xy)
		else:
			xy = (self.owner.rect.x-(self.image.get_width()/2)+(self.owner.image.get_width()/2), self.owner.rect.y)
			self.image = pygame.transform.rotate(self.original_image, 210)
			self.rect = self.image.get_rect(topleft=xy)
		self.worldBlit()


	def attack(self):
		self.attacking = True
		globs.currentgame.lethals.add(self)

	def equip(self):
		self.equipped = True
		globs.load_cursor("SwordCursor_black")

	def unequip(self):
		self.equipped = False
		globs.currentgame.lethals.remove(self)
		globs.load_cursor("CircleCursor_black")

	def draw(self):
		pass

class Sword(MeleeWeapon):
	def __init__(self, owner):
		wh = (20,60)
		damage = 6
		speed = 6
		push = 10
		MeleeWeapon.__init__(self, owner, wh, damage, speed, push)

	def draw(self):
		self.image.fill((255,0,255))
		self.image.set_colorkey((255,0,255))
		weaponimg = pygame.image.load(globs.datadir+"/png/weapons/sword.png").convert_alpha()
		self.image.blit(weaponimg, (0,0))

class LongSword(MeleeWeapon):
	def __init__(self, owner):
		wh = (20,90)
		damage = 10
		speed = 4
		push = 15
		MeleeWeapon.__init__(self, owner, wh, damage, speed, push)

	def draw(self):
		self.image.fill((255,0,255))
		self.image.set_colorkey((255,0,255))
		weaponimg = pygame.image.load(globs.datadir+"/png/weapons/longsword.png").convert_alpha()
		self.image.blit(weaponimg, (0,0))

class Bow(Weapon):
	def __init__(self, owner):
		wh = (30,60)
		Weapon.__init__(self, owner, wh, inhand=True)
		self.original_image = self.image
		self.r = 0
		self.minCharge = 12.0
		self.maxCharge = 30.0
		self.charge = 0
		self.lastmousepos = None
		self.projectiles = pygame.sprite.Group()

		self.held = 0

		self.draw()

	def draw(self):
		self.image.fill((255,0,255))
		self.image.set_colorkey((255,0,255))
		weaponimg = pygame.image.load(globs.datadir+"/png/weapons/longsword.png").convert_alpha()
		self.image.blit(weaponimg, (0,0))

	def blit(self):
		if self.equipped:
			# Bow rotation
			mousepos = list(pygame.mouse.get_pos())
			mousepos[0] -= globs.resolution[0]/2
			mousepos[1] -= globs.resolution[1]/2
			if mousepos[1] != 0:
				mouserel = mousepos[0]/float(mousepos[1])
				if mousepos[1] > 0:
					self.r = math.degrees(math.atan(mouserel))
				else:
					self.r = math.degrees(math.atan(mouserel))
				self.r -= 90
			if mousepos[1] < 0:
				self.r = self.r+180
			else:
				self.r = 360+self.r
			#print(self.r)

			x = self.owner.rect.center[0]
			if self.r < 180:
				x += (90-self.r)/2
			else:
				x -= (270-self.r)/2

			y = self.owner.rect.center[1]-10

			r = self.r
			if r < 180:
				if r > 90: r = abs(r-180)
				y -= r/3
			else:
				r -= 180
				if r > 90: r = abs(r-180)
				y += r/3

			bowxy = (x, y)
			self.image = pygame.transform.rotate(self.original_image, self.r)
			self.rect = self.image.get_rect(center=bowxy)

		else:
			xy = (self.owner.rect.x-(self.image.get_width()/2)+(self.owner.image.get_width()/2), self.owner.rect.y)
			self.image = pygame.transform.rotate(self.original_image, 210)
			self.rect = self.image.get_rect(topleft=xy)
		self.worldBlit()

	def isHurting(self):
		for projectile in self.projectiles:
			if projectile.attacking:
				projectile.checkHit()

	def attack(self):
		if self.charge == 0:
			self.projectile = Arrow(self.owner, -self.r, self.charge)
		self.charge += 1
		if self.charge > self.maxCharge:
			self.charge = self.maxCharge

	def unattack(self):
		self.attacking = True
		if self.charge > self.minCharge:
			self.projectile.shoot(self.charge)
			self.projectiles.add(self.projectile)
		else:
			self.projectile.kill()
			self.projectile = None
		self.charge = 0


class Projectile(Weapon):
	def __init__(self, owner, wh, direction, damage, speed, push):
		Weapon.__init__(self, owner, wh, False, damage, push)
		globs.currentgame.lethals.remove(self)
		self.original_image = self.image

		self.direction = direction
		self.attacking = False
		self.defaultremovetime = 5000
		self.removetime = self.defaultremovetime

		self.rect.center = owner.weapon.rect.center

		self.lasthitxy = None
		self.is_shot = False
		#if owner.facing == "left":
		#	self.rect.x += owner.image.get_width()+10
		#elif owner.facing == "right":
		#	self.rect.x = 10

		#self.rect.midright

	def shoot(self, speed):
		self.speedX = math.cos(math.radians(self.direction))*speed
		self.speedY = math.sin(math.radians(self.direction))*speed
		globs.currentgame.lethals.add(self)
		self.attacking = True
		self.is_shot = True

	def events(self):
		#self.movement()
		#CollidableEntity.movement(self)
		if not self.is_shot:
			self.rotate()
			self.moveCharge()
		elif self.attacking:
			self.moveShoot()
			self.checkOutOfBounds()
			self.rotate()
			self.checkHit()
		else:
			self.fade_away()

	def checkOutOfBounds(self):
		# Reaches bottom boundary
		if self.rect.y > globs.currentregion.pixelHeight-self.image.get_height():
			self.kill()
		# Reaches top boundary
		elif self.rect.y < 0:
			self.kill()

	def rotate(self):
		self.r = -self.direction
		self.image = pygame.transform.rotate(self.original_image, self.r)

	def moveRotate(self):
		self.r = math.degrees(math.atan(self.speedY/self.speedX))
		self.image = pygame.transform.rotate(self.original_image, self.r)

	def hit(self, target):
		# Push
		speedX = self.push
		if self.speedX < 0:
			speedX = -speedX
		target.speedX += speedX

		# Remove health
		target.health -= self.damage

	def checkHit(self):
		if self.hitting:
			# Stop attacking
			self.attacking = False
			globs.currentgame.lethals.remove(self)
			self.lasthitxy = self.hitting[0].rect.topleft
		else:
			if self.attacking:
				collidedItems = pygame.sprite.spritecollide(self, globs.currentgame.living_entities, False)
				for collidedItem in collidedItems:
					if collidedItem and collidedItem != self.owner and collidedItem != self:
						#print(str(self) + " and " + str(collidedItem))
						self.hit(collidedItem)
						globs.currentgame.lethals.remove(self)
						self.attacking = False
				if self.colliding_blocks():
				#if pygame.sprite.spritecollideany(self, globs.currentgame.collidableBlocks):
					self.attacking = False


	def moveCharge(self):
		percentage = self.owner.weapon.charge/self.owner.weapon.maxCharge

		movemax = 50

		#print(self.direction)
		x = math.cos(math.radians(self.r))/math.pi
		#print(x)
		x = (x/180)*movemax*percentage
		y = math.sin(math.radians(self.r))/math.pi
		#print(y)
		y = (y/180)*movemax*percentage
		#print("x:" + str(x) + " y:" + str(y))



		self.rect.center = (self.owner.weapon.rect.center[0]+x,
							self.owner.weapon.rect.center[1]+y)

		self.direction = -self.owner.weapon.r

	def moveShoot(self):
		self.rect.x += self.speedX
		self.rect.y += self.speedY
		self.speedY += globs.clock.get_time()/80.0
		if self.speedX > 0:
			#self.speedX -= globs.clock.get_time()/160.0
			self.speedX -= self.speedY*globs.clock.get_time()/1200.0
		elif self.speedX < 0:
			#self.speedX += globs.clock.get_time()/160.0
			self.speedX += self.speedY*globs.clock.get_time()/1200.0
		#print(globs.clock.get_time()/1200.0)

	def fade_away(self):
		self.removetime -= globs.clock.get_time()
		#print(globs.clock.get_time())
		if self.removetime < 0:
			self.kill()
		alpha = (float(self.removetime)/self.defaultremovetime)*255
		#print(alpha)
		self.image.set_alpha(alpha)

		if self.hitting:
			hitxy = self.hitting[0].rect.topleft
			if self.lasthitxy:
				hitxy = (hitxy[0]-self.lasthitxy[0], hitxy[1]-self.lasthitxy[1])
			self.rect.topleft = (self.rect.topleft[0]+hitxy[0], self.rect.topleft[1]+hitxy[1])
			#self.rect.x = self.hitting[0].rect.x
			self.lasthitxy = self.hitting[0].rect.topleft

	def colliding_blocks(self):
		x = self.rect.x/50
		maxx = (self.rect.x+self.image.get_width())/50
		possible_x = []
		for iteration in range(x, maxx+1):
			possible_x.append(iteration)
		#print(possible_x)

		y = (self.rect.y)/50
		maxy = (self.rect.y+self.image.get_height())/50
		possible_y = []
		for iteration in range(y, maxy+1):
			possible_y.append(iteration)
		#print(possible_y)
		for x in possible_x:
			for y in possible_y:
				try:
					block = globs.currentregion.renderedmap[y][x]
					if block and block.collidable:
						if self.rect.colliderect(block.rect):
							return block
				except IndexError:
					pass

class Arrow(Projectile):
	def __init__(self, owner, direction, speed, inhand=False):
		damage = 10
		push = 20
		wh = (25,8)
		#print("Arrow!")
		Projectile.__init__(self, owner, wh, direction, damage, speed, push)