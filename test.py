#jumping 

    class Jumping(object):
        def __init__(self):
            pass

        def internal(self, player, pressed, previouslyPressed):
            if not pressed[K_DOWN] and previouslyPressed[K_DOWN]:
            	pos0 = player.pos
            	vel0 = slowUpVel



        def checkChange(self, player, pressed, previouslyPressed):
            if player.hitGound:
                return True, PlayerFSM.StateID.standing, ()
            return False, None, None

        def enter(self, player, direction = 0):
            print "enter jumping"
            pos0 = player.pos
            vel0 = fastUpVel

        def exit(self, player):
            player.hurtBool = True 
            #timerController.stopTimer(self.rollTimer)
