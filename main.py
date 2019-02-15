

import pygame, sys
from pygame import K_a, K_s, K_d, K_w, K_LSHIFT, K_SPACE, K_UP, K_DOWN,K_LEFT, K_RIGHT
from pygame.locals import QUIT


import numpy as np

from PlayerFSM import PlayerFSM
from AIFSM import AIFSM
from TimerController import TimerController
from InputHandler import InputHandler
from CollisionHandler import CollisionHandler
from Player import Player

from Conts import *

from PlayerConsts import *
    


def checkQuit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

"""--------------------------------------------------------"""

def timeIntegrator(player):    

    player.pos[x] += player.gDir[x]*player.gSpeed*timePerFrameInms*player.Lx
    player.pos[y] += (player.yJumpSpeed + player.yImpulse)*timePerFrameInms*player.Ly
    player.yJumpSpeed += player.yImpulse


def drawScene(surface, player):
    surface.fill(Colors.black)
    pygame.draw.rect(surface, player.colour, player.body.move(player.pos))

    pygame.draw.rect(surface, Colors.green, pygame.Rect(100.0, 130.0, 100, 40))
    pygame.draw.rect(surface, Colors.green, pygame.Rect(10.0, 70.0, 40, 40))
    pygame.draw.rect(surface, Colors.green, pygame.Rect(0.0, 160.0, 300, 40))

    if player.hurtBool:
        pygame.draw.rect(surface, Colors.yellow, player.colBox.move(player.pos),0)
    if player.hitBool:
        pygame.draw.rect(surface, Colors.yellow, player.hitbox.move(player.pos+player.hitboxOffset()),1)

    pygame.display.update()

def main():
    global surface
    global timerController

    timerController = TimerController()

    timeSinceRender = timePerFrameInms+1

    pygame.init()
    pygame.display.set_caption('Window')    
    
    viewSize = (300,300)
    surface = pygame.display.set_mode(viewSize)

    clock = pygame.time.Clock()

    player = Player()
    playerFSM = PlayerFSM(timerController)
    inputHandler = InputHandler()
    collisionHandler = CollisionHandler()

    #main game loop
    while True:
        timeSinceRender += clock.tick()
        #timeSinceRender is in milliseconds 
        #print "timeSinceRender", timeSinceRender
        #counter = counter +1

        while timeSinceRender > timePerFrameInms:

            timeSinceRender -= timePerFrameInms

            checkQuit()

            #update logic
            inputHandler.updateKeyState()
            timerController.tick()

            #update intents
            playerFSM(player, inputHandler.pressed, inputHandler.previouslyPressed)

            AIFSM()

            #find contraints (i.e l used in time integrator)
            collisionHandler(player)

            #update world
            timeIntegrator(player)
        
        drawScene(surface, player)

if __name__ == '__main__':
    main()