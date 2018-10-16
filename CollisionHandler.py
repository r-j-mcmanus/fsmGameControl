

x,y = 0,1
e = 0.01

counter = 0

FPS = 60
timePerFrameInms = 1.0/FPS*1000

class CollisionHandler(object):

    def __init__(self):
        self.counter = 0

    def __call__(self, player):
        #collision with window
        player.Lx = 1
        dv = player.gSpeed*player.gDir[x]*timePerFrameInms
        # left - right
        L = (-player.pos[x] + 0) / dv
        if 0 <= L <= 1 and dv<0:
            player.Lx = L

        # left - rightaaa
        dv = -dv
        L = (-300 + (player.pos[x] + player.body.width) ) / dv
        if 0 <= L <= 1 and dv<0:
            player.Lx = L