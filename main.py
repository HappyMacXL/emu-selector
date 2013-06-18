#!/usr/bin/env python
import ConfigParser

import pygame, sys
import os
from pygame.locals import *

import random
#import library
import time
import subprocess

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.key.set_repeat(300, 25)

font_name = "extra/ttf/Orbitron-Regular.ttf"
font2_name = "extra/ttf/QuattrocentoSans-Regular.ttf"
tada = pygame.mixer.Sound("extra/sounds/ultimate.ogg")
pygame.mouse.set_visible( False )
screen = pygame.display.set_mode((0,0))
#screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)
screenX = screen.get_width()
screenY = screen.get_height()
convX = float( screenX ) / float( 1920 )
convY = float( screenY ) / float( 1080 )
#print screenX,screenY,convX,convY


def scale_image(image):
    img = pygame.image.load("extra/images/"+image).convert_alpha()
    if convX != 1 or convY != 1:
        img = pygame.transform.scale( img, (int(img.get_width() * convX), int(img.get_height() *convY)) )
    return img


def paintelement( image , px ):
    dy = (-100 * convY ) + screenY/2 - image.get_height() / 2
    dx = screenX/2- image.get_width()/2+px
    screen.blit( image, (dx, dy) )


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

def main():
    items,config = get_machines()
    tada.play()
    ft = scale_image("fonstram.png")
    moving = 0
    moving_count =0
    moving_start = 0
    moving_duration = 180
    offsetX = 0
    moving_dist = screenX / 2
    current = 0
    nitems = len( items)
    font = pygame.font.Font(font_name, int(100*convY))
    font2 = pygame.font.Font(font2_name, int(22*convY))
    help2 = font2.render("F1 - HELP , O - Extra menu", 1, (187,17, 66))
    axisval = 0
    #print items
    while True:
        event = None
        if moving == 0:
            event = pygame.event.wait()
            #print " event: %s\n" %event

            if (event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE)) or (event.type == QUIT) :
                img = scale_image("On-Off.png")
                screen.blit( img, (0,0))
                pygame.display.update()
                time.sleep(1)
                sys.exit()

            if (event.type == KEYDOWN and (event.key == K_o))  :
                sys.exit( 199 )

            if event.type == KEYDOWN and (event.key == K_RETURN) :
                print items[current]["name"], items[current]["roms"], items[current]["image"]
                ## ./filesel.py "TITLE" "./roms/snes/" './extra/images/snes.png'
                file = subprocess.call(['./filesel.py',items[current]["name"], items[current]["roms"], items[current]["image"]])
                #TODO: call subprocess to execute the emulator with rom :D
                print file
                #sys.exit( current + 2)

            if moving == 0:
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

#       screen.fill((230,230,230))
        screen.blit( ft, (0,0))

        nom = font.render(items[current]["name"], 1, (60,60, 60))

        if moving == 0:
            screen.blit( nom, (screenX/2 - nom.get_width()/2, screenY - (330*convY)))
            screen.blit( help2, ((screenX - (screenX/5) )- help2.get_width(), screenY - (935*convY)))

        paintelement( items[current]["picture"], offsetX )
        paintelement( items[((current + 1) % nitems)]["picture"], offsetX +screenX/2)
        paintelement( items[((current - 1) % nitems)]["picture"], offsetX -screenX/2)

        #paintelement( items[((current + moving*2) % nitems)]["image"], screenX*moving)

        pygame.display.update()
        #print " moving: %s\n moving_count: %s\n moving_start: %s\n moving_duration: %s\n offsetX: %s\n moving_dist: %s\n current: %s\n axisval: %s\n userevernt: %s\n" %(moving,moving_count,moving_start, moving_duration,offsetX, moving_dist, current,axisval,pygame.USEREVENT)


if __name__ == "__main__":
    main()
