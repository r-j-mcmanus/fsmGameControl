
#PlayerConsts

from PlayerConsts import PlayerConsts
import numpy as np
from InputHandler import Actions

x = 0
y = 1

global timerController

class PlayerFSM(object):
    """
    Will control the state of the player object, making minimal 
    changes to Player member variables e.g. state, direction, 
    speed and various bools
    """

    def __init__(self, timerControllerMain):
        global timerController
        timerController = timerControllerMain
        self.states = {
                        self.StateID.Standing :  PlayerFSM.Standing(),
                        self.StateID.Jab_1    :  PlayerFSM.Jab_1(),
                        self.StateID.Jab_2    :  PlayerFSM.Jab_2(),
                        self.StateID.Rolling  :  PlayerFSM.Rolling(),
                        self.StateID.Running  :  PlayerFSM.Running(),
                        self.StateID.RunAttack:  PlayerFSM.RunAttack(),
                        self.StateID.Jumping  :  PlayerFSM.Jumping(),
                        self.StateID.Falling  :  PlayerFSM.Falling(),
                    }
        self.messages = []
        
    class StateID:
        Standing = 0
        Running = 1
        Rolling = 2
        Attacking = 3
        Jab_1 = 4
        Jab_2 = 5
        RunAttack = 6
        Jumping = 7
        Falling = 8


    def __call__(self, player, pressed, previouslyPressed):
        self.messages = []
        state = self.states[player.stateID]
        state.internal(player, pressed, previouslyPressed)
        try:
            changeBool, changeID, chageArgs = state.checkChange(player, pressed, previouslyPressed)
        except ValueError:
                print "ERROR!!"
                print message
                print "changing from StateID ", player.stateID
                print "not enough values returned in state.checkChange"
                raise SystemExit

        if changeBool:
            state.exit(player)
            player.stateID = changeID
            try:
                self.states[player.stateID].enter(player, *chageArgs)
            except TypeError, message:
                print "ERROR!!"
                print message
                print "changing to StateID ", player.stateID
                print "Given chageArgs ", chageArgs
                raise SystemExit
            except KeyError, message:
                print "ERROR!"
                print message
                print "stateID", player.stateID, "not registered in PlayerFSM.states"
                raise SystemExit


    class Standing(object):
        def __init__(self):
            pass

        def internal(self, player, pressed, previouslyPressed):
            pass

        def checkChange(self, player, pressed, previouslyPressed):
            if pressed[Actions.left] and pressed[Actions.dodge]:
                return True, PlayerFSM.StateID.Rolling, (np.array([-1,0]),)
            if pressed[Actions.right] and pressed[Actions.dodge]:
                return True, PlayerFSM.StateID.Rolling, (np.array([1,0]),)
            if pressed[Actions.left]:
                return True, PlayerFSM.StateID.Running, (np.array([-1,0]),)
            if pressed[Actions.right]:
                return True, PlayerFSM.StateID.Running, (np.array([1,0]),)
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                return True, PlayerFSM.StateID.Jab_1, ()
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                return True, PlayerFSM.StateID.Jumping, ()
            return False, None, None

        def enter(self, player):
            print "enter standing"
            player.gSpeed = 0  

        def exit(self, player):
            pass    

    class Running(object):
        def __init__(self):
            pass

        def internal(self, player, pressed, previouslyPressed):
            if pressed[Actions.left] and not previouslyPressed[Actions.left]:
                player.gDir *= -1
                return
            if pressed[Actions.right] and not previouslyPressed[Actions.right]:
                player.gDir *= -1
                return

        def checkChange(self, player, pressed, previouslyPressed):
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge]:
                return True, PlayerFSM.StateID.Rolling, ()
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                return True, PlayerFSM.StateID.Jumping, ()
            if not pressed[Actions.left] and not pressed[Actions.right]:
                return True, PlayerFSM.StateID.Standing, ()
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                return True, PlayerFSM.StateID.RunAttack, ()

            return False, None, None

        def enter(self, player, direction):
            print "enter running"
            player.gSpeed = PlayerConsts.maxRunSpeed
            player.gDir = direction

        def exit(self, player):
            pass

    class Rolling(object):
        def __init__(self):
            global timerController 
            self.rollTimer = timerController.addTimer(PlayerConsts.Roll.duration, "rollTimer")
            self.rollCoolDown = timerController.addTimer(PlayerConsts.Roll.cooldown, "RollCooldown")

        def internal(self, player, pressed, previouslyPressed):
            pass

        def checkChange(self, player, pressed, previouslyPressed):
            if self.rollTimer.elapsed == self.rollTimer.duration:
                if pressed[Actions.left]:
                    return True, PlayerFSM.StateID.Running, (np.array([-1,0]),)
                if pressed[Actions.right]:
                    return True, PlayerFSM.StateID.Running, (np.array([1,0]),)
                return True, PlayerFSM.StateID.Standing, ()
            return False, None, None

        def enter(self, player, direction = [0,0]):
            print "enter rolling"
            if not np.array_equal(direction,[0,0]):
                player.gDir = direction
            else:
                print "wtf?"
            global timerController 
            timerController.startTimer(self.rollTimer)
            player.gSpeed = PlayerConsts.Roll.maxSpeed
            player.hurtBool = False 

        def exit(self, player):
            player.hurtBool = True 
            #timerController.stopTimer(self.rollTimer)

    class Jab_1(object):
        def __init__(self):
            global timerController 
            self.attackTimer = timerController.addTimer(PlayerConsts.Jab_1.duration, "Jab1_timer")
            self.jab2Bool = False

        def internal(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == PlayerConsts.Jab_1.hitBoxStart:
                player.hitBool = True
            if self.attackTimer.elapsed == PlayerConsts.Jab_1.hitBoxEnd:
                player.hitBool = False
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                self.jab2Bool = True

        def checkChange(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == self.attackTimer.duration:
                if self.jab2Bool:
                    return True, PlayerFSM.StateID.Jab_2, () 
                if pressed[Actions.left]:
                    return True, PlayerFSM.StateID.Running, (np.array([-1,0]),)
                if pressed[Actions.right]:
                    return True, PlayerFSM.StateID.Running, (np.array([1,0]),)
                return True, PlayerFSM.StateID.Standing, ()
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge] and pressed[Actions.left]:
                return True, PlayerFSM.StateID.Rolling, (np.array([-1,0]),)
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge] and pressed[Actions.right]:
                return True, PlayerFSM.StateID.Rolling, (np.array([1,0]),)
            return False, None, None

        def enter(self, player):
            print "enter jab 1"
            global timerController 
            timerController.startTimer(self.attackTimer)
            player.gSpeed = 0
            self.jab2Bool = False

        def exit(self, player):
            #timerController.stopTimer(self.rollTimer)
            player.hitBool = False

    class Jab_2(object):
        def __init__(self):
            global timerController 
            self.attackTimer = timerController.addTimer(PlayerConsts.Jab_2.duration, "Jab2_timer")

        def internal(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == PlayerConsts.Jab_2.hitBoxStart:
                player.hitBool = True
            if self.attackTimer.elapsed == PlayerConsts.Jab_2.hitBoxEnd:
                player.hitBool = False

        def checkChange(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == self.attackTimer.duration:
                if pressed[Actions.left]:
                    return True, PlayerFSM.StateID.Running, (np.array([-1,0]),)
                if pressed[Actions.right]:
                    return True, PlayerFSM.StateID.Running, (np.array([1,0]),)
                return True, PlayerFSM.StateID.Standing, ()
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge] and pressed[Actions.left]:
                return True, PlayerFSM.StateID.Rolling, (np.array([-1,0]),)
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge] and pressed[Actions.right]:
                return True, PlayerFSM.StateID.Rolling, (np.array([1,0]),)
            return False, None, None

        def enter(self, player):
            print "enter jab 2"
            global timerController 
            timerController.startTimer(self.attackTimer)
            player.gSpeed = 0

        def exit(self, player):
            #timerController.stopTimer(self.rollTimer)
            player.hitBool = False

    class RunAttack(object):
        def __init__(self):
            global timerController 
            self.attackTimer = timerController.addTimer(PlayerConsts.RunAttack.duration, "RunAttack_timer")

        def internal(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == PlayerConsts.RunAttack.hitBoxStart:
                player.hitBool = True
            if self.attackTimer.elapsed == PlayerConsts.RunAttack.hitBoxEnd:
                player.hitBool = False
            if self.attackTimer.elapsed == PlayerConsts.RunAttack.runEnd:
                player.gSpeed = 0

        def checkChange(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == self.attackTimer.duration:
                if pressed[Actions.left]:
                    return True, PlayerFSM.StateID.Running, (np.array([-1,0]),)
                if pressed[Actions.right]:
                    return True, PlayerFSM.StateID.Running, (np.array([1,0]),)
                return True, PlayerFSM.StateID.Standing, ()
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge] and pressed[Actions.left]:
                return True, PlayerFSM.StateID.Rolling, (np.array([-1,0]),)
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge] and pressed[Actions.right]:
                return True, PlayerFSM.StateID.Rolling, (np.array([1,0]),)
            return False, None, None

        def enter(self, player):
            print "enter run attack"
            global timerController 
            timerController.startTimer(self.attackTimer)
            player.gSpeed = PlayerConsts.maxRunAttackSpeed

        def exit(self, player):
            #timerController.stopTimer(self.rollTimer)
            player.hitBool = False

    class Jumping(object):
        def __init__(self):
            self.highjump = True;

        def internal(self, player, pressed, previouslyPressed):
            if not pressed[Actions.jump] and self.highjump:
                player.Dgrav = PlayerConsts.Jumping.lowJumpDgrav
                self.highjump = False

        def checkChange(self, player, pressed, previouslyPressed):
            if player.yJumpSpeed >=0:
                return True, PlayerFSM.StateID.Falling, ()
            return False, None, None

        def enter(self, player):
            print "enter jumping"
            player.onGround = False
            player.yJumpSpeed = PlayerConsts.Jumping.initialJumpSpeed - player.gDir[y]*player.gSpeed
            player.Dgrav = PlayerConsts.Jumping.highJumpDgrav
            self.highjump = True

        def exit(self, player):
            player.yJumpSpeed = 0

    class Falling(object):
        def __init__(self):
            pass

        def internal(self, player, pressed, previouslyPressed):
            pass

        def checkChange(self, player, pressed, previouslyPressed):
            if player.pos[y] >= 150:
                return True, PlayerFSM.StateID.Standing, ()
            if player.landed:
                return True, PlayerFSM.StateID.Standing, ()


            return False, None, None

        def enter(self, player):
            print "enter falling"
            player.Dgrav = 0

        def exit(self, player):
            player.pos[y] = 150
            player.onGround = True
            player.landed = False
            player.Dgrav = 1

