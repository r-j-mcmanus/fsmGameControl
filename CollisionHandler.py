
import pygame

from Conts import *
import numpy as np
from PlayerConsts import PlayerConsts

def clamp(nmin, nmax, n):
    return max(min(n,nmax), nmin)


class CollisionHandler(object):

    def __init__(self):
        pass

    def __call__(self, entities, geometries):
        #in principle, can move full range
        for e in entities:
            self.entitiesVsGeometry(e, geometries)

    def entitiesVsGeometry(self, e, geometries):
        e.Lx = 1
        e.Ly = 1


        #for window boundaries
        if  e.onGround:
            speed = PlayerConsts.Ground.maxSpeed
        else:
            speed = clamp(0,PlayerConsts.Air.maxSpeed, e.gSpeed + e.xImpulse * PlayerConsts.Air.xImpulseMagnitude)


        dv = speed * e.gDir[x]*timePerFrameInms

        L = (-e.left + 0) / dv
        if 0 <= L <= 1 and dv<0:
            e.Lx = L

        dv = -dv
        L = (-300 + (e.right) ) / dv
        if 0 <= L <= 1 and dv<0:
            e.Lx = L
        

        lx = -1
        lx1 = -1
        lx2 = -1
        ly = -1
        ly1 = -1
        ly2 = -1
        overlap_x=False
        overlap_y=False
        dv = 0
        l = [0,0]

        #e should fall if no collision with ground is found
        onGround = False

        for geometry in geometries:

            lx = -1
            ly = -1

            overlap_x = False
            overlap_y = False


            dv = e.gSpeed * e.gDir[x]

            lx1 = (geometry.right - e.left) / (dv*timePerFrameInms)
            lx2 = (geometry.left - e.right) / (dv*timePerFrameInms)

            # if 0<= lx1 <=1, then the projections overlap at l
            # let lx1 < lx2, if [lx1,lx2] supset [0,1], then projections overlap

            if 0<=lx1<=1 or 0<=lx2<=1:
                if not (0<=lx2<=1) and e.gDir[x]<0:
                    lx = lx1
                    # geometry.right = e.left
                elif not (0<=lx1<=1) and e.gDir[x]>0:
                    lx = lx2
                    # geometry.left = e.right
                else:
                    # Collision but not in direction of motion
                    continue
            else:
                l = [lx1,lx2]
                l.sort()
                if l[0] > 0 or 1 > l[1]:
                    continue
                else:
                    lx = 1
                    overlap_x = True
                    # The boxs' projection will lie 
                    # within each other for the duration 
                    # of the fraim.


            dv = e.yJumpSpeed + gravImpulse*(1 + e.Dgrav)

            ly1 = (geometry.bottom - e.top) / (dv*timePerFrameInms)
            ly2 = (geometry.top - e.bottom) / (dv*timePerFrameInms)
            if np.isnan(ly2):
                ly2 = -ly1

            if 0<=ly1<=1 or 0<=ly2<=1:
                if not (0<=ly2<=1) and dv <= 0:
                    ly = ly1
                    e.startFalling = True
                    # Collision on top of e, flag falling
                    # Remove to hug roof
                elif not (0<=ly1<=1) and dv >= 0:
                    ly = ly2
                    onGround = True
                    # Collision on bottom of e, flag landing
                else:
                    continue
            else:
                l = [ly1,ly2]
                l.sort()
                if l[0] > 0 or 1 > l[1]:
                    continue
                ly = 1
                overlap_y = True
              
            # This will evaluate true when moving across a surface
            if overlap_y and overlap_x:
                onGround = True
                continue

            # This proritises removing y velocity over x
            # needed so that when a corner is hit, we remove
            # y velocity but no x, moving onto the platform.
            # No if will result in being stuck at the corner
            # If lx!=1 will result in falling down at the corner
            # This way feels better and is more forgiving.
            if ly !=1:
                if ly < e.Ly:
                    e.Ly = ly
            else:
                if lx < e.Lx:
                    e.Lx = lx

        e.onGround = onGround