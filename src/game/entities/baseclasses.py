import pygame
from graphics.baseclasses import Sprite
import globals as globs

class Entity(Sprite):
	def __init__(self, xy, wh, bgColor=None, add=True):
		Sprite.__init__(self, xy, wh)

		if bgColor:
			self.image.fill(bgColor)
		if add:
			globs.currentgame.entities.add(self)

	def events(self):
		pass


class CollidableEntity(Entity):
	def __init__(self, xy, wh, bgColor, bounce=0.0, force=None, add=True):
		Entity.__init__(self, xy, wh, bgColor, add)

		if add:
			globs.currentgame.collidableEntities.add(self)

		self.spawnxy = xy

		self.speedX = 0.0
		self.speedY = 1.0
		self.bounce = bounce
		self.mass = wh[0]*wh[1]
		self.force = force
		print(self.mass)

	def get_force(self):
		if not self.force:
			return self.speedX*self.mass, self.speedY*self.mass
		else:
			return self.force

	def movement(self):
		globs.currentgame.collidableEntities.remove(self)

		# Horizontal

		for speed in self.movement_steps(self.speedX, self.image.get_width()):
			self.collidingX(speed)
		# Check if on ground
		a = (globs.clock.get_time()/(20.0*7))
		self.speedX = self.accelerate(self.speedX, -a)
		if self.speedX < 0.5 and self.speedX > -0.5:
			self.speedX = 0

		# Vertical

		if self.speedY < 1 and self.speedY > -1:
			self.speedY = 1

		for speed in self.movement_steps(self.speedY, self.image.get_height()):
			self.collidingY(speed)


		# Out of bounds fix
		self.fixOutOfBounds()

		globs.currentgame.collidableEntities.add(self)

		# Acceleration
		#a = 0.1
		a = globs.clock.get_time()/150.0
		#print(a)
		if self.speedY < 0:
			# Jumping
			self.speedY = self.accelerate(self.speedY, -a)
		elif self.speedY > 0:
			# Falling
			self.speedY = self.accelerate(self.speedY, a)

		#print("ms since last frame:{} gravityequation: {} speedY: {}".format(globs.ticktime, gravityequation, self.speedY))

	def accelerate(self, direction, percentage):
		direction *= (1+percentage)
		return direction
		#print("acceleration: "+str(1+percentage) + "\t" + str(self))
		#print("Speed: "+str(self.speedY)+ "\t" + str(self))
		#print("xy: " + str(self.rect.topleft) + "\t" + str(self))

	def movement_steps(self, speed, height):
		mylist = []
		if speed < 0:
			for iteration in range(int(abs(speed)/height)-1):
				mylist.append(-height)
			num = int((speed%height)-height)
		elif speed > 0:
			for iteration in range(int(speed/height)-1):
				mylist.append(height)
			num = int(speed%height)
		else:
			return []
		mylist.append(num)
		return mylist

	def collidingX(self, speed):
		self.rect.x += speed

		# Entities
		collided_entity = pygame.sprite.spritecollideany(self, globs.currentgame.collidableEntities)
		while collided_entity:
			self.entityCollisionX(collided_entity)
			collided_entity = pygame.sprite.spritecollideany(self, globs.currentgame.collidableEntities)

		# Blocks
		collidingBlock = self.colliding_blocks()
		if collidingBlock:
			while collidingBlock:
				self.unstuckBlocksX(collidingBlock)
				collidingBlock = self.colliding_blocks()
			self.speedX *=self.bounce

	def collidingY(self, speed):
		self.rect.y += speed

		# Entities
		#if pygame.sprite.spritecollideany(self, globs.currentgame.collidableEntities):
		#	self.unstuckEntitiesY()
		for entity in self.colliding_entities():
			collided_entity = pygame.sprite.spritecollideany(self, globs.currentgame.collidableEntities)
			while collided_entity:
				self.entityCollisionY(collided_entity)
				collided_entity = pygame.sprite.spritecollideany(self, globs.currentgame.collidableEntities)

		# Blocks
		collidingBlock = self.colliding_blocks()
		if collidingBlock:
			while collidingBlock:
				self.unstuckBlocksY(collidingBlock)
				collidingBlock = self.colliding_blocks()
			# Sets speedY to 0 if bounce is off
			if self.speedY <= -1:
				# Jumping
				self.speedY = 1
			elif self.speedY >= 1:
				# Falling
				self.speedY *= -self.bounce

	def colliding_entities(self):
		entities = pygame.sprite.spritecollide(self, globs.currentgame.collidableEntities, False)
		return entities

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

	def unstuckBlocksY(self, collided_block):
		if collided_block:
			#print("Unstucking " + str(self) + " from block " + str(collided_block) + " in Y")
			#print("Before - s1: {} xy1: {} xy2:{}".format(self.speedY, self.rect.topleft, collided_block.rect.topleft))
			if self.speedY < 0:
				Y = collided_block.rect.y+collided_block.image.get_height()
			elif self.speedY > 0:
				Y = collided_block.rect.y-self.image.get_height()
			else:
				print("Colliding in Y without a speed in Y!")
			#print("After - s1: {} xy1: {} xy2: {}".format(self.speedY, self.rect.topleft, collided_block.rect.topleft))

			self.rect.y = Y

	def unstuckBlocksX(self, collided_block):
		if collided_block:
			#print("Unstucking " + str(self) + " from block " + str(collided_block) + " in X")
			#print("Before - s1: {} xy1: {} xy2:{}".format(self.speedX, self.rect.topleft, collided_block.rect.topleft))
			if self.speedX > 0:
				x = collided_block.rect.x-self.image.get_width()
			elif self.speedX < 0:
				x = collided_block.rect.x+collided_block.image.get_width()
			else:
				print("Colliding in X without a speed in X!")
			#print("After - s1: {} xy1: {} xy2: {}".format(self.speedX, self.rect.topleft, collided_block.rect.topleft))
			self.rect.x = x

	def unstuckEntitiesY(self, collided_entity):
		if collided_entity:
			print("Unstucking " + str(self) + " from entity " + str(collided_entity) + " in Y")
			print("s1: {} s2: {} xy1: {} xy2:{}".format(self.speedY, collided_entity.speedY, self.rect.topleft, collided_entity.rect.topleft))
			Y = self.rect.y
			if (self.rect.y+self.image.get_height())/2 > (collided_entity.rect.y+collided_entity.image.get_height())/2:
				print("3")
				Y = self.underOf(collided_entity)
			elif (self.rect.y+self.image.get_height())/2 < (collided_entity.rect.y+collided_entity.image.get_height())/2:
				print("4")
				Y = self.aboveOf(collided_entity)

			self.rect.y = Y

	def unstuckEntitiesX(self, collided_entity):
		if collided_entity:
			print("Unstucking " + str(self) + " from entity " + str(collided_entity) + " in X")
			print("s1: {} s2: {} xy1: {} xy2:{}".format(self.speedX, collided_entity.speedX, self.rect.topleft, collided_entity.rect.topleft))
			X = self.rect.x
			if (self.rect.x+self.image.get_width())/2 < (collided_entity.rect.x+collided_entity.image.get_width())/2:
				print("3")
				X = self.leftOf(collided_entity)
			elif (self.rect.x+self.image.get_width())/2 > (collided_entity.rect.x+collided_entity.image.get_width())/2:
				print("4")
				X = self.rightOf(collided_entity)

			self.rect.x = X

	def onGround(self):
		self.rect.y += 1
		if self.colliding_blocks() or self.colliding_entities()!=[]:
			onground = True
		else:
			onground = False
		self.rect.y -= 1
		return onground

	def bySide(self):
		byside = False
		# Right
		# Move
		self.rect.x += 1
		# Checks
		if self.colliding_blocks(): #or self.colliding_entities()!=[self]:
			byside = True

		#Left
		# Move
		self.rect.y -= 2
		# Checks
		if self.colliding_blocks(): #or self.colliding_entities()!=[self]:
			byside = True
		if self.rect.w+self.rect.y >= globs.resolution[0] or \
		   self.rect.y <= 0:
			byside = True
		self.rect.y += 1
		return byside

	def aboveOf(self, item):
		return item.rect.y-self.image.get_height()

	def underOf(self, item):
		return item.rect.y+item.image.get_height()

	def leftOf(self, item):
		return item.rect.x-self.image.get_width()

	def rightOf(self, item):
		return item.rect.x+item.image.get_width()

	def entityCollisionX(self, collided_entity):
		#print(self.speedX)

		p1 = self.get_force()[0]
		p2 = collided_entity.get_force()[0]
		if self.bySide():
			p1 = p2
			p2 = 0
			print("By side!")
		elif collided_entity.bySide():
			p1 = 0
			p2 = p1
			print("By side!")

		f1 = (p2/self.mass)/2
		f2 = (p1/collided_entity.mass)/2

		self.unstuckEntitiesX(collided_entity)

		if abs(p1) < abs(p2):
			self.speedX += f1
			collided_entity.speedX -= f2
		elif abs(p1) > abs(p2):
			collided_entity.speedX += f2
			self.speedX -= f1

	def entityCollisionY(self, collided_entity):
		#print(self.speedY)

		p1 = abs(self.get_force()[1])
		p2 = abs(collided_entity.get_force()[1])

		bounce = self.bounce
		if self.onGround:
			bounce = 1
		elif collided_entity.onGround():
			bounce = 0
		else:
			if self.bounce:
				bounce = self.bounce
				if collided_entity.bounce:
					bounce *= (1+collided_entity.bounce)
			elif collided_entity.bounce:
				bounce = collided_entity.bounce

		self.unstuckEntitiesY(collided_entity)

		if p1 < p2:
			self.speedY *= bounce
			collided_entity.speedY *= -bounce
		elif p2 < p1:
			collided_entity.speedY *= bounce
			self.speedY *= -bounce


	def fixOutOfBounds(self):
		# Out of bounds Y

		# Reaches bottom boundary
		if self.rect.y > globs.currentregion.pixelHeight-self.image.get_height():
			self.rect.topleft = (self.rect.x, globs.currentregion.pixelHeight-self.image.get_height())
			self.speedX *= -self.bounce
		# Reaches top boundary
		elif self.rect.y < 0:
			self.rect.topleft = (self.rect.x, 0)
			self.speedY = 1


		# Out of bounds X

		# Reaches left boundary
		if self.rect.x > globs.currentregion.pixelWidth-self.image.get_width():
			self.rect.topleft = (globs.currentregion.pixelWidth-self.image.get_width(), self.rect.y)
			self.speedX *= -self.bounce
		# Reaches right boundary
		elif self.rect.x < 0:
			self.rect.topleft = (0, self.rect.y)
			self.speedX *= -self.bounce

	def onCollide(self):
		pass


class LivingEntity(CollidableEntity):
	def __init__(self, xy, wh, health, add=True):
		CollidableEntity.__init__(self, xy, wh, (255,0,255), add=add)

		#self.attackArea = Sprite(parent, (0,0), (attackArea, attackArea))
		#print(self.attackArea)
		#self.updateAttackArea()

		self.maxhealth = health
		self.health = self.maxhealth
		self.lasthealth = None
		self.hitted = []

		if add:
			globs.currentgame.living_entities.add(self)

		# Initialize healthbar
		self.healthbar = Sprite((0,0), (self.image.get_width(), 5))

	def drawHealthbar(self):
		self.healthbar.image.fill((0,0,0))

		healthpercentage = float(self.health)/self.maxhealth

		w = self.healthbar.rect.w * healthpercentage
		newrect = pygame.Rect(0, 0, w, self.healthbar.rect.h)
		self.healthbar.image.fill((255,0,0), newrect)


	def blitHealthbar(self):
		xy = (self.rect.x, self.rect.y-10)

		if self.health != self.lasthealth:
			self.drawHealthbar()
		self.lasthealth = self.health

		self.healthbar.rect = self.healthbar.image.get_rect(topleft=xy)
		self.healthbar.worldBlit()

	def worldBlit(self):
		CollidableEntity.worldBlit(self)
		self.blitHealthbar()

	def isAlive(self):
		if self.health <= 0:
			return False
		return True

	def die(self):
		self.kill()
		print(str(self) + " died")
		for item in self.hitted:
			item.hitting = None
		print(self.hitted)

	def checkHurt(self):
		pass

		#collidedItems = pygame.sprite.spritecollide(self, globs.currentgame.lethals, False)
		#for collidedItem in collidedItems:
		#	print(collidedItem)
		#	if collidedItem and collidedItem.owner != self and collidedItem != self:
		#		print(collidedItem.__class__)
		#		print("hitted!")
		#		collidedItem.hit(self)

		#		# Needed so he is not hurt every frame the player is colliding with the lethal item
		#		self.hitted.append(collidedItem.owner)
		#		collidedItem.hitting.append(self)