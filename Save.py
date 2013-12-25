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
import datetime
import os
from pygame.locals import *

def saveGame(currentWorld, heroPos, heroHealth, enemyPos, enemyHealth, enemyWorld, old, current):
	save = [currentWorld, heroPos, heroHealth, enemyPos, enemyHealth,enemyWorld, old, current]
	time = datetime.datetime.now().strftime('%H.%M.%S.%Y-%m-%d')
	time = time+'.save'
	print time
	with open(os.path.join('conf', 'SaveGames',time), 'w') as f:
		for i in save:
			f.write(str(i)+"\n")
			
def loadGame(window):
	values = []
	fileName = fileDialogue(window)
	with open(os.path.join('conf','SaveGames',fileName), 'r') as l:
		for line in l:
			values.append(line.rstrip())
	return values
	
def fileDialogue(window):
	FontRender = []
	rectList = []
	FileFont = pygame.font.SysFont("monospace", 20, bold=True)
	files = os.listdir(os.path.join('conf','SaveGames'))
	files.sort(reverse=True)
	for i in files:
		FontRender.append(FileFont.render(i,1,(0,0,0)))
		#print FontRender[0].get_rect().height, FontRender[0].get_rect().width
	yvalue = window.get_rect().height/2 - len(files)*35
	while True:
		rectNumber = 0
		window.fill((0,0,0))
		background = pygame.Surface((300,30))
		background.fill((166,166,166))
		for i in range(len(files)):
			window.blit(background, (window.get_rect().centerx-150,yvalue))
			window.blit(FontRender[i], (window.get_rect().centerx-150+6,yvalue+3))
			rectList.append(pygame.Rect((window.get_rect().centerx-150,yvalue),(300,30)))
			yvalue += 35
		pygame.display.flip()
		yvalue = window.get_rect().height/2 - len(files)*35
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): #check for quit signal and properly terminate.
				exit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					for rect in rectList:
						if rect.collidepoint(event.pos):
							return files[rectNumber]
						else:
							rectNumber+=1
			rectNumber = 0
		# +3
		# +10

