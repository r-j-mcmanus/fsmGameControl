
import pygame

from Conts import *



class CollisionHandler(object):

    def __init__(self):
        self.worldGeometry = []

        self.worldGeometry.append(pygame.Rect(100.0, 130.0, 20, 40))

    def __call__(self, player):
        #collision with window
        player.Lx = 1
        player.Ly = 1

        dv = player.gSpeed*player.gDir[x]*timePerFrameInms
        L = (-player.left + 0) / dv
        if 0 <= L <= 1 and dv<0:
            player.Lx = L

        dv = -dv
        L = (-300 + (player.right) ) / dv
        if 0 <= L <= 1 and dv<0:
            player.Lx = L
        

        lx = -1
        lx1 = -1
        ly = -1
        lx2 = -1

        for geometry in self.worldGeometry:

            lx = -1
            ly = -1

            lx1 = (geometry.right - player.left) / (player.gDir[x]*player.gSpeed*timePerFrameInms)
            lx2 = (geometry.left - player.right) / (player.gDir[x]*player.gSpeed*timePerFrameInms)
            if 0<=lx1<=1 or 0<=lx2<=1:
                if not (0<=lx2<=1) and player.gDir[x]<0:
                    lx = lx1
                    colSide = "left"
                elif not (0<=lx1<=1) and player.gDir[x]>0:
                    lx = lx2
                    colSide = "right"
            else:
                continue

            """if player.onGround == False:
                dv_y = player.yJumpSpeed + player.yImpulse
                ly1 = (geometry.top - player.bottom) / (dv_y*timePerFrameInms)
                ly2 = (geometry.bottom - player.top) / (dv_y*timePerFrameInms)
                if 0<=ly1<=1 or 0<=ly2<=1:
                    if not 0<=ly2<=1 and dv_y<0:
                        ly = ly1
                        print "hit top"
                    elif not 0<=ly1<=1 and dv_y>0:
                        ly = ly2
                        print "hit bottom"
                else:
                    continue
            elif player.top < geometry.bottom and geometry.top < player.bottom:
                ly = 0
            else:
                continue"""

            if player.top < geometry.bottom and geometry.top < player.bottom:
                ly = 0  
            
            if lx != -1 and ly != -1:
                    player.Lx = lx
            