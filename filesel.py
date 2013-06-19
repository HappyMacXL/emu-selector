#! /usr/bin/python
# -*- coding: utf-8 -*- 
# ./filesel.py "TITLE" "./roms/snes/" './extra/images/snes.png'
import pygame, sys
import os
from pygame.locals import *

import random
import inspect
import glob

execpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.key.set_repeat(300, 25)
pygame.mouse.set_visible( False )
# init video
#screen = pygame.display.set_mode((0,0), FULLSCREEN)
screen = pygame.display.set_mode((0,0))
screenX = screen.get_width()
screenY = screen.get_height()
convX = float( screenX ) / float( 1920 )
convY = float( screenY ) / float( 1080 )
folder = sys.argv[2]
original_folder = folder

img_folderico = pygame.image.load("./extra/images/folder.png")
if convX != 1 or convY != 1:
    img_folderico = pygame.transform.scale( img_folderico, (int(img_folderico.get_width() * convX), int(img_folderico.get_height() *convY)) )


# load fonts
font_name = "extra/ttf/Orbitron-Regular.ttf"
font2_name = "extra/ttf/QuattrocentoSans-Regular.ttf"
font_title = pygame.font.Font(font_name, int(48*convY))
font_subtitle = pygame.font.Font(font_name, int(28*convY))
font_item = pygame.font.Font(font2_name, int(26*convY))
font_itemsel = pygame.font.Font(font2_name, int(20*convY))


# load menu items
pitems = []
title = sys.argv[1] # "CHAMELEONPI"
#subtitle = sys.argv[2] # "Retroarch MAME"
folder = sys.argv[2] # "/dades2/jocs/spectrum"


startpos = 250
itemh = 40
limitpos = 900
listleft = 900
selectmarge = 50
selectleft = listleft-selectmarge
selwidth = 700
visibleitems = (limitpos - startpos) / itemh

items = []
nitems = 0

filter = ""

img_title = font_title.render(title, 1, (50,50, 50))
#img_subtitle = font_subtitle.render(subtitle, 1, (50,50, 50))

def prepareitems( pfilter, force = False ):
    global items, nitems, current, pitems, filter, offset
    titems = []

    for item in pitems:
        if pfilter in item["name"].upper() or pfilter == "":
            titems.append( item )

    if len (titems) != 0 or force == True:
        items = titems
        nitems = len(items );
        current = 0
        offset = 0
        filter = pfilter

def loadfolder( folder ):
    global currentfolder, pitems, current, offset, img_folder
    pitems = []
    currentfolder = folder

    for file in glob.glob(currentfolder+"/*"):
        try:
            filen = file.decode('utf-8')
        except Exception: 
            filen = file
            print file
            pass
        
        pitems.append ( {"value":filen, "name":os.path.basename(filen)} )
    pitems.sort()
    current = 0
    offset = 0
    img_folder = font_subtitle.render(currentfolder, 1, (187,17,66))
    prepareitems( "", True )


def pintaelement( imatge, px, py, mw = 0  ):
    mw *= convX
    screen.blit( imatge, (px*convX, py*convY), (0, 0, mw if mw != 0 else imatge.get_width(), imatge.get_height()) );


loadfolder( folder )

img_icon = pygame.image.load("extra/images/"+sys.argv[3])
w = 500
h = w / float(img_icon.get_width()) * float(img_icon.get_height())
img_icon = pygame.transform.scale( img_icon, (int(w * convX), int(h *convY)) )



while True:
    event = pygame.event.wait()

    if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT) :
        sys.exit(-1)    

    if event.type == KEYDOWN and event.key == K_RETURN :
        cpos = current - offset
        #don't crash when the directory is empty
        if current != -1 :
            fname = items[cpos]["value"];
            if os.path.isdir( fname ) :
                loadfolder( fname )
            else:
                print( items[current]["value"] )
                sys.exit( 0 )

    if (event.type == KEYDOWN and event.key == K_UP) :
        current -= 1
        if current < offset:
            offset = current
    
    if (event.type == KEYDOWN and event.key == K_DOWN) :
        current += 1
        if current - offset >= visibleitems:
            offset +=1

    if (event.type == KEYDOWN and event.key == K_PAGEDOWN) :
        current += visibleitems
        offset += visibleitems
        if current - offset >= visibleitems:
            offset = current

    if (event.type == KEYDOWN and event.key == K_PAGEUP) :
        current -= visibleitems
        offset -= visibleitems
        if current - offset >= visibleitems:
            offset = current


    if event.type == KEYDOWN:
        nk = pygame.key.name( event.key )
        if nk == "space":
            nk = " " 
        if nk in "abcdefghijklmnopqrstuvwxyz1234567890 .,;:-__?¿*!\"·$%&/()=":
            prepareitems( filter + nk.upper())


    if (event.type == KEYDOWN and event.key == K_DELETE) :
        prepareitems( "" )

    if (event.type == KEYDOWN and event.key == K_BACKSPACE) :
        prepareitems( filter[:-1] )


    if (event.type == KEYDOWN and event.key == K_LEFT) :
        print original_folder, currentfolder
        #TODO: don't let go to other folders
        if currentfolder != original_folder:
            dirname = os.path.dirname(currentfolder)
            if dirname == "/":
                dirname = ""
            loadfolder( dirname )

    if (event.type == KEYDOWN and event.key == K_RIGHT) :
        cpos = current - offset
        #don't crash when the directory is empty
        if current != -1 :
            fname = items[cpos]["value"];
            if os.path.isdir( fname ) :
                loadfolder( fname  )



    if current < 0:
        current = 0
    if current >= nitems:
        current = nitems-1

    if (current < offset) or (current >= offset+visibleitems):
        offset = current

    if offset >= nitems - visibleitems:
        offset = nitems - visibleitems
    if offset < 0:
        offset = 0


    screen.fill((236,236,236))

    pintaelement( img_title, 225, 146 )
#    pintaelement( img_subtitle, 225, 200 )
    pintaelement( img_folder, 900, 146 )

    cpos = current - offset
    rectsel = pygame.Rect( selectleft*convX, (startpos+cpos*itemh-3) * convY, selwidth*convX, itemh*convY-2 )
    screen.fill((187,17,66), rectsel )

    pospaint=0

    for compta in range(0, min(visibleitems, nitems )) :
        item = items[compta+offset]
        leftpad = 0

        if os.path.isdir( item["value"] ) :
            pintaelement( img_folderico, listleft , startpos + (itemh * pospaint)+4 )
            leftpad = 50

        img_item = font_item.render(item["name"], 1, (50,50,50) if pospaint != cpos else (255,255,255))
        pintaelement( img_item, listleft+leftpad, startpos + (itemh * pospaint), selwidth-selectmarge*2)

        if( img_item.get_width() >= selwidth-selectmarge*2 ):

            img_item = font_item.render("...", 1, (50,50,50) if pospaint != cpos else (255,255,255))
            pintaelement( img_item, listleft+selwidth-selectmarge*2, startpos + (itemh * pospaint) )
        
        pospaint += 1

    img_item = font_itemsel.render(filter, 1, (187,17,66))
    pintaelement( img_item, listleft, startpos - 30 )

    img_item = font_itemsel.render("...", 1, (187,17,66))

    if offset+visibleitems < nitems:
        pintaelement( img_item, selectleft ,  limitpos )

    if offset > 1:
        pintaelement( img_item, selectleft,  startpos - 30 )


    rectsel = pygame.Rect( (listleft+selwidth) * convX, startpos * convY, 8*convX, (limitpos-startpos)*convY )
    screen.fill((220,220,220), rectsel )

    if float(nitems-1) > 0:
        npos = startpos+float(current) * float(limitpos-startpos) / float(nitems-1)
    else:
        npos = startpos

    pygame.draw.circle ( screen, (180, 180, 180), (int( (listleft+selwidth+4) * convX), int(npos * convY)), 10)
    pintaelement( img_icon, 225, 400 )
    pygame.display.update()