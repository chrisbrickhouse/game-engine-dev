#!/usr/bin/python
#
#   CMCGame
#   Sourcecde Copyright Christian Brickhouse 2012 -2013
#   Art Copyright Christian Brickhouse and Charlie Carver 2012 - 2013
#   Version 0.0_9.2
#   12 July 2013
#
##########################
import pygame
from pygame.locals import *
from Teleport import Teleport
from Level import Level

class Sprite(pygame.sprite.Sprite):
	def __init__(self, position, obstacles, spritesheet, stills, control=False, speed=2.5, offset=(20,40)):
		pygame.sprite.Sprite.__init__(self)
		self.obstacles = obstacles
		self.old_state = None
		self.warp = None
		if spritesheet != None:
			self.spritesheet, self.rectangle = self.load_image(spritesheet)
			self.animate = Animate(self.spritesheet, offset)
		self.state = 'still'                               # sets initial state
		self.speed = speed                                   # sets the speed at which the character moves 
		self.displacement = [0,0]
		self.x_pos, self.y_pos = position
		self.control = control
		self.UpStill, self.RightStill, self.DownStill, self.LeftStill = stills
		if spritesheet != None:
			self.image = self.animate.getCurrentFrame()
		else:
			self.image = pygame.image.load(self.UpStill)
		self.rect = self.image.get_rect()
		self.rect.center = (self.x_pos, self.y_pos)
		self.screen = pygame.display.get_surface()              # sets screen as the display surface, I think?
		self.area = self.screen.get_rect()                      # makes the self.area variable equal to the area of the screen
		if self.control == False:
			self.obstacles.append(self.rect)
	
	def load_image(self, path):
		"""loads an image and returns it and the rectangle"""
		image = pygame.image.load(path)
		image.convert_alpha()
		return image, image.get_rect
	
	def update(self, obstacles, item=None):
		change = self.animate.update()
		if change:
			self.image = self.animate.getCurrentFrame()
		if self.state == 'still':
			if self.old_state == 'down':
				self.image = pygame.image.load(self.DownStill)
				self.image.convert_alpha()
			elif self.old_state == 'left':
				self.image = pygame.image.load(self.LeftStill)
				self.image.convert_alpha()
			elif self.old_state == 'right':
				self.image = pygame.image.load(self.RightStill)
				self.image.convert_alpha()
			elif self.old_state == 'up':
				self.image = pygame.image.load(self.UpStill)
				self.image.convert_alpha()
			else:
				self.image = pygame.image.load(self.DownStill).convert_alpha()
			
		newposition = self.rect.move(self.displacement)    # takes the displacement and has the sprite displaced by that much
		if self.area.contains(newposition):                # checks to see if sprite is still in the window
			#print self.rect
			collide = self.check_collision(self.rect, obstacles)
			if collide == False:
				self.rect = newposition            # if true, the character is moved to that position
			elif collide == True:
				if self.state == 'up':
					self.old_state = 'up'
					self.displacement = [0,0]  # negates any movement already going on
					self.movedown()            # 'bumps' the character off the wall
					newposition = self.rect.move(self.displacement)
					self.rect = newposition
					self.displacement = [0,0]  # stops the bump
					self.state = 'still'       # makes sure the state is still
				if self.state == 'down':
					self.old_state = 'down'
					self.displacement = [0,0]
					self.moveup()
					newposition = self.rect.move(self.displacement)
					self.rect = newposition
					self.displacement = [0,0]
					self.state = 'still'
				if self.state == 'left':
					self.old_state = 'left'
					self.displacement = [0,0]
					self.moveright()
					newposition = self.rect.move(self.displacement)
					self.rect = newposition
					self.displacement = [0,0]
					self.state = 'still'
				if self.state == 'right':
					self.old_state = 'right'
					self.displacement = [0,0]
					self.moveleft()
					newposition = self.rect.move(self.displacement)
					self.rect = newposition
					self.displacement = [0,0]
					self.state = 'still'
		pygame.event.pump()
			
	def moveup(self):
		self.displacement[1] -= self.speed                 # displaces rectangle up by speed
		if self.state != 'still':
			self.displacement[0] = 0                   # makes sure character only moves in one axis at a time
		self.state = 'up'
	
	def movedown(self):
		self.displacement[1] += self.speed                 # displaces rectangle down by speed
		if self.state != 'still':
			self.displacement[0] = 0
		self.state = 'down'
	
	def moveleft(self):
		self.displacement[0] -= self.speed                 # displaces rectangle left by speed
		if self.state != 'still':
			self.displacement[1] = 0
		self.state = 'left'
		
	def moveright(self):
		self.displacement[0] += self.speed                 # displaces rectangle right by speed
		if self.state != 'still':
			self.displacement[1] = 0
		self.state = 'right'
		
	def check_collision(self, rectangle, obstacle):
		"""This function takes a rectangle passed to it (that is, the character)
		and makes sure that it doesn't colide with any of the rectangles in
		the list. it's really backwards how it works though:
		It will return a -1 if nothing collides, so the first if statement
		checks to see if it *did* collide. If it does, it returns the
		Boolean value True, meaning that it did collide. Otherwise
		it returns saying there is no collision"""
		if rectangle.collidelist(obstacle) != -1:
			#print self.obstacles[rectangle.collidelist(self.obstacles)]
			return True
		else:
			return False
			
	def check_teleport(self, current, teleport):
		if len(teleport) > 0:
			#print "%s, %d" % (self.area.right, self.rect.y)
			if (self.rect.collidelist(teleport)) != -1:
				self.warp = Teleport((self.rect.x, self.rect.y), current, self.area)
				path, newWorld, movement, axis = self.warp.renderWorld()
				print movement
				self.moveSprite(movement, axis)
				self.getWorld(True, newWorld)
				return path
				
	def moveSprite(self, movement, axis='z'):
		if axis == 'x':
			self.rect.x = movement
		elif axis == 'y':
			self.rect.y = movement
		else:
			print "Error in Teleport.py"
		#print self.area.right
			
	def getWorld(self, set=False, world=None):
		if (set == True) and (world != None):
			self.world = world
		else:
			return self.world

class Animate:
	def __init__(self, spritesheetimage, position):
		self.frame = {}
		self.x, self.y = position
		framemaker = self.make_framemap()
		for key in framemaker:
			self.frame[key] = []
			for rect in framemaker[key]:
				self.frame[key].append(spritesheetimage.subsurface(rect))
		self.cycle = self.frame.values()[0]
		self.framenumber = 0
		self.time_last = pygame.time.get_ticks()
		#print self.frame
		
	def make_framemap(self):
		"""Because of how the sprite size is
		hard-coded into the function, all 
		animated sprites must be 40x40"""
		rect_base = pygame.Rect(0,0,self.x,self.y)  # very first rectangle on the image
		framemap = {}            # empty dictionary for the frame map later
		left = [rect_base]       # makes the left list populated with the base rectangle
		
		for each in range(3):
			left.append(left[-1].move(self.x, 0)) #takes the last item in the list, adds 40 to the x and then appends that to the end
		framemap['left'] = left
		rect_base = pygame.Rect(0,self.y*1,self.x,self.y)
		up = [rect_base]
		for each in range(3):
			up.append(up[-1].move(self.x, 0)) #takes the last item in the list, adds 40 to the x and then appends that to the end
		framemap['up'] = up
		rect_base = pygame.Rect(0,self.y*2,self.x,self.y)
		right = [rect_base]
		for each in range(3):
			right.append(right[-1].move(self.x, 0)) #takes the last item in the list, adds 40 to the x and then appends that to the end
		framemap['right'] = right
		rect_base = pygame.Rect(0,self.y*3,self.x,self.y)
		down = [rect_base]
		for each in range(3):
			down.append(down[-1].move(self.x, 0)) #takes the last item in the list, adds 40 to the x and then appends that to the end
		framemap['down'] = down
		#print framemap
		return framemap
		
	def update(self, force = None):
		change = False
		#if force != None: print force
		now = pygame.time.get_ticks()
		delta = now - self.time_last
		if delta > 100:
			if self.framenumber < len(self.cycle) - 1: #checks to see that the frame number is still less than the final frame
				self.framenumber += 1
			else:
				self.framenumber = 0
			self.time_last = now
			change = True
		if force == True:
			self.framenumber = 0
			change = True
		return change
		
	def getCurrentFrame(self):
		return self.cycle[self.framenumber]
		
	def setCycle(self, name_cycle):
		self.cycle = self.frame[name_cycle]
