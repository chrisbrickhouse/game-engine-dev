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
import re
import os
import Dialogue
from Dialogue import *
from pygame.locals import *

class KeyReader():
	def __init__(self, key, window, clock):
		self.parser = ConfigParser.ConfigParser()
		self.key = key
		self.window = window
		self.tick = clock
		#self.inventory = InventoryMap(self.window)
		
	def testKey(self, OGbackground, track=1, Rbackground=None):
		self.trackback = track
		if self.key == K_e:
			self.trackback = 'inventory'
			if track != 1:
				return (42, OGbackground, self.trackback)
			return (1, OGbackground, self.trackback)
		elif self.key == K_w:
			self.trackback = 'weapons'
			if track != 1:
				return (42, OGbackground, self.trackback)
			return (1, OGbackground, self.trackback)
		elif self.key == K_SPACE:
			self.trackback = 'swing'
			#self.swing()
			#textList = []
			logue = Dialogue('5', self.window, OGbackground)
			text = logue.readTable()
			textList = logue.breakText(text)
			#print textList
			#logue.printToScreen(text)
			self.tick
			return (textList, OGbackground, self.trackback)
		elif self.key == K_q:
			self.trackback = 'quit'
			#print "QUIT"
			return (42, OGbackground, self.trackback)
		

def FileRead(toParse):
	f = open(toParse, "r")
	fLines = f.readlines()
	f.close()
#	print "blah",fLines
	FilesList = []
	for n in range(len(fLines)):
#		g = open(fLines[n], "r")
#		gRead = g.read()
#		g.close()
		p = re.compile(".{1,}\.png") # RegEx that matches any expression ending with '.png'
		m = p.search(fLines[n])
		FilesList.append(m.group())
#	print FilesList
	return FilesList

