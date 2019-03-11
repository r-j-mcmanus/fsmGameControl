

import pygame, sys
from pygame.locals import QUIT


import numpy as np

from PlayerFSM import PlayerFSM
from AIFSM import AIFSM
from TimerController import TimerController
from InputHandler import InputHandler
from CollisionHandler import CollisionHandler
from Player import Player

from Conts import *
    
x=0
y=1

class Geometry(object):
    def __init__(self, rect, colour = Colors.green):
        self.body = rect
        self.colour = colour

    @property
    def right(self):
        return self.body.right

    @property
    def top(self):
        return self.body.top

    @property
    def left(self):
        return self.body.left

    @property
    def bottom(self):
        return self.body.bottom

    @property
    def width(self):
        return self.body.width

    @property
    def height(self):
        return self.body.height

    def draw(self, surface, view):
        pygame.draw.rect(surface, self.colour, view.apply(self.body))

def checkQuit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

"""--------------------------------------------------------"""

class View(object):
    def __init__(self, size):
        self.size = size
        self.position = (0,0)
        self.offset = 150
        self.center = 0

    def centerView(self, pos):
        self.center = pos

    def apply(self, rect):
        return rect.move(-self.center+self.offset,0)

def timeIntegrator(player):    

    player.pos[x] += player.gDir[x]*player.gSpeed*timePerFrameInms*player.Lx
    player.pos[y] += (player.yJumpSpeed + player.yImpulse)*timePerFrameInms*player.Ly
    player.yJumpSpeed += player.yImpulse


def drawScene(surface, view, player, enemies, geometries):
    view.centerView(player.pos[0])

    surface.fill(Colors.black)
    pygame.draw.rect(surface, player.colour, view.apply(player.getBody()))

    for e in enemies:
        pygame.draw.rect(surface, e.colour, view.apply(e.getBody()))

    for g in geometries:
        g.draw(surface, view)

    if player.hurtBool:
        pygame.draw.rect(surface, Colors.yellow, view.apply(player.getColBox()) ,0)
    if player.hitBool:
        pygame.draw.rect(surface, Colors.yellow, view.apply(player.getHitBox()),1)

    pygame.display.update()

def main():

    pygame.init()
    pygame.display.set_caption('Window')  

    timerController = TimerController()
    player = Player()
    inputHandler = InputHandler()

    playerFSM = PlayerFSM(timerController, player, inputHandler.pressed, inputHandler.previouslyPressed)

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

    enemies = [
        Player(pos = (100,100)),
        Player(pos = (150,100))
    ]

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

            #AIFSM(enemies)

            #find contraints (i.e l used in time integrator)
            collisionHandler(player, enemies, geometries)

            #update world
            timeIntegrator(player)
        
        drawScene(surface, view, player, enemies, geometries)

if __name__ == '__main__':
    main()