

from Conts import *

import pygame


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