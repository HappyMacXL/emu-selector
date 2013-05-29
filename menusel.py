#! /usr/bin/python

import pygame, sys
from pygame.locals import *

import pygame
import os
import random
import inspect

execpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

pygame.init()
pygame.mixer.init()
pygame.font.init()

# init video
pygame.mouse.set_visible( False )
screen = pygame.display.set_mode((0,0))
#screen = pygame.display.set_mode((1920,1080))
screenX = screen.get_width()
screenY = screen.get_height()
convX = float( screenX ) / float( 1920 )
convY = float( screenY ) / float( 1080 )

# load fonts
font_name = execpath+"/extra/ttf/Orbitron-Regular.ttf"
font2_name = execpath+"/extra/ttf/QuattrocentoSans-Regular.ttf"

font_titol = pygame.font.Font(font_name, int(48*convY))
font_subtitol = pygame.font.Font(font_name, int(28*convY))
font_item = pygame.font.Font(font2_name, int(32*convY))
font_itemsel = pygame.font.Font(font2_name, int(20*convY))

# load menu items
pitems = []
ins = open( sys.argv[1], "r" )
titol = "chameleonpi"
subtitol = "menu"
compta = 0
for line in ins:
	line = line.replace("\n", "")
	compta += 1
	if compta == 1:
		titol = line
	elif compta == 2:
		subtitol = line
	else :
		newitem = line.split("|")
		pitems.append ( {"value":newitem[0], "name":newitem[1]} )
ins.close()

npitems = len( pitems) 

clock = pygame.time.Clock()

moving_dist = screenX / 2

current = 0

img_titol = font_titol.render(titol, 1, (50,50, 50))
img_subtitol = font_subtitol.render(subtitol, 1, (50,50, 50))


def pintaelement( imatge, px, py ):
	screen.blit( imatge, (px*convX, py*convY) );

startpos = 343
itemh = 54

pygame.key.set_repeat(300, 25)

items = []
nitems = 0

filter = ""

def prepareitems( pfilter ):

	global items, nitems, current, pitems, filter

	titems = []
	
	for item in pitems:
		if pfilter in item["name"].upper() or pfilter == "":
			titems.append( item )

	if len (titems) != 0:
		items = titems
		nitems = len(items );
		current = 0
		filter = pfilter


prepareitems( "" )
Inici = True

while True:

	if Inici == False :
		event = pygame.event.wait()

		if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT) :
			sys.exit(-1)	

		if event.type == KEYDOWN and event.key == K_RETURN :
				print( items[current]["value"] )
				sys.exit( 0 )

		if (event.type == KEYDOWN and event.key == K_UP) :
			current -= 1
			current %= nitems
	
		if (event.type == KEYDOWN and event.key == K_DOWN) :
			current += 1
			current %= nitems

		if event.type == KEYDOWN:
			nk = pygame.key.name( event.key )
			if nk == "space":
				nk = " " 
			if nk in "abcdefghijklmnopqrstuvwxyz1234567890 ":
				prepareitems( filter + nk.upper())


		if (event.type == KEYDOWN and event.key == K_DELETE) :
			prepareitems( "" )

		if (event.type == KEYDOWN and event.key == K_BACKSPACE) :
			prepareitems( filter[:-1] )

	screen.fill((236,236,236))

	pintaelement( img_titol, 225, 146 )
	pintaelement( img_subtitol, 225, 200 )

	rectsel = pygame.Rect( 370*convX, (startpos+current*itemh-3) * convY, 1160*convX, itemh*.8*convY )
	screen.fill((187,17,66), rectsel )

	pospaint=0
	for item in items :
		img_item = font_item.render(item["name"], 1, (50,50,50) if pospaint != current else (255,255,255))
		pintaelement( img_item, 425, startpos + (itemh * pospaint) )
		pospaint += 1

	img_item = font_itemsel.render(filter, 1, (187,17,66))
	pintaelement( img_item, 425 , startpos - 30 )

	pygame.display.update()

	Inici = False


