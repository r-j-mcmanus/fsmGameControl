

import pygame, sys
from pygame import K_a, K_s, K_d, K_w, K_LSHIFT, K_SPACE, K_UP, K_DOWN,K_LEFT, K_RIGHT
from pygame.locals import QUIT


import numpy as np

from PlayerFSM import PlayerFSM
from TimerController import TimerController
from InputHandler import InputHandler
from CollisionHandler import CollisionHandler

x,y=0,1

FPS = 60
timePerFrameInms = 1.0/FPS*1000

grav = 0.0015

class Colors:
    white = (255,255,255)
    black = (000,000,000)
    red   = (255,000,000)
    green = (000,255,000)
    blue  = (000,000,255)
    yellow= (255,255,000)
    purple= (255,000,255)

class Player(object):
    def __init__(self):
        self.body = pygame.Rect(0, 0, 10, 10)
        self.colour = Colors.red
        self.stateID = PlayerFSM.StateID.Standing
        self.pos = np.array([10.0, 150.0])
        self.gDir = np.array([1,0]) # right == 1 or left == -1
        self.gSpeed = 0 #ground speed
        self.colBox = pygame.Rect(0, 0, 10, 10)
        self.physColBool = True
        self.hurtbox = pygame.Rect(0, 0, 10, 10)
        self.hurtBool = True
        self.hitBool = False
        self.hitbox = pygame.Rect(0, 3, 10, 4)
        self.yJumpSpeed = 0
        self.onGround = True
        self.Dgrav = 0
        self.Lx = 1

    def move(self, x, y):
        self.pos += [x,y]

    def hitboxOffset(self):
        return [0.5*((self.gDir[x]+1)*self.colBox.width + (self.gDir[x]-1)*self.hitbox.width),0]


def checkQuit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

"""--------------------------------------------------------"""

def timeIntegrator(player):
    global grav
    if player.onGround:
        player.pos += player.gDir*player.gSpeed*timePerFrameInms*player.Lx
    else:
        player.pos[x] += player.gDir[x]*player.gSpeed*timePerFrameInms*player.Lx
        player.yJumpSpeed += grav*(1 + player.Dgrav)*timePerFrameInms
        player.pos[y] += player.yJumpSpeed*timePerFrameInms + grav*(1 + player.Dgrav)*timePerFrameInms*timePerFrameInms
        if player.pos[y]>=150:
            player.pos[y] = 150


def drawScene(surface, player):
    surface.fill(Colors.black)
    pygame.draw.rect(surface, player.colour, player.body.move(player.pos))
    if player.hurtBool:
        pygame.draw.rect(surface, Colors.yellow, player.colBox.move(player.pos),1)
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

            #find contraints
            collisionHandler(player)

            #update world
            timeIntegrator(player)
        
        drawScene(surface, player)

if __name__ == '__main__':
    main()