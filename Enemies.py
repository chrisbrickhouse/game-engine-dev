#!/usr/bin/python
#
#   CMCGame
#   Sourcecde Copyright Christian Brickhouse 2012 -2013
#   Art Copyright Christian Brickhouse and Charlie Carver 2012 - 2013
#   Version 0.0_12
#   25 Dec 2013
#
##########################
import pygame
import Sprite
from random import randint
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
	def __init__(self, position, obstacles, spritesheet, stills, world, control=False, health=8, speed=1.5, offset=(20,40)):
		pygame.sprite.Sprite.__init__(self)
		self.count = 1
		self.obstacles = obstacles
		self.old_state = None
		self.warp = None
		self.health = health
		self.world = world
		if spritesheet != None:
			self.spritesheet, self.rectangle = self.load_image(spritesheet)
			self.animate = Sprite.Animate(self.spritesheet, offset)
		self.state = 'up'                               # sets initial state
		self.speed = speed                                   # sets the speed at which the character moves 
		self.displacement = [0,0]
		self.x_pos, self.y_pos = position
		self.control = control
		self.basehealth = health
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
		self.pointwalk = False
		self.limitx = None
		self.limity = None	
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
				self.stop()
		pygame.event.pump()
			
	def moveup(self, mod=1):
		self.displacement[1] -= self.speed*mod                 # displaces rectangle up by speed
		if self.state != 'still':
			self.displacement[0] = 0                   # makes sure character only moves in one axis at a time
		self.old_state = self.state
		self.state = 'up'
	
	def movedown(self, mod=1):
		self.displacement[1] += self.speed*mod                 # displaces rectangle down by speed
		if self.state != 'still':
			self.displacement[0] = 0
		self.old_state = self.state
		self.state = 'down'
	
	def moveleft(self, mod=1):
		self.displacement[0] -= self.speed*mod                 # displaces rectangle left by speed
		if self.state != 'still':
			self.displacement[1] = 0
		self.old_state = self.state
		self.state = 'left'
		
	def moveright(self, mod=1):
		self.displacement[0] += self.speed*mod                 # displaces rectangle right by speed
		if self.state != 'still':
			self.displacement[1] = 0
		self.old_state = self.state
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
			return True
		else:
			return False
			
	def getWorld(self, set=False, world=None):
		if (set == True) and (world != None):
			self.world = world
		else:
			return self.world
			
	def getRect(self):
		return self.rect
		
	def start(self, event, obstacles):
		if obstacles != []:
			#print self.state
			if event == pygame.K_LEFT:
				self.animate.setCycle('left')
				self.moveleft()
				self.animate.update(True)
				self.update(obstacles)
			if event == pygame.K_RIGHT:
				self.animate.setCycle('right')
				self.moveright()
				self.animate.update(True)
				self.update(obstacles)
			if event == pygame.K_UP:
				self.animate.setCycle('up')
				self.moveup()
				self.animate.update(True)
				self.update(obstacles)
			if event == pygame.K_DOWN:
				self.animate.setCycle('down')
				self.movedown()
				self.animate.update(True)
				self.update(obstacles)
		else:
			if event == pygame.K_LEFT:
				self.moveleft()
				self.update(obstacles)
			if event == pygame.K_RIGHT:
				self.moveright()
				self.update(obstacles)
			if event == pygame.K_UP:
				self.moveup()
				self.update(obstacles)
			if event == pygame.K_DOWN:
				self.movedown()
				self.update(obstacles)
				
	def stopSimple(self):
		if (self.state == 'up'):
			self.displacement = [0,0]
			self.old_state = 'up'
			self.state = 'still'
		if (self.state == 'down'):
			self.displacement = [0,0]
			self.old_state = 'down'
			self.state = 'still'
		if (self.state == 'right'):
			self.displacement = [0,0]
			self.old_state = 'right'
			self.state = 'still'
		if (self.state == 'left'):
			self.displacement = [0,0]
			self.old_state = 'left'
			self.state = 'still'
				
	def stop(self,mod=3, state='up'):
		if self.state == 'up':
			self.old_state = 'up'
			self.displacement = [0,0]  # negates any movement already going on
			self.movedown(mod)           # 'bumps' the character off the wall
			newposition = self.rect.move(self.displacement)
			self.rect = newposition
#			self.movedown()
#			newposition = self.rect.move(self.displacement)
#			self.rect = newposition
			self.displacement = [0,0]  # stops the bump
			self.state = 'still'       # makes sure the state is still
		if self.state == 'down':
			self.old_state = 'down'
			self.displacement = [0,0]
			self.moveup(mod)
			newposition = self.rect.move(self.displacement)
			self.rect = newposition
			self.displacement = [0,0]
			self.state = 'still'
		if self.state == 'left':
			self.old_state = 'left'
			self.displacement = [0,0]
			self.moveright(mod)
			newposition = self.rect.move(self.displacement)
			self.rect = newposition
			self.displacement = [0,0]
			self.state = 'still'
		if self.state == 'right':
			self.old_state = 'right'
			self.displacement = [0,0]
			self.moveleft(mod)
			newposition = self.rect.move(self.displacement)
			self.rect = newposition
			self.displacement = [0,0]
			self.state = 'still'
			
	def AI(self, HeroPos, obstacles):
		#print self.old_state
		#print self.state
		#if 1 == 1:
		HeroX, HeroY = HeroPos
		EnemyX, EnemyY = self.getRect().center
		Xdisp = HeroX - EnemyX
		Ydisp = HeroY - EnemyY
		absValueX = abs(Xdisp)
		absValueY = abs(Ydisp)
		#print absValueX,",",absValueY
		#print self.old_state,',',self.state
		if self.pointwalk == True:
			self.walkToPoint(obstacles[self.getRect().collidelist(obstacles)].topleft, obstacles, Ydisp, Xdisp)
			return
		if self.check_collision(self.getRect(), obstacles) == True:
			#print "h"
			self.stop()
			self.walkToPoint(obstacles[self.getRect().collidelist(obstacles)].topleft, obstacles, Ydisp, Xdisp)
		elif self.state != self.old_state and self.old_state != 'still':
			#print absValueX,",",absValueY
			if absValueX < absValueY and (absValueX > 21 or absValueY > 21):
				#print "a"
				if Ydisp < 0:
					self.start(pygame.event.Event(KEYDOWN, key=K_UP).key, obstacles)
					pygame.display.flip()
					#self.stopSimple()
				elif Ydisp > 0:
					self.start(pygame.event.Event(KEYDOWN, key=K_DOWN).key, obstacles)
					pygame.display.flip()
					#self.stopSimple()
			elif absValueX > absValueY and (absValueX > 21 or absValueY > 21):
				#print "a"
				if Xdisp < 0:
					self.start(pygame.event.Event(KEYDOWN, key=K_LEFT).key, obstacles)
					pygame.display.flip()
					#self.stopSimple()
				elif Xdisp > 0:
					self.start(pygame.event.Event(KEYDOWN, key=K_RIGHT).key, obstacles)
					pygame.display.flip()
					#self.stopSimple()
			else:
				#print "a"
				integer = randint(1,2)
				if integer == 1:
					if Xdisp < 0:
						self.start(pygame.event.Event(KEYDOWN, key=K_LEFT).key, obstacles)
						pygame.display.flip()
						#self.stopSimple()
					elif Xdisp > 0:
						self.start(pygame.event.Event(KEYDOWN, key=K_RIGHT).key, obstacles)
						pygame.display.flip()
						#self.stopSimple()
				else:
					if Ydisp < 0:
						self.start(pygame.event.Event(KEYDOWN, key=K_UP).key, obstacles)
						pygame.display.flip()
						#self.stopSimple()
					elif Ydisp > 0:
						self.start(pygame.event.Event(KEYDOWN, key=K_DOWN).key, obstacles)
						pygame.display.flip()
						#self.stopSimple()
			#print self.state
		elif self.state == self.old_state or (self.state != self.old_state and self.old_state == 'still'):
			if self.state == "left" or self.state == "right":
				if absValueY >= absValueX:
						pygame.display.flip()
						self.stopSimple()
			elif self.state == "up" or self.state == "down":
					if absValueX >= absValueY:
						pygame.display.flip()
						self.stopSimple()
	def walkToPoint(self, position, obstacles, Ydisp, Xdisp):
		#print self.limity,"q","limit"
		if (self.old_state == "left" or self.old_state == "right") and (self.limitx == None and self.limity == None):
			self.pointwalk = True
			if Ydisp < 0:
				#move up
				self.limity = self.getRect().centery + Ydisp
				self.start(pygame.event.Event(KEYDOWN, key=K_UP).key, obstacles)
			elif Ydisp > 0:
				#move down
				self.limity = self.getRect().centery + Ydisp
				self.start(pygame.event.Event(KEYDOWN, key=K_DOWN).key, obstacles)
		elif (self.old_state == "up" or self.old_state == "down") and (self.limitx == None and self.limity == None):
			self.pointwalk = True
			if Xdisp < 0:
				#walk left
				self.limitx = self.getRect().centerx + Xdisp
				self.start(pygame.event.Event(KEYDOWN, key=K_LEFT).key, obstacles)
			elif Xdisp > 0:
				#walk right
				self.limitx = self.getRect().centerx + Xdisp
				self.start(pygame.event.Event(KEYDOWN, key=K_RIGHT).key, obstacles)
		#print self.getRect().centery,"q","center"
		if self.limity == self.getRect().centery or self.limitx == self.getRect().centerx:
			self.stopSimple()
			self.pointwalk = False
			self.limity = None
			self.limitx = None
