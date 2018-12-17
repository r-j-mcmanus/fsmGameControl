
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
                        self.StateID.Jab    :  PlayerFSM.Jab(),
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
        Jab = 4
        RunAttack = 6
        Jumping = 9
        Falling = 10


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
            if player.onGround == False:
                return True, PlayerFSM.StateID.Falling, ()
            if pressed[Actions.left] and pressed[Actions.dodge]:
                return True, PlayerFSM.StateID.Rolling, (np.array([-1,0]),)
            if pressed[Actions.right] and pressed[Actions.dodge]:
                return True, PlayerFSM.StateID.Rolling, (np.array([1,0]),)
            if pressed[Actions.left]:
                return True, PlayerFSM.StateID.Running, (np.array([-1,0]),)
            if pressed[Actions.right]:
                return True, PlayerFSM.StateID.Running, (np.array([1,0]),)
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                return True, PlayerFSM.StateID.Jab, (0,) #We enter jab in substate 0
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                return True, PlayerFSM.StateID.Jumping, ()

            return False, None, None

        def enter(self, player):
            print "enter standing"
            player.gSpeed = 0  
            player.onGround = True

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
            if player.onGround == False:
                return True, PlayerFSM.StateID.Falling, ()
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge]:
                return True, PlayerFSM.StateID.Rolling, ()
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                return True, PlayerFSM.StateID.Jumping, ()
            if not pressed[Actions.left] and not pressed[Actions.right]:
                return True, PlayerFSM.StateID.Standing, ()
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                return True, PlayerFSM.StateID.RunAttack, (0,) #We enter running attack in substate 0

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
                if player.onGround == False:
                    print "not on floor as finishing rolling, new state?"
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
            global timerController 
            timerController.startTimer(self.rollTimer)
            player.gSpeed = PlayerConsts.Roll.maxSpeed
            player.hurtBool = False 

        def exit(self, player):
            player.hurtBool = True 
            #timerController.stopTimer(self.rollTimer)

    class Jab(object):
        def __init__(self):
            global timerController 
            self.attackTimers = (timerController.addTimer(PlayerConsts.Jab.duration[0], "Jab_1_timer"),
                timerController.addTimer(PlayerConsts.Jab.duration[1], "Jab_2_timer"))
            self.followUpAttackBool = False
            self.substateID = 1

        def internal(self, player, pressed, previouslyPressed):
            if self.attackTimers[self.substateID].elapsed == PlayerConsts.Jab.hitBoxStart[self.substateID]:
                player.hitBool = True
            if self.attackTimers[self.substateID].elapsed == PlayerConsts.Jab.hitBoxEnd[self.substateID]:
                player.hitBool = False
            if self.substateID < 1 and pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                self.followUpAttackBool = True

        def checkChange(self, player, pressed, previouslyPressed):
            if player.onGround == False:
                return True, PlayerFSM.StateID.Falling, ()
            if self.attackTimers[self.substateID].elapsed == self.attackTimers[self.substateID].duration:
                if self.followUpAttackBool:
                    return True, PlayerFSM.StateID.Jab, (self.substateID+1,)
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

        def enter(self, player,substateID):
            print "enter jab", substateID
            global timerController 
            self.substateID = substateID
            timerController.startTimer(self.attackTimers[self.substateID])
            player.gSpeed = 0
            self.followUpAttackBool = False

        def exit(self, player):
            #timerController.stopTimer(self.rollTimer)
            player.hitBool = False

    class RunAttack(object):
        def __init__(self):
            global timerController 
            self.attackTimers = (timerController.addTimer(PlayerConsts.RunAttack.duration[0], "RunAttack_1_timer"),
                timerController.addTimer(PlayerConsts.RunAttack.duration[1], "RunAttack_2_timer"),
                timerController.addTimer(PlayerConsts.RunAttack.duration[2], "RunAttack_3_timer"))
            self.followUpAttackBool = False
            self.substateID = 0

        def internal(self, player, pressed, previouslyPressed):
            if self.attackTimers[self.substateID].elapsed == PlayerConsts.RunAttack.hitBoxStart[self.substateID]:
                player.hitBool = True
            if self.attackTimers[self.substateID].elapsed == PlayerConsts.RunAttack.hitBoxEnd[self.substateID]:
                player.hitBool = False
            if self.attackTimers[self.substateID].elapsed == PlayerConsts.RunAttack.runEnd[self.substateID]:
                player.gSpeed = 0
            if self.substateID < 2 and pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                self.followUpAttackBool = True

        def checkChange(self, player, pressed, previouslyPressed):
            if player.onGround == False:
                return True, PlayerFSM.StateID.Falling, ()
            if self.attackTimers[self.substateID].elapsed == self.attackTimers[self.substateID].duration:
                if self.followUpAttackBool == True:
                    return True, PlayerFSM.StateID.RunAttack, (self.substateID+1,)
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

        def enter(self, player,substateID):
            print "enter run attack"
            global timerController 
            assert 0<=substateID<3
            self.substateID = substateID
            timerController.startTimer(self.attackTimers[self.substateID])
            player.gSpeed = PlayerConsts.RunAttack.speed[self.substateID]

        def exit(self, player):
            #timerController.stopTimer(self.rollTimer)
            player.hitBool = False
            self.followUpAttackBool = False

    class Jumping(object):
        def __init__(self):
            self.highjump = True;

        def internal(self, player, pressed, previouslyPressed):
            if not pressed[Actions.jump] and self.highjump:
                player.Dgrav = PlayerConsts.Jumping.lowJumpDgrav
                self.highjump = False

        def checkChange(self, player, pressed, previouslyPressed):
            if player.yJumpSpeed >= 0 or player.startFalling:
                return True, PlayerFSM.StateID.Falling, ()
            return False, None, None

        def enter(self, player, direction=[0,0]):
            print "enter jumping"

            if not np.array_equal(direction,[0,0]):
                player.gDir = direction

            player.onGround = False
            player.startFalling = False
            player.yJumpSpeed = PlayerConsts.Jumping.initialJumpSpeed - player.gDir[y]*player.gSpeed
            player.Dgrav = PlayerConsts.Jumping.highJumpDgrav
            self.highjump = True

        def exit(self, player):
            player.yJumpSpeed = 0

    class Falling(object):
        def __init__(self):
                self.graceEndJumpTimer = timerController.addTimer(PlayerConsts.Falling.endGracePeriod, "endJumpGracePeriod")
                #self.graceEnterJumpTimer = timerController.addTimer(PlayerConsts.Falling.startGracePeriod, "enterJumpGracePeriod")

        def internal(self, player, pressed, previouslyPressed):
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                timerController.startTimer(self.graceEndJumpTimer)
                player.graceJumpBool = True
            if self.graceEndJumpTimer.elapsed == self.graceEndJumpTimer.duration:
                player.graceJumpBool = False


        def checkChange(self, player, pressed, previouslyPressed):
            if player.onGround:
                if player.graceJumpBool:
                    if pressed[Actions.left]:
                        return True, PlayerFSM.StateID.Jumping, (np.array([-1,0]),)
                    if pressed[Actions.right]:
                        return True, PlayerFSM.StateID.Jumping, (np.array([1,0]),)
                else:
                    return True, PlayerFSM.StateID.Standing, ()

            return False, None, None

        def enter(self, player):
            print "enter falling"
            player.Dgrav = 0
            player.startFalling = False
            player.onGround = False

        def exit(self, player):
            player.yJumpSpeed = 0
            player.Dgrav = -1
            player.graceJumpBool = False

