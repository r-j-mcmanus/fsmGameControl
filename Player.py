
import pygame

from PlayerFSM import PlayerFSM

import numpy as np

from Conts import *

class Player(object):
    def __init__(self):
        self.body = pygame.Rect(0, 0, 10, 10)
        self.colour = Colors.red
        self.stateID = PlayerFSM.StateID.Standing
        self.pos = np.array([50.0, 150.0])
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
        self.landed = False
        self.Dgrav = -1
        self.Lx = 1
        self.Ly = 1
        self.vel = np.array([0,0])

    def move(self, x, y):
        self.pos += [x,y]

    def hitboxOffset(self):
        return [0.5*((self.gDir[x]+1)*self.colBox.width + (self.gDir[x]-1)*self.hitbox.width),0]

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
        
    