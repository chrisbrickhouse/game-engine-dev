#!/usr/bin/python
#
#   CMCGame
#   Sourcecde Copyright Christian Brickhouse 2012 -2013
#   Art Copyright Christian Brickhouse and Charlie Carver 2012 - 2013
#   Version 0.0_9.2
#   12 July 2013
#
##########################

import os
import ConfigParser

class Teleport():
	def __init__(self, position, current, area):
		self.x, self.y = position
		#print current
		self.currentWorld = current
		self.line = []
		self.parser = ConfigParser.ConfigParser()      # Loads the parser
		self.parser.read(os.path.join('conf','Universe.map'))               # reads the file
		self.area = area
	
	def renderWorld(self, x=0, y=0, xR=0, yR=0):
		q = (self.area.right - 800)/2
		for option in self.parser.options('universe'):
			self.line.append(self.parser.get('universe', option).split(" "))
		for section in self.parser.sections():
			if section != 'universe':
				if self.parser.get(section, 'name') == self.currentWorld:
					self.currentWorld = section
		for n in range(len(self.line)):
			for i in range(len(self.line[n])):
				if self.currentWorld == self.line[n][i]:
					if self.x < (40 + q):
						#print 'check'
						newWorld = self.line[n][i-1]
						movement = (self.area.right - (80 + q))
						axis = 'x'
					elif self.area.right - (q+self.x+40) < 40:
						newWorld = self.line[n][i+1]
						movement = (self.area.x + q + 80)
						axis = 'x'
					elif self.y < 40:
						newWorld = self.line[n-1][i]
						movement = (self.area.bottom - 80)
						axis = 'y'
					elif self.area.bottom - (self.y+40) < 40:
						newWorld = self.line[n+1][i]
						movement = (self.area.y + 80)
						axis = 'y'
		path = self.parser.get(newWorld, 'map')
		#print "Teleport" + newWorld
		return (path, newWorld, movement, axis)
		
	def getWorld(self):
		return self.currentWorld
