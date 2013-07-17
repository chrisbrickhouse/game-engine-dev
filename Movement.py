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

def start(sprite, event, obstacles):
	if obstacles != []:
		if event == pygame.K_LEFT:
			sprite.animate.setCycle('left')
			sprite.moveleft()
			sprite.animate.update(True)
			sprite.update(obstacles)
		if event == pygame.K_RIGHT:
			sprite.animate.setCycle('right')
			sprite.moveright()
			sprite.animate.update(True)
			sprite.update(obstacles)
		if event == pygame.K_UP:
			sprite.animate.setCycle('up')
			sprite.moveup()
			sprite.animate.update(True)
			sprite.update(obstacles)
		if event == pygame.K_DOWN:
			sprite.animate.setCycle('down')
			sprite.movedown()
			sprite.animate.update(True)
			sprite.update(obstacles)
	else:
		if event == pygame.K_LEFT:
			sprite.moveleft()
			sprite.update(obstacles)
		if event == pygame.K_RIGHT:
			sprite.moveright()
			sprite.update(obstacles)
		if event == pygame.K_UP:
			sprite.moveup()
			sprite.update(obstacles)
		if event == pygame.K_DOWN:
			sprite.movedown()
			sprite.update(obstacles)
		
def stop(sprite, event):
	if (event == K_UP) and (sprite.state == 'up'):
		sprite.displacement = [0,0]
		sprite.old_state = 'up'
		sprite.state = 'still'
	if (event == K_DOWN) and (sprite.state == 'down'):
		sprite.displacement = [0,0]
		sprite.old_state = 'down'
		sprite.state = 'still'
	if (event == K_RIGHT) and (sprite.state == 'right'):
		sprite.displacement = [0,0]
		sprite.old_state = 'right'
		sprite.state = 'still'
	if (event == K_LEFT) and (sprite.state == 'left'):
		sprite.displacement = [0,0]
		sprite.old_state = 'left'
		sprite.state = 'still'
