
#PlayerConsts

from PlayerConsts import PlayerConsts
import numpy as np
from InputHandler import Actions

from TimerController import TimerIDs

from HelperFns import clamp

x = 0
y = 1

global timerController

class direction:
    right = 1
    left = -1
    noChange = 0
    none = 0

class ChangeResult:
    def __init__(self, result=False, stateID=None, *stateArgs):
        self.result = result
        self.stateID = stateID
        self.stateArgs = stateArgs

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
                        self.StateID.Jab      :  PlayerFSM.Jab(),
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
            changeResult = state.checkChange(player, pressed, previouslyPressed)
        except ValueError:
                print "ERROR!!"
                print message
                print "changing from StateID ", player.stateID
                print "not enough values returned in state.checkChange"
                raise SystemExit

        if changeResult.result:
            state.exit(player)
            player.stateID = changeResult.stateID
            try:
                self.states[player.stateID].enter(player, *changeResult.stateArgs)
            except TypeError, message:
                print "ERROR!!"
                print message
                print "changing to StateID ", player.stateID
                print "Given chageArgs ", changeResult.stateArgs
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
                return ChangeResult(True, PlayerFSM.StateID.Falling)
            if pressed[Actions.left] and pressed[Actions.dodge]:
                return ChangeResult(True, PlayerFSM.StateID.Rolling, direction.left)
            if pressed[Actions.right] and pressed[Actions.dodge]:
                return ChangeResult(True, PlayerFSM.StateID.Rolling, direction.right)
            if pressed[Actions.left]:
                return ChangeResult(True, PlayerFSM.StateID.Running, direction.left)
            if pressed[Actions.right]:
                return ChangeResult(True, PlayerFSM.StateID.Running, direction.right)
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                return ChangeResult(True, PlayerFSM.StateID.Jab, 0)#We enter jab in substate 0
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                return ChangeResult(True, PlayerFSM.StateID.Jumping, direction.noChange)

            return ChangeResult(False, None)

        def enter(self, player):
            print "enter standing"
            player.gSpeed = 0  

        def exit(self, player):
            pass    

    class Running(object):
        def __init__(self):
            pass

        def internal(self, player, pressed, previouslyPressed):
            #for chanign direction when running
            if pressed[Actions.left] and pressed[Actions.right] and not previouslyPressed[Actions.right]:
                player.dir = direction.right
            if pressed[Actions.left] and pressed[Actions.right] and not previouslyPressed[Actions.left]:
                player.dir = direction.left
            if pressed[Actions.left] and not pressed[Actions.right] and previouslyPressed[Actions.right]:
                player.dir = direction.left  
            if not pressed[Actions.left] and pressed[Actions.right] and previouslyPressed[Actions.left]:
                player.dir = direction.right  
                

        def checkChange(self, player, pressed, previouslyPressed):
            # ensuring falling takes priorety
            if player.onGround == False:
                return ChangeResult(True, PlayerFSM.StateID.Falling)

            # player input actions
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge]:
                return ChangeResult(True, PlayerFSM.StateID.Rolling, direction.noChange)
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                return ChangeResult(True, PlayerFSM.StateID.Jumping, direction.noChange)#we do not need to change the direction as internal handels it
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                return ChangeResult(True, PlayerFSM.StateID.RunAttack, 0) #We enter running attack in substate 0


            # ensuring stoping is the least prefered 
            if not pressed[Actions.left] and not pressed[Actions.right]:
                return ChangeResult(True, PlayerFSM.StateID.Standing)

            return ChangeResult(False, None)

        def enter(self, player, direction):
            print "enter running"
            player.gSpeed = PlayerConsts.maxRunSpeed
            player.dir = direction

        def exit(self, player):
            pass

    class Rolling(object):
        def __init__(self):
            pass

        def internal(self, player, pressed, previouslyPressed):
            pass

        def checkChange(self, player, pressed, previouslyPressed):
            if timerController[TimerIDs.rollTimer].ended():
                if player.onGround == False:
                    return ChangeResult(True, PlayerFSM.StateID.Falling)
                if pressed[Actions.left]:
                    return ChangeResult(True, PlayerFSM.StateID.Running, direction.left)
                if pressed[Actions.right]:
                    return ChangeResult(True, PlayerFSM.StateID.Running, direction.right)
                return ChangeResult(True, PlayerFSM.StateID.Standing)
            return ChangeResult(False, None)

        def enter(self, player, direction):
            print "enter rolling"
            player.dir = direction
            global timerController
            timerController.startTimer(TimerIDs.rollTimer)
            player.gSpeed = PlayerConsts.Roll.maxSpeed
            player.hurtBool = False 

        def exit(self, player):
            player.hurtBool = True
            player.gSpeed = PlayerConsts.maxRunSpeed

    class Jab(object):
        def __init__(self): 
            self.followUpAttackBool = False
            self.substateID = 1
            self.substateIDtoTimerID = {0: TimerIDs.jab1, 1: TimerIDs.jab2}

        def internal(self, player, pressed, previouslyPressed):
            if timerController[self.substateIDtoTimerID[self.substateID]].elapsed == PlayerConsts.Jab.hitBoxStart[self.substateID]:
                player.hitBool = True
            if timerController[self.substateIDtoTimerID[self.substateID]].elapsed == PlayerConsts.Jab.hitBoxEnd[self.substateID]:
                player.hitBool = False
            if self.substateID < 1 and pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                self.followUpAttackBool = True

        def checkChange(self, player, pressed, previouslyPressed):
            if player.onGround == False:
                return ChangeResult(True, PlayerFSM.StateID.Falling)
            if timerController[self.substateIDtoTimerID[self.substateID]].ended():
                if self.followUpAttackBool:
                    return ChangeResult(True, PlayerFSM.StateID.Jab, self.substateID+1)
                if pressed[Actions.left]:
                    return ChangeResult(True, PlayerFSM.StateID.Running, direction.left)
                if pressed[Actions.right]:
                    return ChangeResult(True, PlayerFSM.StateID.Running, direction.right)
                return ChangeResult(True, PlayerFSM.StateID.Standing)
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge] and pressed[Actions.left]:
                return ChangeResult(True, PlayerFSM.StateID.Rolling, direction.left)
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge] and pressed[Actions.right]:
                return ChangeResult(True, PlayerFSM.StateID.Rolling, direction.right)
            return ChangeResult(False, None)

        def enter(self, player,substateID):
            print "enter jab", substateID
            global timerController 
            self.substateID = substateID
            try:
                timerController.startTimer(self.substateIDtoTimerID[self.substateID])
            except KeyError:
                print "self.substateID not in self.substateIDtoTimerID"
                raise SystemExit, message
            player.gSpeed = 0
            self.followUpAttackBool = False

        def exit(self, player):
            #timerController.stopTimer(self.rollTimer)
            player.hitBool = False

    class RunAttack(object):
        def __init__(self):
            self.followUpAttackBool = False
            self.substateID = 0
            self.substateIDtoTimerID = {0: TimerIDs.runAttack1, 
                                        1: TimerIDs.runAttack2, 
                                        2: TimerIDs.runAttack3}

        def internal(self, player, pressed, previouslyPressed):
            if timerController[self.substateIDtoTimerID[self.substateID]].elapsed == PlayerConsts.RunAttack.hitBoxStart[self.substateID]:
                player.hitBool = True
            if timerController[self.substateIDtoTimerID[self.substateID]].elapsed == PlayerConsts.RunAttack.hitBoxEnd[self.substateID]:
                player.hitBool = False
            if timerController[self.substateIDtoTimerID[self.substateID]].elapsed == PlayerConsts.RunAttack.runEnd[self.substateID]:
                player.gSpeed = 0
            if self.substateID < 2 and pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                self.followUpAttackBool = True

        def checkChange(self, player, pressed, previouslyPressed):
            if player.onGround == False:
                return ChangeResult(True, PlayerFSM.StateID.Falling)
            if timerController[self.substateIDtoTimerID[self.substateID]].ended():
                if self.followUpAttackBool == True:
                    return ChangeResult(True, PlayerFSM.StateID.RunAttack, self.substateID+1)
                if pressed[Actions.left]:
                    return ChangeResult(True, PlayerFSM.StateID.Running, direction.left)
                if pressed[Actions.right]:
                    return ChangeResult(True, PlayerFSM.StateID.Running, direction.right)
                return ChangeResult(True, PlayerFSM.StateID.Standing)
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge] and pressed[Actions.left]:
                return ChangeResult(True, PlayerFSM.StateID.Rolling, direction.left)
            if pressed[Actions.dodge] and not previouslyPressed[Actions.dodge] and pressed[Actions.right]:
                return ChangeResult(True, PlayerFSM.StateID.Rolling, direction.right)
            return ChangeResult(False, None)

        def enter(self, player,substateID):
            print "enter run attack"
            global timerController
            self.substateID = substateID
            try:
                timerController.startTimer(self.substateIDtoTimerID[self.substateID])
            except KeyError:
                print "self.substateID not in self.substateIDtoTimerID"
                raise SystemExit, message
            player.gSpeed = PlayerConsts.RunAttack.speed[self.substateID]

        def exit(self, player):
            #timerController.stopTimer(self.rollTimer)
            player.hitBool = False
            self.followUpAttackBool = False

    class Jumping(object):
        def __init__(self):
            self.highjump = True;

        def internal(self, player, pressed, previouslyPressed):
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                timerController.startTimer(TimerIDs.graceJump)
                player.graceJumpBool = True
            if not pressed[Actions.jump] and self.highjump:
                player.Dgrav = PlayerConsts.Jumping.lowJumpDgrav
                self.highjump = False

            if pressed[Actions.left] and not pressed[Actions.right]:
                print "jumping left", PlayerConsts.Air.minSpeed, PlayerConsts.Air.maxSpeed, player.gSpeed + direction.left*player.dir*PlayerConsts.Air.xImpulseMagnitude
                player.gSpeed = clamp(PlayerConsts.Air.minSpeed,PlayerConsts.Air.maxSpeed, player.gSpeed + direction.left*player.dir*PlayerConsts.Air.xImpulseMagnitude)
            else:
                if pressed[Actions.right] and not pressed[Actions.left]:
                    player.gSpeed = clamp(PlayerConsts.Air.minSpeed,PlayerConsts.Air.maxSpeed, player.gSpeed + direction.right*player.dir*PlayerConsts.Air.xImpulseMagnitude)

        def checkChange(self, player, pressed, previouslyPressed):
            if player.yJumpSpeed >= 0 or player.startFalling:
                return ChangeResult(True, PlayerFSM.StateID.Falling)
            return ChangeResult(False, None)

        def enter(self, player, direction = direction.noChange):
            print "enter jumping"
            player.dir = direction
            player.onGround = False
            player.startFalling = False
            player.yJumpSpeed = PlayerConsts.Jumping.initialJumpSpeed - player.gDir[y]*player.gSpeed
            player.Dgrav = PlayerConsts.Jumping.highJumpDgrav
            self.highjump = True

        def exit(self, player):
            player.yJumpSpeed = 0

    class Falling(object):
        def __init__(self):
            pass

        def internal(self, player, pressed, previouslyPressed):
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                timerController.startTimer(TimerIDs.graceJump)
                player.graceJumpBool = True
            if timerController[TimerIDs.graceJump].ended():
                player.graceJumpBool = False


            if pressed[Actions.left] and not pressed[Actions.right]:
                print "falling left", PlayerConsts.Air.minSpeed, PlayerConsts.Air.maxSpeed, player.gSpeed + direction.left*player.dir*PlayerConsts.Air.xImpulseMagnitude
                player.gSpeed = clamp(PlayerConsts.Air.minSpeed,PlayerConsts.Air.maxSpeed, player.gSpeed + direction.left*player.dir*PlayerConsts.Air.xImpulseMagnitude)
            else:
                if pressed[Actions.right] and not pressed[Actions.left]:
                    player.gSpeed = clamp(PlayerConsts.Air.minSpeed,PlayerConsts.Air.maxSpeed, player.gSpeed + direction.right*player.dir*PlayerConsts.Air.xImpulseMagnitude)

        def checkChange(self, player, pressed, previouslyPressed):
            if player.onGround:
                if player.graceJumpBool:
                    if pressed[Actions.left]:
                        return ChangeResult(True, PlayerFSM.StateID.Jumping, direction.left)
                    if pressed[Actions.right]:
                        return ChangeResult(True, PlayerFSM.StateID.Jumping, direction.right)
                    return ChangeResult(True, PlayerFSM.StateID.Jumping, direction.noChange)
                else:
                    return ChangeResult(True, PlayerFSM.StateID.Standing)

            return ChangeResult(False, None)

        def enter(self, player):
            print "enter falling"
            player.Dgrav = 0
            player.startFalling = False
            player.onGround = False

        def exit(self, player):
            player.yJumpSpeed = 0
            player.Dgrav = -1
            player.graceJumpBool = False
            player.onGround = True
            timerController.endTimer(TimerIDs.graceJump)

