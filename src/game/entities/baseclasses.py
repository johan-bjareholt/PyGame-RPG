import pygame
from graphics.baseclasses import Sprite
import globals as globs

class Entity(Sprite):
	def __init__(self, parent, xy, wh, bgColor, add=True):
		Sprite.__init__(self, parent, xy, wh, bgColor)

		if add:
			globs.currentgame.entities.add(self)

	def blit(self):
		blitxy = (self.xy[0]-globs.cameraX, 
			      self.xy[1]-globs.cameraY)
		globs.screen.blit(self.image, blitxy)

	def events(self):
		pass

class CollidableEntity(Entity):
	def __init__(self, parent, xy, wh, bgColor, bounce=0.0, force=None, add=True):
		Entity.__init__(self, parent, xy, wh, bgColor, add)

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

		for speed in self.movementSteps(self.speedX, self.image.get_width()):
			self.collidingX(speed)
		# Check if on ground
		self.speedX /= 1.15

		# Vertical

		if self.speedY < 1 and self.speedY > -1:
			self.speedY = 1

		for speed in self.movementSteps(self.speedY, self.image.get_height()):
			self.collidingY(speed)


		# Collision check
		self.fixOutOfBounds()

		globs.currentgame.collidableEntities.add(self)

		# Acceleration
		#a = 0.1
		a = globs.clock.get_time()/150.0
		print(a)
		if self.speedY < 0:
			# Jumping
			self.accelerateY(-a)
		elif self.speedY > 0:
			# Falling
			self.accelerateY(a)

		#print("ms since last frame:{} gravityequation: {} speedY: {}".format(globs.ticktime, gravityequation, self.speedY))

	def accelerateY(self, percentage):
		self.speedY *= (1+percentage)

	def movementSteps(self, speed, height):
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
		self.move((self.X + speed, self.Y))

		# Entities
		for entity in self.entitiesColliding():
			self.entityCollisionX(entity)
			self.unstuckEntitiesX()
		
		# Blocks
		collidingBlock = self.blockColliding()
		if collidingBlock:
			self.unstuckBlocksX(collidingBlock)
			self.speedX *=self.bounce

	def collidingY(self, speed):
		self.move((self.X, self.Y + speed))

		# Entities
		if pygame.sprite.spritecollideany(self, globs.currentgame.collidableEntities):
			self.unstuckEntitiesY()
		#for entity in self.entitiesColliding():
		#	self.entityCollisionY(entity)
		#	self.unstuckEntitiesY()

		# Blocks
		collidingBlock = self.blockColliding()
		if collidingBlock:
			self.unstuckBlocksY(collidingBlock)
			# Sets speedY to 0 if bounce is off
			if self.speedY <= -1:
				# Jumping
				self.speedY = 1
			elif self.speedY >= 1:
				# Falling
				self.speedY *= -self.bounce

	def entitiesColliding(self):
		entities = pygame.sprite.spritecollide(self, globs.currentgame.collidableEntities, False)
		return entities

	def blockColliding(self):
		x = self.xy[0]/50
		maxx = (self.xy[0]+self.image.get_width())/50
		possible_x = []
		for iteration in range(x, maxx+1):
			possible_x.append(iteration)
		#print(possible_x)

		y = (self.xy[1])/50
		maxy = (self.xy[1]+self.image.get_height())/50
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

	def unstuckBlocksY(self, collidedItem=None):
		collided = True
		if not collidedItem:
			collidedItem = self.blockColliding()

		if collidedItem:
			while collided:
				print("Unstucking " + str(self) + " from block " + str(collidedItem))
				if self.speedY < 0:
					Y = collidedItem.xy[1]+collidedItem.image.get_height()
				elif self.speedY > 0:
					Y = collidedItem.xy[1]-self.image.get_height()
				self.move((self.X, Y))
				collidedItem = self.blockColliding()

				if not collidedItem:
					collided = False

	def unstuckBlocksX(self, collidedItem=None):
		if not collidedItem:
			x = None
			collidedItem = self.blockColliding()

		if self.speedX > 0:
			x = collidedItem.xy[0]-self.image.get_width()
			self.move((x, self.Y))
		elif self.speedX < 0:
			x = collidedItem.xy[0]+self.image.get_width()
			self.move((x, self.Y))

	def unstuckEntitiesY(self):
		collided = True
		collidedItem = pygame.sprite.spritecollideany(self, globs.currentgame.collidableEntities)
		if collidedItem:
			while collided:
				self.entityCollisionY(collidedItem)
				print("Unstucking " + str(self) + " from entity " + str(collidedItem) + " in Y")
				print("s1: {} s2: {} xy1: {} xy2:{}".format(self.speedY, collidedItem.speedY, self.xy, collidedItem.xy))
				Y = self.Y
				if (self.xy[1]+self.image.get_height())/2 > (collidedItem.xy[1]+collidedItem.image.get_height())/2:
					print("3")
					Y = self.underOf(collidedItem)
				elif (self.xy[1]+self.image.get_height())/2 < (collidedItem.xy[1]+collidedItem.image.get_height())/2:
					print("4")
					Y = self.aboveOf(collidedItem)

				self.move((self.X, Y))
				if self.blockColliding():
					self.unstuckBlocksY()
					collidedItem.unstuckEntitiesY()

				collidedItem = pygame.sprite.spritecollideany(self, globs.currentgame.collidableEntities)

				if not collidedItem:
					collided = False

	def unstuckEntitiesX(self):
		collided = True
		collidedItem = pygame.sprite.spritecollideany(self, globs.currentgame.collidableEntities)
		if collidedItem:
			while collided:
				print("Unstucking " + str(self) + " from entity " + str(collidedItem) + " in X")
				print("s1: {} s2: {} xy1: {} xy2:{}".format(self.speedX, collidedItem.speedX, self.xy, collidedItem.xy))
				X = self.X
				if (self.xy[0]+self.image.get_width())/2 < (collidedItem.xy[0]+collidedItem.image.get_width())/2:
					print("3")
					X = self.leftOf(collidedItem)
				elif (self.xy[0]+self.image.get_width())/2 > (collidedItem.xy[0]+collidedItem.image.get_width())/2:
					print("4")
					X = self.rightOf(collidedItem)

				self.move((X, self.Y))

				if self.blockColliding():
					self.unstuckBlocksX()
					collidedItem.unstuckEntitiesX()

				collidedItem = pygame.sprite.spritecollideany(self, globs.currentgame.collidableEntities)

				if not collidedItem:
					collided = False

	def onGround(self):
		self.move((self.X, self.Y+1))
		if self.blockColliding() or self.entitiesColliding()!=[]:
			onground = True
		else:
			onground = False
		self.move((self.X, self.Y-1))
		return onground

	def aboveOf(self, item):
		return item.xy[1]-self.image.get_height()

	def underOf(self, item):
		return item.xy[1]+item.image.get_height()

	def leftOf(self, item):
		return item.xy[0]-self.image.get_width()

	def rightOf(self, item):
		return item.xy[0]+item.image.get_width()

	def entityCollisionX(self, collidedItem):
		print(self.speedY)


		p1 = self.get_force()[0]
		p2 = collidedItem.get_force()[0]

		f1 = (p2/self.mass)/2
		f2 = (p1/collidedItem.mass)/2

		if abs(p1) < abs(p2):
			self.speedX += f1
			collidedItem.speedX -= f2
		elif abs(p1) > abs(p2):
			collidedItem.speedX += f2
			self.speedX -= f1

	def entityCollisionY(self, collidedItem):
		print(self.speedY)

		p1 = abs(self.get_force()[1])
		p2 = abs(collidedItem.get_force()[1])

		bounce = self.bounce
		if self.onGround:
			bounce = 0
		elif collidedItem.onGround():
			bounce = 1
		else:
			if self.bounce:
				bounce = self.bounce
				if collidedItem.bounce:
					bounce *= (1+collidedItem.bounce)
			elif collidedItem.bounce:
				bounce = collidedItem.bounce

		if p1 < p2:
			self.speedY *= bounce
			collidedItem.speedY *= -bounce
		elif p2 < p1:
			collidedItem.speedY *= bounce
			self.speedY *= -bounce


	def fixOutOfBounds(self):
		# Out of bounds Y

		# Reaches bottom boundary
		if self.Y > globs.currentregion.pixelHeight-self.image.get_height():
			self.move((self.xy[0], globs.currentregion.pixelHeight-self.image.get_height()))
			self.speedX *= -self.bounce
		# Reaches top boundary
		elif self.Y < 0:
			self.move((self.xy[0], 0))
			self.speedY = 1


		# Out of bounds X

		# Reaches left boundary
		if self.X > globs.currentregion.pixelWidth-self.image.get_width():
			self.move((globs.currentregion.pixelWidth-self.image.get_width(), self.xy[1]))
			self.speedX *= -self.bounce
		# Reaches right boundary
		elif self.X < 0:
			self.move((0, self.xy[1]))
			self.speedX *= -self.bounce
