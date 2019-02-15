
import pygame

from PlayerFSM import PlayerFSM

import numpy as np

from Conts import *

from PlayerConsts import *

class direction:
    right = 1
    left = -1

class AI(object):
    def __init__(self):
        self.body = pygame.Rect(0, 0, 10, 10)
        self.colour = Colors.red
        self.pos = np.array([50.0, 150.0])
        self.colBox = pygame.Rect(0, 0, 10, 10)
        self.physColBool = True
        self.hurtbox = pygame.Rect(0, 0, 10, 10)
        self.hurtBool = True
        self.hitBool = False
        self.hitbox = pygame.Rect(0, 3, 10, 4)

    def move(self, x, y):
        self.pos += [x,y]
 
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

        
    