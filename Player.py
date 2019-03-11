
import pygame

from PlayerFSM import StateID

import numpy as np

from Conts import *

from PlayerConsts import *

class direction:
    right = 1
    left = -1

class Player(object):
    def __init__(self, bodyRect = pygame.Rect(0, 0, 10, 10), pos = np.array([50.0, 150.0])):
        self.body = bodyRect
        self.colour = Colors.red
        self.stateID = StateID.Standing
        self.pos = np.array(pos)
        self.__dir = direction.right
        self.gVec = np.array([1,0]) # gVec[0] >=0 for notmalisation
        self.gSpeed = 0 # ground speed
        self.colBox = bodyRect
        self.physColBool = True
        self.hurtbox = bodyRect
        self.hurtBool = True
        self.hitBool = False
        self.hitbox = pygame.Rect(0, 3, 10, 4)
        self.yJumpSpeed = 0
        self.onGround = True
        self.landed = False
        self.startFalling = False
        self.graceJumpBool = False
        self.followUpAttackBool = False
        self.attackEndBool = False
        self.Dgrav = -1
        self.Lx = 1
        self.Ly = 1
        self.vel = np.array([0,0])
        self.highJumpBool = True
        self.changeDirection = 1

        self.xImpulse = 0
        self.maxXSpeed = 100

        #we use two basis, x, y which are window aligned 
        #and g, h which are ground aligned
        #in principle. so for not in practicea

    def getBody(self):
        return self.body.move(self.pos)

    def getColBox(self):
        return self.colBox.move(self.pos)

    def getHitBox(self):
        return self.hitbox.move(self.pos+self.hitboxOffset())

    def move(self, x, y):
        self.pos += [x,y]

    def hitboxOffset(self):
        return [0.5*((self.gDir[x]+1)*self.colBox.width + (self.gDir[x]-1)*self.hitbox.width),0]

    @property
    def speed(self):
        if self.onGround:
            return self.gSpeed
        else:
            return self.aSpeed

    def applyChangeDir(self):
        self.__dir *= self.changeDirection
        self.changeDirection = 1

    @property
    def gDir(self):
        return self.__dir*self.gVec

    @property
    def dir(self):
        return self.__dir

    @dir.setter
    def dir(self, direction):
        if direction != 0:
            self.__dir = direction
 
    @property
    def left(self):
        return self.pos[x]

    @property
    def right(self):
        return self.pos[x] + self.body.width    

    @property
    def top(self):
        return self.pos[y]

    @property
    def bottom(self):
        return self.pos[y] + self.body.height 

    @property
    def yImpulse(self):
        return gravImpulse*(1 + self.Dgrav)
        
    