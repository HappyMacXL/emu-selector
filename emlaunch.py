#! /usr/bin/python

import pygame, sys
import os
from pygame.locals import *

import random
#import library
import time

pygame.init()
pygame.mixer.init()
pygame.font.init()

font_name = "extra/ttf/Orbitron-Regular.ttf"
font2_name = "extra/ttf/QuattrocentoSans-Regular.ttf"
tada = pygame.mixer.Sound("extra/sounds/ultimate.ogg")
screenX = 1920
screenY = 1080
pygame.mouse.set_visible( False )
screen = pygame.display.set_mode((0,0))
#screen = pygame.display.set_mode((1920,1080))
screenX = screen.get_width()
screenY = screen.get_height()
convX = float( screenX ) / float( 1920 )
convY = float( screenY ) / float( 1080 )
print screenX,screenY,convX,convY


def drawimage( filename ):
    #similar to scale_image!!
    off = pygame.image.load("extra/images/"+filename)
    if convX != 1 or convY != 1:
            off = pygame.transform.scale( off, (int(off.get_width() * convX), int(off.get_height() *convY)) )

    screen.blit( off, (0,0))


def scale_image(image):
    img = pygame.image.load("extra/images/"+image).convert_alpha()
    if convX != 1 or convY != 1:
        img = pygame.transform.scale( img, (int(img.get_width() * convX), int(img.get_height() *convY)) )
    return img


def pintaelement( image , px ):
    dy = (-100 * convY ) + screenY/2 - image.get_height() / 2
    dx = screenX/2- image.get_width()/2+px
    screen.blit( image, (dx, dy) );


def get_machines():
    ins = open( "machines.conf", "r" )
    items = []
    for line in ins:
        line = line.replace("\n", "")
        newitem = line.split("|")
        img = scale_image(newitem[1])
        items.append ( {"nom":newitem[0], "image":img, "info":newitem[2], "extemula":newitem[3], "computer":newitem[4], "emula":newitem[5]} )
    ins.close()
    return items

def main():
    items = get_machines()
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
    nom = None
    info = None
    Inici = True
    help1 = font2.render("ONLINE HELP: E- Emulator , C - Computer , W - Emulator official site", 1, (187,17, 66))
    help2 = font2.render("F1 - HELP , O - Extra menu", 1, (187,17, 66))
    showinfo = False
    gleft = False
    gright= False
    axisval = 0
    while True:
        event = None
        if moving == 0 and Inici == False :
            event = pygame.event.wait()
     
            if (event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE)) or (event.type == QUIT) :
                if event.key == K_q:
                    drawimage( "On-Off.png" )
                    pygame.display.update()
                    time.sleep(1)
                sys.exit()
     
     
#            if (event.type == KEYUP and (event.key == K_j))  :
#                event = pygame.event.Event( pygame.USEREVENT )
            
            if (event.type == KEYDOWN and (event.key == K_t))  :
                sys.exit( 100 )
     
            if (event.type == KEYDOWN and (event.key == K_o))  :
                sys.exit( 199 )
     
            if event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_1) :
                sys.exit( current + 2)
     
#            if event.type == KEYDOWN and event.key == K_2 :
#                sys.exit( current + 2 + 50 )
#     
#            if event.type == KEYDOWN and event.key == K_3 :
#                sys.exit( current + 2 + 70 )
     
            if event.type == JOYBUTTONDOWN :
                sys.exit( current + 2)
     
     
            if event.type == pygame.USEREVENT + 1:
                showinfo = True
     
     
            if moving == 0:
                if (event.type == KEYDOWN and event.key == K_LEFT) :
                    moving = 1
                    moving_start = pygame.time.get_ticks()
                    pygame.time.set_timer(pygame.USEREVENT+2, 500)
                    gleft = True
     
     
                if (event.type == KEYDOWN and event.key == K_RIGHT) :
                    moving = -1
                    moving_start = pygame.time.get_ticks()
                    pygame.time.set_timer(pygame.USEREVENT+2, 500)
                    gright = True
     
     
     
            if (event.type == KEYUP and event.key == K_LEFT):
                pygame.time.set_timer(pygame.USEREVENT+2, 0)
                gleft = False
     
            if (event.type == KEYUP and event.key == K_RIGHT):
                pygame.time.set_timer(pygame.USEREVENT+2, 0)
                gleft = False
     
            if (event.type == pygame.USEREVENT + 2):
                pygame.time.set_timer(pygame.USEREVENT+2, 0)
                moving = 1 if gleft else -1
                moving_start = pygame.time.get_ticks()
                pygame.time.set_timer(pygame.USEREVENT+2, 500)
     
     
        if moving != 0:
            moving_time = pygame.time.get_ticks()    - moving_start
            if moving_time >= moving_duration:
                offsetX = 0
                current = current  - moving 
                current %= nitems
                moving = 0
                nom = None
                info = None
            else:
                offsetX = moving_dist * moving_time / moving_duration * moving
      
        screen.fill((230,230,230))
        screen.blit( ft, (0,0))

        if( nom == None):
            nom = font.render(items[current]["nom"], 1, (60,60, 60))


        if( info == None):
            info = font2.render(items[current]["info"], 1, (187,17, 66))

        if moving == 0:
            screen.blit( nom, (screenX/2 - nom.get_width()/2, screenY - (330*convY)))

            if showinfo:
                screen.blit( info, ((screenX - (screenX/5))- info.get_width(), screenY - (165*convY)))
                screen.blit( help1, ((screenX - (screenX/5) )- help1.get_width(), screenY - (135*convY)))
                screen.blit( help2, ((screenX - (screenX/5) )- help2.get_width(), screenY - (935*convY)))


        pintaelement( items[current]["image"], offsetX )
        pintaelement( items[((current + 1) % nitems)]["image"], offsetX +screenX/2)
        pintaelement( items[((current - 1) % nitems)]["image"], offsetX -screenX/2)

        if moving == -1:
            pintaelement( items[((current + 2) % nitems)]["image"], +screenX)

        if moving == 1:
            pintaelement( items[((current - 2) % nitems)]["image"], -screenX)

        #if event:
        #    if (event.type == pygame.USEREVENT)  :
        #        drawimage( "error/error"+ ( "%02d" % random.randrange( 1, 18) ) + ".png")

        pygame.display.update()

        #if event:
        #    if (event.type == pygame.USEREVENT) :
        #        pygame.time.set_timer(pygame.USEREVENT, 1000*60)
        #        pygame.time.set_timer(pygame.USEREVENT+1, 0)
        #
        #else:
        #    pygame.time.set_timer(pygame.USEREVENT, 1000*60*10)
        #    pygame.time.set_timer(pygame.USEREVENT+1, 1000*5)
        #    showinfo = False
        Inici = False




if __name__ == "__main__":
    main()