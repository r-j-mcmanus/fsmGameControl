
import pygame, sys
from pygame import K_a, K_s, K_d, K_w, K_LSHIFT, K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT

class Actions:
    left = 0
    right = 1
    up = 2
    down = 3
    dodge = 4
    attack = 5
    jump = 6



class InputHandler():

    def __init__(self):

        self.keyToActionMap = {
                    K_a:Actions.left,
                    K_s:Actions.down,
                    K_w:Actions.up,
                    K_d:Actions.right,
                    K_DOWN:Actions.jump,
                    K_LEFT:Actions.dodge,
                    K_RIGHT:Actions.attack,
                    }

        self.pressed = {Actions.left:False,
                        Actions.right:False,
                        Actions.up:False,
                        Actions.down:False,
                        Actions.dodge:False,
                        Actions.attack:False,
                        Actions.jump:False}

        self.previouslyPressed = {Actions.left:False,
                        Actions.right:False,
                        Actions.up:False,
                        Actions.down:False,
                        Actions.dodge:False,
                        Actions.attack:False,
                        Actions.jump:False}

        print self.keyToActionMap.keys()

    def updateKeyState(self):
        rawInput = pygame.key.get_pressed()

        for key in self.keyToActionMap.keys():
            action = self.keyToActionMap[key]
            self.previouslyPressed[action] = self.pressed[action]
            if rawInput[key]:
                self.pressed[action] = True
            else:
                self.pressed[action] = False

