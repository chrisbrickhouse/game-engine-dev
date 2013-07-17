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
import os
import ConfigParser
from pygame.locals import *

class Dialogue():
	def __init__(self, code, window, background):
		self.parser = ConfigParser.ConfigParser()
		self.parser.read(os.path.join('conf','Dialogue.config'))
		self.font = pygame.font.Font(None, 12)
		self.code = code
		self.window = window
		self.windowRect = self.window.get_rect()
		self.background = background
		self.location = []
		self.q = (self.windowRect.right - 800)/2
		print self.q
		
	def readTable(self):
		"""
		
		"""
		for option in self.parser.options('code'):
			if option == self.code:
				self.location.append(self.parser.get('code', option).split(" "))
				text = self.ReadText(self.location)
				return text
		
	def ReadText(self, location):
		#print self.location[0]
		f = open(os.path.join('conf','Dialogue.txt'), "r")
		f.seek(int(self.location[0][0]))
		text = f.read(int(self.location[0][1]))
		f.close
		return text
		
	def breakText(self, text):
		textlist = text.split("\n")
		return textlist
