#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser

import pygame, sys
import os
from pygame.locals import *

import random
#import library
import subprocess
import inspect
import glob

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.key.set_repeat(300, 25)
#pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.HWACCEL|pygame.HWSURFACE)
screen = pygame.display.set_mode((0,0),pygame.HWACCEL|pygame.HWSURFACE)
screenX = screen.get_width()
screenY = screen.get_height()
convX = float(screenX) / float(1920)
convY = float(screenY) / float(1080)

font_color = (50,50,50)
white_color = (255,255,255)
red_color = (187,17,66)
font_name = "extra/ttf/Orbitron-Regular.ttf"
font2_name = "extra/ttf/QuattrocentoSans-Regular.ttf"
machine_font = pygame.font.Font(font_name, int(100*convY))
font_title = pygame.font.Font(font_name, int(48*convY))
font_subtitle = pygame.font.Font(font_name, int(28*convY))
font_item = pygame.font.Font(font2_name, int(26*convY))


##filesel.py
# load menu items
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
pitems = []


img_subtitle = font_subtitle.render(subtitle, 1, font_color)


def scale_image(image,width=0,height=0):
    img = pygame.image.load("extra/images/"+image).convert_alpha()
    h = img.get_width()  * convX
    w = img.get_height() * convY
    if height > 0 and width > 0:
        h = height
        w = width
    elif height > 0:
        h = height
        w = h / float(img.get_height()) * float(img.get_width())
    elif width > 0:
        w = width
        h = w / float(img.get_width()) * float(img.get_height())
    img = pygame.transform.scale(img, (int(h), int(w)) )
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
    dy = (-100 * convY) + screenY/2 - image.get_height()/2
    dx = screenX/2- image.get_width()/2+px
    draw_element(image, (dx, dy))


def get_machines():
    c = ConfigParser.ConfigParser()
    c.readfp(open("config.cfg"))
    machines = []
    for s in c.sections():
        if s != "config":
            items = dict(c.items(s))
            items["picture"] = scale_image(items["image"])
            machines.append(items)
    return machines,dict(c.items("config"))


def loadfolder( folder ):
    global currentfolder, pitems
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
    


def filesel(title, folder, machine_img):
    original_folder = folder
    loadfolder( folder )
    current = 0
    offset = 0
    
    
    #img_icon = scale_image(machine_img)
    img_icon = scale_image(machine_img)
    #img_icon = pygame.image.load("extra/images/"+machine_img)
    #w = 500
    #h = w / float(img_icon.get_width()) * float(img_icon.get_height())
    #img_icon = pygame.transform.scale( img_icon, (int(w * convX), int(h *convY)) )

    while True:
        event = pygame.event.wait()
        screen.fill((236,236,236))

        if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT):
            return

        if event.type == KEYDOWN and event.key == K_RETURN:
            cpos = current - offset
            #don't crash when the directory is empty
            if current != -1:
                fname = pitems[cpos]["value"];
                if os.path.isdir( fname ):
                    loadfolder( fname )
                else:
                    return pitems[current]["value"]


        if (event.type == KEYDOWN and event.key == K_LEFT):
            if currentfolder != original_folder:
                dirname = os.path.dirname(currentfolder)
                if dirname == "/":
                    dirname = ""
                loadfolder( dirname )

        if (event.type == KEYDOWN and event.key == K_UP):
            current -= 1
            if current < offset:
                offset = current

        if (event.type == KEYDOWN and event.key == K_DOWN):
            current += 1
            if current - offset >= visibleitems:
                offset +=1

        if (event.type == KEYDOWN and event.key == K_RIGHT):
            cpos = current - offset
            #don't crash when the directory is empty
            if current != -1 and len(pitems) > 0:
                fname = pitems[cpos]["value"];
                if os.path.isdir( fname ):
                    loadfolder( fname  )
        if current < 0:
            current = 0
        if current >= len(pitems):
            current = len(pitems)-1

        if (current < offset) or (current >= offset+visibleitems):
            offset = current

        if offset >= len(pitems) - visibleitems:
            offset = len(pitems) - visibleitems
        if offset < 0:
            offset = 0

        cpos = current - offset
        rectsel = pygame.Rect( selectleft*convX, (startpos+cpos*itemh-3) * convY, selwidth*convX, itemh*convY-2 )
        if len(pitems) > 0:
            screen.fill(red_color, rectsel)

        pospaint=0
        
        if len(pitems) > 0:
            for compta in range(0, min(visibleitems, len(pitems) )):
                img_folderico = scale_image("folder.png")
                item = pitems[compta+offset]
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
            img_item = font_item.render("...", 1, red_color)

        if offset+visibleitems < len(pitems):
            draw_element(img_item, (selectleft , limitpos),1)

        if offset > 1:
            draw_element(img_item, (selectleft, startpos-30),1)

        if float(len(pitems)-1) > 0:
            npos = startpos+float(current) * float(limitpos-startpos) / float(len(pitems)-1)
        else:
            npos = startpos

        rectsel = pygame.Rect( (listleft+selwidth) * convX, startpos * convY, 6*convX, (limitpos-startpos)*convY )
        pygame.draw.circle ( screen, red_color, (int( (listleft+selwidth+3) * convX), int(npos * convY)), 8)
        screen.fill(red_color, rectsel)
        render_text(title,font_title,(screenX/6,screenY/6),font_color)
        draw_element(img_icon, (225, 400),1)
        #draw file selector
        render_text(currentfolder,font_subtitle,(screenX/2,screenY/6),red_color)
        pygame.display.update()

def main():
    tada = pygame.mixer.Sound("extra/sounds/ultimate.ogg")
    items,config = get_machines()
    tada.play()
    ft = scale_image("fonstram.png")
    moving = moving_count = moving_start = offsetX = current = 0
    moving_duration = 180
    moving_dist = screenX / 2
    nitems = len(items)
    while True:
        draw_element(ft, (0,0))
        if moving == 0:
            event = pygame.event.wait()
            if (event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE)) or (event.type == QUIT):
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_RETURN):
                file = filesel(items[current]["name"], items[current]["roms"], items[current]["image"])
                if file != None:
                    print "JUGANDO!"
            if (event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_RIGHT)):
                moving = 1 if (event.key == K_LEFT) else -1
                moving_start = pygame.time.get_ticks()
                pygame.time.set_timer(pygame.USEREVENT, 500)
            nom = machine_font.render(items[current]["name"], 1, (60,60, 60))
            screen.blit( nom, (screenX/2 - nom.get_width()/2, screenY - int(screenY/4)) )

        if moving != 0:
            moving_time = pygame.time.get_ticks() - moving_start
            if moving_time >= moving_duration:
                offsetX = 0
                current = current  - moving
                current %= nitems
                moving = 0
            else:
                offsetX = moving_dist * moving_time / moving_duration * moving
        paint_element(items[current]["picture"], offsetX)
        paint_element(items[(current + 1) % nitems]["picture"], offsetX+screenX/2)
        paint_element(items[(current - 1) % nitems]["picture"], offsetX-screenX/2)
        pygame.display.update()

if __name__ == "__main__":
    main()