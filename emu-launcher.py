#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser

import pygame, sys
import os
from pygame.locals import *
import subprocess
# play random game?
#import random
import glob

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.key.set_repeat(300, 25)
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.HWACCEL|pygame.HWSURFACE)
#screen = pygame.display.set_mode((0,0),pygame.HWACCEL|pygame.HWSURFACE)
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
pitems = []

def center_element_in_area(element,area):
    x = area[2]/2 - element.get_width()/2
    y = area[3]/2 - element.get_height()/2
    position = (x+area[0],y+area[1])
    screen.blit(element,position)

def scale_image(image,width=0,height=0):
    img = pygame.image.load("extra/images/"+image).convert_alpha()
    w = img.get_width()
    h = img.get_height()
    if height > 0 and width > 0:
        h = height
        w = width
    elif height > 0:
        h = height
        w = h / float(img.get_height()) * float(img.get_width())
    elif width > 0:
        w = width
        h = w / float(img.get_width()) * float(img.get_height())
    img = pygame.transform.scale(img, (int(w * convY),int(h*convX) ))
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
    font_size = int(26*convY)
    font_item = pygame.font.Font(font2_name, font_size)
    list_area = (screenX/16*9*convX, screenY/9*convY, screenX/16*6*convX, screenY/9*7*convY)
    itemh = font_size + 14
    selectmarge = 50
    selectleft = list_area[0]-selectmarge
    visibleitems = int((list_area[3]) / itemh)
    print list_area[3], list_area[1], itemh

    original_folder = folder
    loadfolder(folder)
    current = 0
    offset = 0
    machine_img = scale_image(machine_img,width=screenX/4)

    while True:
        event = pygame.event.wait()
        screen.fill((236,236,236))

        if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT):
            return

        if event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_RIGHT):
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

        if (event.type == KEYDOWN and (event.key == K_PAGEDOWN or event.key == K_PAGEUP)):
            if event.key == K_PAGEUP:
                current -= visibleitems
                offset -= visibleitems
            else:
                current += visibleitems
                offset += visibleitems
            if current - offset >= visibleitems:
                offset = current

        #don't go outside pitems
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

        if len(pitems) > 0:
            pospaint=0
            rectsel = pygame.Rect( selectleft*convX, (list_area[1]+cpos*itemh-3), list_area[2], itemh-2 )
            screen.fill(red_color, rectsel)
            for compta in range(0, min(visibleitems, len(pitems) )):
                img_folderico = scale_image("folder.png")
                item = pitems[compta+offset]
                leftpad = 0

                if os.path.isdir( item["value"] ):
                    draw_element(img_folderico, (list_area[0], list_area[1]+(itemh * pospaint)+4),1)
                    leftpad = 50

                item_name = font_item.render(item["name"], 1, font_color if pospaint != cpos else white_color)
                draw_element(item_name, (list_area[0]+leftpad, list_area[1] + (itemh * pospaint)),1)

                # FIXME: crop the file name
                if ( item_name.get_width() >= list_area[2]-selectmarge*2 ):
                    item_name = font_item.render("...", 1, font_color if pospaint != cpos else white_color)
                    draw_element(item_name, (list_area[0]+list_area[2]-selectmarge*2, list_area[1]+(itemh * pospaint)),1)
                pospaint += 1

        if offset+visibleitems < len(pitems):
            item_name = font_item.render("...", 1, red_color)
            draw_element(item_name, (selectleft , list_area[1]+list_area[3]),1)
        if offset > 1:
            item_name = font_item.render("...", 1, red_color)
            draw_element(item_name, (selectleft, list_area[1]-30),1)

        if len(pitems)-1 > 0:
            npos = list_area[1]+current * list_area[3] / len(pitems)-1
        else:
            npos = list_area[1]

        render_text(title,machine_font,(screenX/32,screenY/18),font_color)
        render_text(currentfolder,font_subtitle,(screenX/2,screenY/18),red_color)
        rectsel = pygame.Rect( (list_area[0]+list_area[2]), list_area[1], 6, list_area[3])
        pygame.draw.circle ( screen, red_color, (int( (list_area[0]+list_area[2]+3)), int(npos)), 8)
        screen.fill(red_color, rectsel)
        draw_element(machine_img, (screenX/8,screenY/9),1)
        #draw file selector
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
        screen.fill((236,236,236))
        draw_element(ft, (0,0))
        if moving == 0:
            event = pygame.event.wait()
            if (event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE)) or (event.type == QUIT):
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_RETURN):
                file = filesel(items[current]["name"], items[current]["roms"], items[current]["image"])
                if file != None:
                    print "JUGANDO! %s" %(file)
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
