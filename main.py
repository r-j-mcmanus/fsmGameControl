

import pygame, sys
from pygame.locals import QUIT


import numpy as np

from View import View
from Geometry import Geometry
from FSMs import FSMs
from AIFSM import AIFSM
from TimerController import TimerController
from InputHandler import InputHandler
from CollisionHandler import CollisionHandler
from Entity import Entity

from Conts import *
    
x=0
y=1



def checkQuit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

"""--------------------------------------------------------"""



def timeIntegrator(entities):    
    for e in entities:
        e.pos[x] += e.gDir[x]*e.gSpeed*timePerFrameInms*e.Lx
        e.pos[y] += (e.yJumpSpeed + e.yImpulse)*timePerFrameInms*e.Ly
        e.yJumpSpeed += e.yImpulse


def drawScene(surface, view, entities, geometries):
    view.centerView()

    surface.fill(Colors.black)

    for e in entities:
        e.draw(surface, view)

    for g in geometries:
        g.draw(surface, view)

    pygame.display.update()

def main():

    pygame.init()
    pygame.display.set_caption('Window')  

    timerController = TimerController()
    inputHandler = InputHandler()

    fsms = FSMs(timerController, inputHandler.pressed, inputHandler.previouslyPressed)

    timeSinceRender = timePerFrameInms+1
  
    view = View(size = (300,300))
    
    surface = pygame.display.set_mode(view.size)

    clock = pygame.time.Clock()

    collisionHandler = CollisionHandler()

    geometries = [
        Geometry(pygame.Rect(100.0, 130.0, 100, 40)),
        Geometry(pygame.Rect(10.0, 70.0, 40, 40)),
        Geometry(pygame.Rect(0.0, 160.0, 300, 40)),
        Geometry(pygame.Rect(-40,0,40,200)),
        Geometry(pygame.Rect(300,0,40,200))
    ]

    entities = [
        Entity(entityType = "player", pos = (100,100)),
        Entity(entityType = "yBox", pos = (50.0, 150.0))
    ]

    view.hook(lambda : entities[0].pos)

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

            #run fsm
            fsms(entities, inputHandler.pressed, inputHandler.previouslyPressed)

            #find constraints (i.e l used in time integrator)
            collisionHandler(entities, geometries)

            #update world
            timeIntegrator(entities)
        
        drawScene(surface, view, entities, geometries)

if __name__ == '__main__':
    main()