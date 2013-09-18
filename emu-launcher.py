#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser

import pygame, sys
import os
from pygame.locals import *

import random
#import library
import time
import subprocess
import inspect
import glob

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.key.set_repeat(300, 25)
#pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.HWACCEL|pygame.HWSURFACE)
screenX = screen.get_width()
screenY = screen.get_height()
convX = float( screenX ) / float(1920)
convY = float( screenY ) / float(1080)

font_color = (50,50,50)
white_color = (255,255,255)
red_color = (187,17,66)
font_name = "extra/ttf/Orbitron-Regular.ttf"
font2_name = "extra/ttf/QuattrocentoSans-Regular.ttf"
font = pygame.font.Font(font_name, int(100*convY))
font2 = pygame.font.Font(font2_name, int(22*convY))
font_title = pygame.font.Font(font_name, int(48*convY))
font_subtitle = pygame.font.Font(font_name, int(28*convY))
font_item = pygame.font.Font(font2_name, int(26*convY))
font_itemsel = pygame.font.Font(font2_name, int(20*convY))


##filesel.py
# load menu items
pitems = []
title =  "CHAMELEONPI"
subtitle =  "MAME"
folder = "/home/roms"

startpos = 250
itemh = 40
limitpos = 900
listleft = 900
selectmarge = 50
selectleft = listleft-selectmarge
selwidth = 700
visibleitems = (limitpos - startpos) / itemh
items2 = []
nitems2 = 0
filter = ""

img_title = font_title.render(title, 1, font_color)
img_subtitle = font_subtitle.render(subtitle, 1, font_color)
#render_text(title,font_title)
#render_text(subtitle,font_subtitle)
#help2 = font2.render("F1 - HELP , O - Extra menu", 1, red_color)


def scale_image(image):
    img = pygame.image.load("extra/images/"+image).convert_alpha()
    if convX != 1 or convY != 1:
        img = pygame.transform.scale( img, (int(img.get_width() * convX), int(img.get_height() *convY)) )
    return img

def scale_element(img,pos):
    if convX != 1 or convY != 1:
        #img = pygame.transform.scale(img, (int(img.get_width() * convX), int(img.get_height() *convY)) )
        pos = (pos[0]*convX,pos[1]*convY)
    return (img,pos)

def draw_element(image,position,scale=0):
    if scale:
        image,position = scale_element(image,position)
    screen.blit(image,position)

def render_text(text,font,position,color=font_color,antialias=1):
    surface = font.render(text,antialias,color)
    draw_element(surface, position)

def paint_element(image, px):
    dy = (-100 * convY ) + screenY/2 - image.get_height() / 2
    dx = screenX/2- image.get_width()/2+px
    draw_element(image, (dx, dy))


def get_machines(convX,convY):
    c = ConfigParser.ConfigParser()
    c.readfp(open("config.cfg"))
    machines = []
    for s in c.sections():
        if s != "config":
            items = dict(c.items(s))
            items["picture"] = scale_image(items["image"])
            machines.append(items)
    return machines,dict(c.items("config"))


def prepareitems( pfilter, force = False ):
    global items2, nitems2, current, pitems, filter, offset
    titems = []

    for item in pitems:
        if pfilter in item["name"].upper() or pfilter == "":
            titems.append( item )

    if len (titems) != 0 or force == True:
        items2 = titems
        nitems2 = len(items2 );
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
            #print file
            pass
        pitems.append ( {"value":filen, "name":os.path.basename(filen)} )
    pitems.sort()
    current = 0
    offset = 0
    img_folder = font_subtitle.render(currentfolder, 1, red_color)
    prepareitems( "", True )


def filesel(title, folder, machine_img):
    original_folder = folder
    loadfolder( folder )
    current = 0
    offset = 0

    img_icon = pygame.image.load("extra/images/"+machine_img)
    w = 500
    h = w / float(img_icon.get_width()) * float(img_icon.get_height())
    img_icon = pygame.transform.scale( img_icon, (int(w * convX), int(h *convY)) )

    while True:
        event = pygame.event.wait()

        if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT):
            return

        if event.type == KEYDOWN and event.key == K_RETURN:
            cpos = current - offset
            #don't crash when the directory is empty
            if current != -1:
                fname = items2[cpos]["value"];
                if os.path.isdir( fname ):
                    loadfolder( fname )
                else:
                    return items2[current]["value"]

        if (event.type == KEYDOWN and event.key == K_UP):
            current -= 1
            if current < offset:
                offset = current

        if (event.type == KEYDOWN and event.key == K_DOWN):
            current += 1
            if current - offset >= visibleitems:
                offset +=1

        if (event.type == KEYDOWN and (event.key == K_PAGEDOWN or event.key == K_PAGEUP)):
            if event.key == K_PAGEUP:
                current -= visibleitems
                offset -= visibleitems
            else:
                current += visibleitems
                offset += visibleitems
            if current - offset >= visibleitems:
                offset = current

        if event.type == KEYDOWN:
            nk = pygame.key.name( event.key )
            if nk == "space":
                nk = " "
            if nk in "abcdefghijklmnopqrstuvwxyz1234567890 .,;:-__?¿*!\"·$%&/()=":
                prepareitems( filter + nk.upper())

        if (event.type == KEYDOWN and event.key == K_DELETE):
            prepareitems( "" )

        if (event.type == KEYDOWN and event.key == K_BACKSPACE):
            prepareitems( filter[:-1] )

        if (event.type == KEYDOWN and event.key == K_LEFT):
            if currentfolder != original_folder:
                dirname = os.path.dirname(currentfolder)
                if dirname == "/":
                    dirname = ""
                loadfolder( dirname )

        if (event.type == KEYDOWN and event.key == K_RIGHT):
            cpos = current - offset
            #don't crash when the directory is empty
            if current != -1:
                fname = items2[cpos]["value"];
                if os.path.isdir( fname ):
                    loadfolder( fname  )
        if current < 0:
            current = 0
        if current >= nitems2:
            current = nitems2-1

        if (current < offset) or (current >= offset+visibleitems):
            offset = current

        if offset >= nitems2 - visibleitems:
            offset = nitems2 - visibleitems
        if offset < 0:
            offset = 0

        screen.fill((236,236,236))

        draw_element(img_title, (225, 146))
        draw_element(img_folder, (900, 146))
        cpos = current - offset
        rectsel = pygame.Rect( selectleft*convX, (startpos+cpos*itemh-3) * convY, selwidth*convX, itemh*convY-2 )
        screen.fill(red_color, rectsel )

        pospaint=0

        for compta in range(0, min(visibleitems, nitems2 )):
            img_folderico = scale_image("folder.png")
            item = items2[compta+offset]
            leftpad = 0

            if os.path.isdir( item["value"] ):
                draw_element(img_folderico, (listleft, startpos+(itemh * pospaint)+4),1)
                leftpad = 50

            img_item = font_item.render(item["name"], 1, font_color if pospaint != cpos else white_color)
            draw_element(img_item, (listleft+leftpad, startpos + (itemh * pospaint), selwidth-selectmarge*2),1)

            if( img_item.get_width() >= selwidth-selectmarge*2 ):

                img_item = font_item.render("...", 1, font_color if pospaint != cpos else white_color)
                draw_element(img_item, (listleft+selwidth-selectmarge*2, startpos+(itemh * pospaint)),1)

            pospaint += 1

        img_item = font_itemsel.render(filter, 1, red_color)
        draw_element(img_item, (listleft, startpos - 30),1)

        img_item = font_itemsel.render("...", 1, red_color)

        if offset+visibleitems < nitems2:
            draw_element(img_item, (selectleft , limitpos),1)

        if offset > 1:
            draw_element(img_item, (selectleft, startpos-30),1)

        rectsel = pygame.Rect( (listleft+selwidth) * convX, startpos * convY, 8*convX, (limitpos-startpos)*convY )
        screen.fill((220,220,220), rectsel )

        if float(nitems2-1) > 0:
            npos = startpos+float(current) * float(limitpos-startpos) / float(nitems2-1)
        else:
            npos = startpos

        pygame.draw.circle ( screen, (180, 180, 180), (int( (listleft+selwidth+4) * convX), int(npos * convY)), 10)
        draw_element(img_icon, (225, 400),1)
        pygame.display.update()



def main():
    tada = pygame.mixer.Sound("extra/sounds/ultimate.ogg")

    items,config = get_machines(convX,convY)
    tada.play()
    ft = scale_image("fonstram.png")
    moving = moving_count = moving_start = offsetX = current = 0
    moving_duration = 180
    moving_dist = screenX / 2
    nitems = len( items)
    while True:
        event = None
        if moving == 0:
            event = pygame.event.wait()

            if (event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE)) or (event.type == QUIT):
                draw_element(scale_image("On-Off.png"), (0,0))
                pygame.display.update()
                sys.exit()

            if (event.type == KEYDOWN and (event.key == K_o)):
                sys.exit( 199 )

            if event.type == KEYDOWN and (event.key == K_RETURN):
                print items[current]["name"], items[current]["roms"], items[current]["image"]
                file = filesel(items[current]["name"], items[current]["roms"], items[current]["image"])
                if file != None:
                    #TODO: call subprocess to execute the emulator with rom :D
                    print "JUGANDO!"

            if (event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_RIGHT)):
                moving = 1 if (event.key == K_LEFT) else -1
                moving_start = pygame.time.get_ticks()
                pygame.time.set_timer(pygame.USEREVENT+2, 500)

        if moving != 0:
            moving_time = pygame.time.get_ticks()    - moving_start
            if moving_time >= moving_duration:
                offsetX = 0
                current = current  - moving
                current %= nitems
                moving = 0
            else:
                offsetX = moving_dist * moving_time / moving_duration * moving

        draw_element(ft, (0,0))

        nom = font.render(items[current]["name"], 1, (60,60, 60))
        if moving == 0:
            screen.blit( nom, (screenX/2 - nom.get_width()/2, screenY - (330*convY)))

        help2 = font2.render("F1 - HELP , O - Extra menu", 1, red_color)
        tx = (screenX - (screenX/5) ) - help2.get_width()
        ty = screenY - (935*convY)
        render_text("F1 - HELP , O - Extra menu",font2,(tx,ty),red_color)

        paint_element(items[current]["picture"], offsetX)
        paint_element(items[((current + 1) % nitems)]["picture"], offsetX +screenX/2)
        paint_element(items[((current - 1) % nitems)]["picture"], offsetX -screenX/2)
        pygame.display.update()


if __name__ == "__main__":
    main()