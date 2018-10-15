

x,y = 0,1

class CollisionHandler(object):

    def __init__(self):
        self.e = 0.1

    def __call__(self, player):
        #collision with window
        player.Lx = 1
        L = (player.pos[x] - 0) / (player.gSpeed*player.gDir[x])
        print "L", L
        if 0 <= L <= 1:
            player.Lx = (L+self.e)

        L = (player.pos[x] + player.body.width - 300) / (player.gSpeed*player.gDir[x])
        if 0 < L < 1:
            player.Lx = (L-self.e)

