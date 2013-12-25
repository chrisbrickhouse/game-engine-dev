#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   CMCGame
#   Sourcecode Copyright Christian Brickhouse 2012 -2013
#   Art Copyright Christian Brickhouse and Charlie Carver 2012 - 2013
#   Version 0.0_12
#   25 Dec 2013
#
##########################
import pygame
import Movement
import ConfigParser
import os
import sys
import shutil
import time
import Enemies
import Save
import datetime
import inspect
import xml.etree.ElementTree as ET
from pygame.locals import *
from Level import *
from KeyReader import *
import Sprite
from KeyReader import *



def main(currentWorld, path, windowRect, level, background, obstacles, teleports, position, Hero, char, attack, defense, Enemy, heroSprite, enemySprites):
	leftcount = 0
	while True:
		fpsClock.tick(45)                                  # max of 45fps
		for event in pygame.event.get():
			#print event
			if event.type == QUIT: #check for quit signal and properly terminate. 
				shutdown()
				return
			if event.type == KEYDOWN: # checks for actions
				#print event.key
				if event.key == K_ESCAPE: #escape key exits
					shutdown()
					return
				elif event.key == K_l:
					Save.saveGame(currentWorld, Hero.getRect().topleft, Hero.health, Enemy.getRect().topleft, Enemy.health, Enemy.world, Enemy.old_state, Enemy.state)
				elif (event.key == K_LEFT) or (event.key == K_RIGHT) or (event.key == K_DOWN) or (event.key == K_UP):
					# Checks for arrow keys and moves the character in that direction
					Hero.start(event.key, obstacles)
					#Enemy.start(event.key, obstacles)
				else:
					k, q = 1,1 #counters
					while k == 1:
						if q == 1: #this is a way to prevent a bug where everything was being done twice causing a crash
							reader = KeyReader(event.key, window, fpsClock.tick(45))
							k, backg, track = reader.testKey(background) # from KeyReader.py
							inventory = InventoryMap(window) #initializes the inventory system
							if track == 'inventory':
								item = inventory.moveCursor(False,track)
								if item != False and item != None:
									Hero.changeSheet(os.path.join('SpriteDev','Sheets',item.rstrip())) #updates the sprite sheet to be of the character holding the weapon
									pygame.display.flip() #updates the screen
									heroSprite = pygame.sprite.RenderPlain(Hero) #renders the sprite
								break
							elif track == 'weapons':
								item = inventory.moveCursor(True,track)
								if item != False and item != None:
									Hero.changeSheet(os.path.join('SpriteDev','Sheets',item.rstrip())) #updates the sprite sheet to be of the character holding the weapon
									pygame.display.flip() #updates the screen
									heroSprite = pygame.sprite.RenderPlain(Hero) #renders the sprite
									#if item.rstrip() == "Sword.png":
									attack, defense = weaponData(item)
								break
							elif track == 'swing':
								kill = swing(Hero, attack, defense, Enemy)
								if kill == True:
									Enemy.kill(True)
									enemycollide = False
								break
							if backg != 1 and track == 'talk': #just a testing thing
								dialogueLoop(k, path) # see documentation there
								level = Level(path, windowRect) #re parses teh backround
								level.read_map() 
								background = level.render() #resets the background
								#if Hero.old_state == None:
								#	print "down"
								#	print attack 
								#elif Hero.state == 'still': #and Hero.state != None:
								#	print Hero.old_state+" old"
								#	print attack
								#else:
								#	print Hero.state+" current"
								#	print attack
							#print isinstance(k, int)
							if k == 42: #42 is the official quit signal for k
								q = 0
							elif isinstance(k, int) != True: # checks to see if k value is a code or string
								#print "break"
								break
							elif event.key == K_ESCAPE:
								shutdown() #makes sure that pressing escape quits the program
								return
							else:
								q +=1 #iterates the main loop if nothing happens
						if backg != 1:
							change_Background(backg, (0,0), True)
						if track == 'quit':
							break
						pygame.display.flip()
			elif event.type == KEYUP: #stops movement when arrow key is released
				#print Hero.state,"hero"
				Hero.stopSimple()
				#Enemy.stopSimple()
				#print Hero.state,"hero"
		herocollide = True
		if Enemy.alive() == True:
			herocollide = Enemy.check_collision(Enemy.getRect(),[Hero.getRect()])
			enemyCollide = Hero.check_collision(Hero.getRect(),[Enemy.getRect()])
		else:
			enemyCollide = False
		if herocollide != True:
			Enemy.AI(Hero.getRect().center, obstacles)
			#Enemy2.AI(Hero.getRect().center, obstacles)
		elif Enemy.alive():
			Enemy.stop(20)
			damage = .25-float(defense)
			if damage < 0:
				damage = 0 
			Hero.health -= damage
			#print "hero: %s" % Hero.health
			#print Hero.rect.size
		if leftcount == 140:
			leftcount = 0
		#if leftcount%10 == 0:
			#print Enemy.rect.center
		char.update(obstacles) #checks for collisions between sprites
		if enemyCollide != False and Enemy.alive() == True:
			#print "Here"
			Hero.stop(5)
		path_2 = Hero.check_teleport(currentWorld, teleports) #checks to see if the character has moved to a different world
		if (path_2 != path) and (path_2 != None): #if path_2 is different than the already existent one, and exists
			path = path_2 #sets path to path_2
			#print "main path:", path
			level = Level(os.path.join('conf',path), windowRect)
			level.read_map()                #redoes the level render
			currentWorld = Hero.getWorld()  #sets the current word to wherever the hero is so that background can be properly rendered
			#print currentWorld
			background = level.render() #makes the background
			char = pygame.sprite.RenderPlain(Hero) 
		teleports = [] # clears the sets
		obstacles = []
		obstacles, teleports = getTiles() # resets the tiles
		if Hero.health <= 0:
			shutdown()
		#Test = Hero.check_collision(Hero.getRect(),[Enemy.getRect()])
		#print Test
		change_Background(background, (0,0), True, char)
		updateHearts(Hero.health)
#		window.blit(background, (0,0))
#		char.draw(window)
#		pygame.display.flip()
		save = [currentWorld, Hero.getRect().topleft, Hero.health, Enemy.getRect().topleft, Enemy.health]
		#print datetime.datetime.now().strftime('%H.%M.%S.%Y-%m-%d')

def weaponData(weapon):
	#print "here"
	name = weapon.split('.')
	name = name[0]
	tree = ET.parse(os.path.join('ItemData','weapons.xml'))
	#print "done"
	root = tree.getroot()
	element = root.find(name)
	#element = root.Element(name)
	#print element
	tag = element.find('attack')
	attack = tag.text
	tag = element.find('defense')
	defense = tag.text
	print attack+","+defense
	return (attack,defense)
	

def dialogueLoop(textList, path):
	q = 1 # this might actually be useless
	font = pygame.font.SysFont('Courier New', 30) #initializes pygame.font
	#font = pygame.font.Font(None, 30)
	dialogueBox = pygame.image.load(os.path.join('conf','TextBox.png')) #loads the image that holds the text
	#print "hero: ",Hero.rect.bottom
	#print "path: ",path
	windowRect = window.get_rect()
	x = (windowRect.right - 800)/2
	yTest = windowRect.bottom - 300
	if Hero.rect.bottom >= yTest - 10: # if the sprite is too close to where the text box would noramlly be, the box is moved to the top
		y = windowRect.top
		#print "True"
	else:
		y = yTest
	level = Level(path, windowRect)
	level.read_map() #redoes the level
	Textbackground = level.render()
	#Textbackground = pygame.Surface(windowRect.bottomright)
	b = 0
	textList_broken = [] #empty set to use for the broken up text
	if len(textList) > 3:
		while len(textList) != 0: #while there are still things in textList
			a = 0
			tripletset = [] #empty set to hold sets of triple lines
			while a < 3 and len(textList) != 0:
				#print "a: ",a
				#print textList
				tripletset.append(textList[0]) #adds first line from textList to tripleset
				textList.pop(0) #removes the line that was just added
				#print "length :",len(textList)
				a += 1
			if len(textList) !=0:
				tripletset.append(u'\u25bc') #if it's not the last line, adds a ▼ to the set to show text continues
			textList_broken.append(tripletset) #adds tripleset to textList_broken
#			a = 0
			#print "broken: ",textList_broken
	#print "lenght", len(textList)
	textList = textList_broken
	#print "list: ",textList
#	while q <= 200:
		#rectCoord = Hero.get_rect()
		#print y
		#Textbackground.blit(background, (0,0))
	for m in range(len(textList)):
		"""This loop here is what puts the text onto the screen. The data structure is set up so that the first
		is a list of 3 line text blocks (pages) then it is a list of those lines. 
		"""
		Textbackground.blit(dialogueBox, (x,y)) #blits the dialogue image onto the level background
		q = 0
		while q == 0:
			for event in pygame.event.get():
				for n in range(len(textList[m])):
					words = font.render(textList[m][n], 1, (0, 0, 0))
					Textbackground.blit(words, (x+20, y+20+n*30))
				char.update(obstacles)
				change_Background(Textbackground, (0,0), True, char)
				pygame.display.flip()
				if event.key == K_RETURN and event.type == KEYDOWN:
					#print "STUFF"
					q = 1
#		q += 1
#		if q%100 == 0:
			#print "y:    ", yTest
#			print q				
	
def shutdown():
	try:
		os.rename('Inventory.map.bak', 'Inventory.map')
		os.remove('coord.temp')
		print "Shutting down NOW"
		sys.exit()
	except:
		print "nothing to delete"
		print "Shutting down NOW"
		sys.exit()
	

def change_Background(background, coords=(0,0), flip=True, sprite=False):
	window.blit(background, coords)
	if sprite != False:
		sprite.draw(window)
	#if flip != False:
	#	pygame.display.flip()
		
#def renderSprites(sprites):
#	spriteRendered = pygame.sprite.RenderPlain(sprites)
#	return spriteRendered

def swing(sprite, attack, defense, enemies):
	kill = False
	if sprite.state == 'down' or sprite.old_state == 'down':
		rect = sprite.rect.copy()
		rect.bottom = rect.bottom +15
		Collide = sprite.check_collision(rect,[enemies.getRect()])
		if Collide == True:
			enemies.health -= int(attack)
			print enemies.health
		if enemies.health <= 0:
			kill = True
			enemies.rect.size = (0,0)
			sprite.update([enemies.getRect()])
	elif sprite.state == 'left' or sprite.old_state == 'left':
		rect = sprite.rect.copy()
		rect.left = rect.left +15
		Collide = sprite.check_collision(rect,[enemies.getRect()])
		if Collide == True:
			enemies.health -= int(attack)
			print enemies.health
		if enemies.health <= 0:
			kill = True
			enemies.rect.size = (0,0)
			sprite.update([enemies.getRect()])
	elif sprite.state == 'right' or sprite.old_state == 'right':
		rect = sprite.rect.copy()
		rect.right = rect.right +15
		Collide = sprite.check_collision(rect,[enemies.getRect()])
		if Collide == True:
			enemies.health -= int(attack)
			print enemies.health
		if enemies.health <= 0:
			kill = True
			enemies.rect.size = (0,0)
			sprite.update([enemies.getRect()])
	elif sprite.state == 'up' or sprite.old_state == 'up':
		rect = sprite.rect.copy()
		rect.top = rect.top +15
		Collide = sprite.check_collision(rect,[enemies.getRect()])
		if Collide == True:
			enemies.health -= int(attack)
			print enemies.health
		if enemies.health <= 0:
			kill = True
			enemies.rect.size = (0,0)
			sprite.update([enemies.getRect()])
	return kill	
	
def updateHearts(health):
	surf = pygame.Surface((200,40))
	health = int(health)
	windowrect = window.get_rect()
	q = (windowrect.width-200)/2
	left=0
	bottom=0
	full = pygame.image.load(os.path.join('conf','fullheart.png')).convert_alpha()
	empty = pygame.image.load(os.path.join('conf','emptyheart.png')).convert_alpha()
	half = pygame.image.load(os.path.join('conf','halfheart.png')).convert_alpha()
	if health == 10:
		surf.blit(full,(0,0))
		left+=40
		surf.blit(full,(40,0))
		left+=40
		surf.blit(full,(80,0))
		left+=40
		surf.blit(full,(120,0))
		left+=40
		surf.blit(full,(160,0))
	elif health >= 8:
		surf.blit(full,(0,0))
		left+=40
		surf.blit(full,(40,0))
		left+=40
		surf.blit(full,(80,0))
		left+=40
		surf.blit(full,(120,0))
		left+=40
		surf.blit(empty,(160,0))
	elif health >= 6:
		surf.blit(full,(0,0))
		left+=40
		surf.blit(full,(40,0))
		left+=40
		surf.blit(full,(80,0))
		left+=40
		surf.blit(empty,(120,0))
		surf.blit(empty,(160,0))
	elif health >= 4:
		surf.blit(full,(0,0))
		left+=40
		surf.blit(full,(40,0))
		left+=40
		surf.blit(empty,(80,0))
		surf.blit(empty,(120,0))
		surf.blit(empty,(160,0))
	elif health >= 2:
		surf.blit(full,(0,0))
		left+=40
		surf.blit(empty,(40,0))
		surf.blit(empty,(80,0))
		surf.blit(empty,(120,0))
		surf.blit(empty,(160,0))
	if health%2 == 1:
		surf.blit(half,(left,0))
	surf.set_colorkey((0,0,0))
	window.blit(surf,(q,windowRect.top))
	pygame.display.flip()

##################################
class InventoryMap():
	def __init__(self,window):
		self.parser = ConfigParser.ConfigParser()
		self.parser.read(os.path.join('conf','Inventory.map'))
		self.line = []
		self.coord = []
		self.coord1 = []
		self.window = window
		
	def openInventory(self, check):
		asdf = 1
		self.parser.read(os.path.join('conf','Inventory.map'))
		#print check
		self.windowRect = self.window.get_rect()
		surface = pygame.Surface((self.windowRect.bottomright))
		q = (self.windowRect.right - 800)/2
		#print q
		self.coord.append(q)
		self.coord.append(self.windowRect.top)
		self.coord.append(q)
#		print "first",self.windowRect.right
		for option in self.parser.options('map'):
			self.line.append(self.parser.get('map', option).split(" "))
		"""for section in self.parser.sections():
			if section != 'map':
				if self.parser.get(section, 'name') == self.currentWorld:
					self.currentWorld = section"""
		for n in range(len(self.line)):
			for i in range(len(self.line[n])):
				#print "%s coords: %s %s" % (asdf, self.coord[0], self.coord[1])
				asdf +=1
				if self.line[n][i] == '0':
					tile = pygame.image.load(os.path.join('ItemData','Blank.png')) 
					surface.blit(tile, (self.coord[0],self.coord[1]))
					self.coord[0] += 80
				elif self.line[n][i] == '1':
					tile = pygame.image.load(os.path.join('ItemData','InventoryTile.png')) 
					surface.blit(tile, (self.coord[0],self.coord[1]))
					self.coord[0] += 80
				elif self.line[n][i] == '2':
					tile = pygame.image.load(os.path.join('ItemData','InventoryTileSelected.png')) 
					surface.blit(tile, (self.coord[0],self.coord[1]))
					#f = open("coord.temp", "wb")
					#f.write('%r %r' % (i, n))
					#print "x: ",i,"\ny: ",n
					#f.close()
					self.coord[0] += 80
			if self.coord[0] == 800 + q:
				self.coord[0] = q
				self.coord[1] += 80
		if check == False:
			overlay = self.LoadItems(surface)
		else:
			overlay = self.LoadWeapons(surface)
		surface.blit(overlay, (0,0))
		return surface
		
	def LoadItems(self, surface):
		self.images = FileRead(os.path.join('conf','inventory.save'))
		self.windowRect = self.window.get_rect()
		q = (self.windowRect.right - 800)/2
		self.coord1.append(q + 20 + 80*2)
		self.coord1.append(self.windowRect.top + 20 + 80*2)
		self.coord1.append(q + 20 + 80*2)
		#print self.windowRect.right
		#print (800 + q)
		for n in range(len(self.images)):
			path = os.path.join('ItemData', self.images[n])
			tile = pygame.image.load(path)
			tile.convert_alpha()
			surface.blit(tile, (self.coord1[0],self.coord1[1]))
			#print "number: ",n,", coord: ",self.coord1[0]
			self.coord1[0] += 80
			if self.coord1[0] >= 943:
				self.coord1[0] = self.coord1[2]
				self.coord1[1] += 80	
		return surface
		
	def LoadWeapons(self, surface):
		self.images = FileRead(os.path.join('conf','weapons.save'))
		self.windowRect = self.window.get_rect()
		q = (self.windowRect.right - 800)/2
		self.coord1.append(q + 20 + 80*2)
		self.coord1.append(self.windowRect.top + 20 + 80*2)
		self.coord1.append(q + 20 + 80*2)
		#print self.windowRect.right
		#print (800 + q)
		for n in range(len(self.images)):
			path = os.path.join('ItemData', self.images[n])
			tile = pygame.image.load(path)
			tile.convert_alpha()
			surface.blit(tile, (self.coord1[0],self.coord1[1]))
			#print "number: ",n,", coord: ",self.coord1[0]
			self.coord1[0] += 80
			if self.coord1[0] >= 943:
				self.coord1[0] = self.coord1[2]
				self.coord1[1] += 80	
		return surface
		
	def selectItem(self, item, track):
		pos = item-1
		#print track+'.save'
		with open(os.path.join('conf',track+'.save'), 'r') as f:
			itemList = f.readlines()
		try:
			#print itemList[pos]
			return itemList[pos]
		except:
			return False
	
	def moveCursor(self, check, track):
		backg = self.openInventory(check)
		selected = pygame.image.load(os.path.join('ItemData','InventoryTileSelected.png'))
		notselected = pygame.image.load(os.path.join('ItemData','InventoryTile.png'))
		selected.convert_alpha()
		notselected.convert_alpha()
		quitArg = 0
		position = 1
		coordinates = [(windowRect.right - 800)/2 + 160,windowRect.top+160]
		backg.blit(selected, (coordinates[0],coordinates[1]))
		while quitArg == 0:
			change_Background(backg, (0,0))
			pygame.display.flip()
			#print "you fuck"
			for event in pygame.event.get():
				#print event.key
				if event.type == KEYDOWN:
					backg.blit(notselected, (coordinates[0],coordinates[1]))
					if event.key == K_q:
						quitArg = 1
					elif event.key == K_ESCAPE:
						shutdown()
					if (event.key == K_LEFT) and (position-1)%6 != 0:
						position -= 1
						coordinates[0] -= 80
						#print "left %s" % position
					elif (event.key == K_RIGHT) and (position%6 != 0):
						position += 1
						coordinates[0] += 80
						#print "right %s" % position
					elif (event.key == K_DOWN) and position < 25: 
						position += 6
						coordinates[1] += 80
						#print "down %s" % position
					elif (event.key == K_UP) and position > 6:
						position -= 6
						coordinates[1] -= 80
						#print "up %s" % position
					backg.blit(selected, (coordinates[0],coordinates[1]))
					if event.key == K_RETURN:
						item = self.selectItem(position, track)
						return item
					#pygame.display.flip()
			if quitArg == 1:
				break
###########################################################
pygame.init()
pygame.font.init()
fullscreen = pygame.display.list_modes()
#print fullscreen
fpsClock = pygame.time.Clock()
window = pygame.display.set_mode(fullscreen[0])
#window = pygame.display.set_mode((1200,800))
pygame.display.set_caption('Lorem Ipsum: The Game')
global currentWorld, path, windowRect, level, background, obstacles, teleports, position, Hero, char
h = 1
while h == 1:
	TitleFont1 = pygame.font.SysFont("monospace", 90)
	TitleFont2 = pygame.font.SysFont("monospace", 70)
	ButtonFont = pygame.font.SysFont("monospace", 20, bold=True)
	TitleRender1 =  TitleFont1.render("Lorem Ipsum:", 1, (255,255,255), (0,0,0))
	TitleRender2 =  TitleFont2.render("The Game", 1, (255,255,255), (0,0,0))
	Start = ButtonFont.render("New Game", 1, (0,0,0), (255,255,255))
	Load = ButtonFont.render("Load Game", 1, (0,0,0), (255,255,255))
	Options = ButtonFont.render("Options", 1, (0,0,0), (255,255,255))
	Button = pygame.image.load(os.path.join('conf','ButtonBackgroundUp.png'))
	window.fill((0,0,0))
	x,y = window.get_rect().centerx, window.get_rect().height
	xh = window.get_rect().width
	z,a = TitleRender1.get_rect().width, TitleRender1.get_rect().height
	b,c = TitleRender2.get_rect().width, TitleRender2.get_rect().height
	d,e = Start.get_rect().width, Start.get_rect().height
	f,g = Load.get_rect().width, Load.get_rect().height
	i,j = Options.get_rect().width, Options.get_rect().height
	xh = xh / 3
	y=y/3
	z=z/2
	a=a/2 
	b=b/2
	d /= 2
	e /= 2
	f /= 2
	g /= 2
	i /= 2
	j /= 2
	window.blit(TitleRender1, (x - z, y - a))
	window.blit(TitleRender2, (x - b, y + a))
	window.blit(Button, (x-65, 2*y))
	window.blit(Button, (xh-65, 2*y))
	window.blit(Button, (xh*2-65, 2*y))
	####################################
	window.blit(Start, (xh-d, 2*y+18-e))
	window.blit(Load, (x-f, 2*y+18-g))
	window.blit(Options, (xh*2-i, 2*y+18-j))
	####################################
	ButtonRect1 = Rect((xh-d, 2*y+18-e),(130,35))
	ButtonRect2 = Rect((x-f, 2*y+18-g),(130,35))
	ButtonRect3 = Rect((xh*2-i, 2*y+18-j),(130,35))
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): #check for quit signal and properly terminate. 
			shutdown()
			exit()
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				if ButtonRect1.collidepoint(event.pos) == True:
					attack = 1
					defense = 0
					currentWorld = 'Home'
					path = os.path.join('conf','levelmap')
					itemPath = 'ItemData'
					windowRect = window.get_rect()
					level = Level(path, windowRect)
					level.read_map()
					background = level.render()
					window.blit(background, (0,0))
					obstacles, teleports = getTiles()
					pygame.display.flip()
					position = getCharacter()
					Hero = Sprite.Sprite(position, obstacles, os.path.join('SpriteDev','Sheets','spritesheet1.png'),(os.path.join('SpriteDev','UpStill.png'),os.path.join('SpriteDev','RightStill.png'),os.path.join('SpriteDev','DownStill.png'),os.path.join('SpriteDev','LeftStill.png')), True)
					Enemy = Enemies.Enemy((400,500), obstacles, os.path.join('SpriteDev','Sheets','enemysheet.png'),(os.path.join('SpriteDev','EnemyUpStill.png'),os.path.join('SpriteDev','EnemyRightStill.png'),os.path.join('SpriteDev','EnemyDownStill.png'),os.path.join('SpriteDev','EnemyLeftStill.png')), currentWorld, True)
					char = pygame.sprite.RenderPlain(Hero, Enemy)
					heroSprite = pygame.sprite.RenderPlain(Hero)
					enemySprites = pygame.sprite.RenderPlain(Enemy)
					h = 0
					main(currentWorld, path, windowRect, level, background, obstacles, teleports, position, Hero, char, attack, defense, Enemy, heroSprite, enemySprites)
				if ButtonRect2.collidepoint(event.pos) == True:
					save = []
					save = Save.loadGame(window)
					currentWorld, heroPos, heroHealth, enemyPos, enemyHealth, enemyWorld, oldstate, newstate = save
					attack = 1
					defense = 0
					if currentWorld!='Home' and currentWorld!='H':
						currentWorldPath="World"+str(currentWorld)+".map"
					else:
						currentWorldPath='levelmap'
					path = os.path.join('conf',currentWorldPath)
					itemPath = 'ItemData'
					windowRect = window.get_rect()
					level = Level(path, windowRect)
					level.read_map()
					background = level.render()
					window.blit(background, (0,0))
					heroPos = heroPos.strip(")")
					heroPos = heroPos.strip("(")
					heroPos = heroPos.split(",")
					heroPos = (int(heroPos[0]),int(heroPos[1]))
					enemyPos = enemyPos.strip(")")
					enemyPos = enemyPos.strip("(")
					enemyPos = enemyPos.split(",")
					enemyPos = (int(enemyPos[0]),int(enemyPos[1]))
					#print type(heroPos)
					obstacles, teleports = getTiles()
					pygame.display.flip()
					Hero = Sprite.Sprite(heroPos, obstacles, os.path.join('SpriteDev','Sheets','spritesheet1.png'),(os.path.join('SpriteDev','UpStill.png'),os.path.join('SpriteDev','RightStill.png'),os.path.join('SpriteDev','DownStill.png'),os.path.join('SpriteDev','LeftStill.png')), True)
					if enemyWorld == currentWorld:
						Enemy = Enemies.Enemy(enemyPos, obstacles, os.path.join('SpriteDev','Sheets','enemysheet.png'),(os.path.join('SpriteDev','EnemyUpStill.png'),os.path.join('SpriteDev','EnemyRightStill.png'),os.path.join('SpriteDev','EnemyDownStill.png'),os.path.join('SpriteDev','EnemyLeftStill.png')), enemyWorld, True)
						char = pygame.sprite.RenderPlain(Hero, Enemy)
						heroSprite = pygame.sprite.RenderPlain(Hero)
						enemySprites = pygame.sprite.RenderPlain(Enemy)
					else:
						Enemy = Enemies.Enemy(enemyPos, obstacles, os.path.join('SpriteDev','Sheets','enemysheet.png'),(os.path.join('SpriteDev','EnemyUpStill.png'),os.path.join('SpriteDev','EnemyRightStill.png'),os.path.join('SpriteDev','EnemyDownStill.png'),os.path.join('SpriteDev','EnemyLeftStill.png')), enemyWorld, True)
						char = pygame.sprite.RenderPlain(Hero, Enemy)
						heroSprite = pygame.sprite.RenderPlain(Hero)
						enemySprites = pygame.sprite.RenderPlain(Enemy)
						Enemy.kill()
					h = 0
					Enemy.AI(Hero.getRect().center, obstacles)
					Enemy.old_state = Enemy.state
					main(currentWorld, path, windowRect, level, background, obstacles, teleports, heroPos, Hero, char, attack, defense, Enemy, heroSprite, enemySprites)
					#exit()
				if ButtonRect3.collidepoint(event.pos) == True:
					print 'Options isn\'t implemented yet...'
					exit()
