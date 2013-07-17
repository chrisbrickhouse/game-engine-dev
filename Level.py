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
import ConfigParser
from pygame.locals import *

class Level():
	"""This class takes care of loading the levels and parsing
	the information from the config file.
	__init__ takes an argument, path, which is the relative path
	to the level config file"""
	def __init__(self, path, windowRect):
		self.parser = ConfigParser.ConfigParser()      # Loads the parser
		self.Rect = windowRect
		self.path = path
		self.parser.read(path)                         # reads the file
		self.tiles = {}                                # initiates a dictionary for the tile definitions
		self.line = []                                 # initiates a list for the lines
		self.teleport = []
		self.coord = [0,0]                             # initiates the starting coordinates of the screen
		self.obstacles = []                            # initiates a list for solid blocks
		self.rectangles = []                           # initiates a list of rectangles for the solid blocks
		for section in self.parser.sections():         # iterates over each section (the parts in brackets)
			if (section != 'map') and (section != 'universe'):                 # makes it so that it only does the definition sections, ie, not map
				self.tiles[section] = self.parser.get(section, 'tile') # sets the tile's path as the value of the tile dictionary
		
	def read_map(self, response=False):
		"""This function takes the map and for each line of the map
		it splits the values at the space and adds them to the list"""
		for option in self.parser.options('map'):
			self.line.append(self.parser.get('map', option).split(" "))
		if response == True:
			return self.line
	
	def render(self):
		self.teleport = []
		self.obstacles = []
		self.coord[0] = (self.Rect.right - 800)/2
		self.coord.append((self.Rect.right - 800)/2)
		#self.coord[1] = (Self.Rect.bottom - 800)/2 
		#print self.teleport
		#print 'render'
		#print self.path
		surface = pygame.Surface((self.Rect.bottomright))  # when implemented, will create a surface the same size as the window
		#surface = pygame.Surface((800,800))
		for n in range(len(self.line)):                  # number of lines
			for i in range(len(self.line[n])):          # number of items in a line
				x,y,xR = self.coord     # sets the x and y variables to the coordinates currently being editted
				"""This series of if statements checks what tile the map symbol is pointing to and
				then blits the tile onto the surface before incrementing self.coord's x value
				Most are pretty similar, but specific documentation for 3 through 8 and # is needed"""
				if (self.line[n][i] == '0'):
					tile = pygame.image.load(self.tiles['0']) 
					surface.blit(tile, (x,y))
					self.coord[0] += 40
				elif self.line[n][i] == '1':
					tile = pygame.image.load(self.tiles['1'])
					surface.blit(tile, (x,y))
					self.coord[0] += 40
				elif self.line[n][i] == '2':
					tile = pygame.image.load(self.tiles['2'])
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40))
					self.coord[0] += 40
				elif self.line[n][i] == '3':
					number = self.line[n-1][i]
					tile = pygame.image.load(self.tiles[number]) #this takes the tile directly above it and blits it down as a background for the actual tile because this one is transparent in parts
					surface.blit(tile, (x,y))
					tile = pygame.image.load(self.tiles['3']).convert_alpha() #this makes the alpha section transparent
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40)) #because it's solid, this adds it to the list of obstacles
					self.coord[0] += 40
				elif self.line[n][i] == '4':
					tile = pygame.image.load(self.tiles['4'])
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40))
					self.coord[0] += 40
				elif self.line[n][i] == '5':
					number = self.line[n-1][i]
					tile = pygame.image.load(self.tiles[number])
					surface.blit(tile, (x,y))
					tile = pygame.image.load(self.tiles['5']).convert_alpha()
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40))
					self.coord[0] += 40
				elif self.line[n][i] == '6':
					tile = pygame.image.load(self.tiles['2'])
					surface.blit(tile, (x,y))
					tile = pygame.image.load(self.tiles['6']).convert_alpha()
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40))
					self.coord[0] += 40
				elif self.line[n][i] == '7':
					tile = pygame.image.load(self.tiles['2'])
					surface.blit(tile, (x,y))
					tile = pygame.image.load(self.tiles['7']).convert_alpha()
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40))
					self.coord[0] += 40
				elif self.line[n][i] == '8':
					tile = pygame.image.load(self.tiles['2'])
					surface.blit(tile, (x,y))
					tile = pygame.image.load(self.tiles['8']).convert_alpha()
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40))
					self.coord[0] += 40
				elif (self.line[n][i] == '#'):
					"""This is a special case for tiles that cause teleportation"""
					tile = pygame.image.load(self.tiles['0'])
					surface.blit(tile, (x,y))
					self.teleport.append(pygame.Rect(x,y,40,40))
					#print self.teleport
					self.coord[0] += 40
				elif self.line[n][i] == '^':
					tile = pygame.image.load(self.tiles['1'])
					surface.blit(tile, (x,y))
					tile = pygame.image.load(self.tiles['^'])
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40))
					self.coord[0] += 40
				elif self.line[n][i] == '|':
					tile = pygame.image.load(self.tiles['1'])
					surface.blit(tile, (x,y))
					tile = pygame.image.load(self.tiles['|'])
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40))
					self.coord[0] += 40
				elif self.line[n][i] == '<':
					tile = pygame.image.load(self.tiles['1'])
					surface.blit(tile, (x,y))
					tile = pygame.image.load(self.tiles['<'])
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40))
					self.coord[0] += 40
				elif self.line[n][i] == '>':
					tile = pygame.image.load(self.tiles['1'])
					surface.blit(tile, (x,y))
					tile = pygame.image.load(self.tiles['>'])
					surface.blit(tile, (x,y))
					self.obstacles.append(pygame.Rect(x,y,40,40))
					self.coord[0] += 40
				elif (self.line[n][i] == '@'):
					tile = pygame.image.load(self.tiles['0'])
					surface.blit(tile, (x,y))
					setCharacter((x,y))
					#print self.teleport
					self.coord[0] += 40
			if self.coord[0] == 800 + self.coord[2]: #makes sure each item in the row has been printed, if so, it moves to the next line
				self.coord[0] = xR
				self.coord[1] += 40
			else:
				print 'ERROR: Row %s' % (n+1)
				print 'rendering didn\'t iterate through whole line of tiles'
				print 'expect graphics errors'
				self.coord[0] = xR
				self.coord[1] += 40
		#n = 0
		#print self.obstacles
		#print self.rectangles
		#print self.teleport
		setTiles(self.obstacles, self.teleport)
		return surface
		
def setCharacter(position):
		global post
		post = position
			
def getCharacter():
		return post
		
def setTiles(obstacle, teleport):
	global obstacles 
	obstacles = obstacle
	global warplist
	warplist = teleport
	#print "set %s" % (teleport)
def getTiles():
	#print "get %s" % (warplist)
	return obstacles, warplist
