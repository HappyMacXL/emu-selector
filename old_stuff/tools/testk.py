#! /usr/bin/python

import pygame, sys
from pygame.locals import *

import pygame


pygame.init()
screen = pygame.display.set_mode((640, 480))



while True:

	event = pygame.event.wait()
	
	if event.type == KEYDOWN:
		print event.key, event.scancode
		if  event.key == K_ESCAPE :
			sys.exit()	
