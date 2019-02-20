
#PlayerConsts

from PlayerConsts import PlayerConsts
import numpy as np
from InputHandler import Actions

from TimerController import TimerIDs

from HelperFns import clamp

x = 0
y = 1


class direction:
    right = 1
    left = -1
    noChange = 0
    none = 0

class IDMaker():
    def __init__(self):
        self.num = 0
    def __call__(self):
        self.num+=1
        return self.num

idMaker = IDMaker()

class StateID:
    Standing = idMaker()
    Running = idMaker()
    Rolling = idMaker()
    Jab1 = idMaker()
    Jab2 = idMaker()
    Jab3 = idMaker()
    RunAttack1 = idMaker()
    RunAttack2 = idMaker()
    Jumping = idMaker()
    Falling = idMaker()


class PlayerFSM(object):
    """
    Will control the state of the player object, making minimal 
    changes to Player member variables e.g. state, direction, 
    speed and various bools
    """

    def __init__(self, timerController, player, pressed, previouslyPressed):

        self.currentStateID = StateID.Standing

        self.states = {
                        StateID.Standing :  StateFactory.Standing(),
                        StateID.Jab1     :  StateFactory.Jab1(timerController),
                        StateID.Jab2     :  StateFactory.Jab2(timerController),
                        StateID.Jab3     :  StateFactory.Jab3(timerController),
                        StateID.Rolling  :  StateFactory.Rolling(timerController),
                        StateID.Running  :  StateFactory.Running(),
                        StateID.RunAttack1: StateFactory.RunAttack1(timerController),
                        StateID.RunAttack2: StateFactory.RunAttack2(timerController),
                        StateID.Jumping  :  StateFactory.Jumping(timerController),
                        StateID.Falling  :  StateFactory.Falling(timerController),
                    }

        self.stateTransitions = {
                        StateID.Standing :  [],
                        StateID.Jab1     :  [],
                        StateID.Jab2     :  [],
                        StateID.Jab3     :  [],
                        StateID.Rolling  :  [],
                        StateID.Running  :  [],
                        StateID.RunAttack1: [],
                        StateID.RunAttack2: [],
                        StateID.Jumping  :  [],
                        StateID.Falling  :  [],

                    }

        self.transFns = self.TransFns(player, pressed, previouslyPressed)
        self.populateStateTransitions()

    def __call__(self, player, pressed, previouslyPressed):
        self.messages = []
        self.states[player.stateID].internal(player, pressed, previouslyPressed)
        
        for transition in self.stateTransitions[player.stateID]:
            if transition.check():
                self.states[player.stateID].exit(player)
                player.stateID = transition.endID
                self.states[player.stateID].enter(player)
                return

    class Transition(object):
        def __init__(self, endID, transitionFns):
            self.endID = endID
            self.transitionFns = transitionFns

        def check(self):
            transBool = True
            for transFn in self.transitionFns:
                transBool *= transFn()
            if transBool:
                return transBool


    def addTransition(self, startStateID, endStateID, *transitionFn):
        assert startStateID in self.states.keys(), "startStateID %s not in dict of states" % startStateID
        assert endStateID in self.states.keys(), "endStateID %s not in dict of states" % endStateID
        self.stateTransitions[startStateID].append(self.Transition(endStateID,transitionFn))

    def populateStateTransitions(self):
        """Note that the order we add transitions is the order they are checked, and first one true is the result"""
        self.addTransition(StateID.Standing, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(StateID.Standing, StateID.Rolling, self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(StateID.Standing, StateID.Running, self.transFns.checkActionPressed(Actions.right))
        self.addTransition(StateID.Standing, StateID.Running, self.transFns.checkActionPressed(Actions.left))
        self.addTransition(StateID.Standing, StateID.Jab1, self.transFns.checkAction(Actions.attack))
        self.addTransition(StateID.Standing, StateID.Jumping, self.transFns.checkActionPressed(Actions.jump))

        self.addTransition(StateID.Running, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(StateID.Running, StateID.Rolling, self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(StateID.Running, StateID.RunAttack1, self.transFns.checkAction(Actions.attack))
        self.addTransition(StateID.Running, StateID.Jumping, self.transFns.checkActionPressed(Actions.jump))
        self.addTransition(StateID.Running, StateID.Standing, self.transFns.checkAction(Actions.right, False), self.transFns.checkAction(Actions.left, False))

        self.addTransition(StateID.Rolling, StateID.Falling, self.transFns.checkDodging(False), self.transFns.checkOnGround(False))
        self.addTransition(StateID.Rolling, StateID.Running, self.transFns.checkDodging(False), self.transFns.checkAction(Actions.right))
        self.addTransition(StateID.Rolling, StateID.Running, self.transFns.checkDodging(False), self.transFns.checkAction(Actions.left))
        self.addTransition(StateID.Rolling, StateID.Standing, self.transFns.checkDodging(False))

        self.addTransition(StateID.Jab1, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(StateID.Jab1, StateID.Jab2, self.transFns.checkAttackEnd(), self.transFns.checkFollowupAttack())
        self.addTransition(StateID.Jab1, StateID.Rolling, self.transFns.checkAttackEnd(), self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(StateID.Jab1, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.right), self.transFns.checkAction(Actions.left))
        self.addTransition(StateID.Jab1, StateID.Standing, self.transFns.checkAttackEnd())

        self.addTransition(StateID.Jab2, StateID.Falling, self.transFns.checkAttackEnd(), self.transFns.checkOnGround(False))
        self.addTransition(StateID.Jab2, StateID.Jab3, self.transFns.checkAttackEnd(), self.transFns.checkFollowupAttack())
        self.addTransition(StateID.Jab2, StateID.Rolling, self.transFns.checkAttackEnd(), self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(StateID.Jab2, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.right))
        self.addTransition(StateID.Jab2, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.left))
        self.addTransition(StateID.Jab2, StateID.Standing, self.transFns.checkAttackEnd())

        self.addTransition(StateID.Jab3, StateID.Falling, self.transFns.checkAttackEnd(), self.transFns.checkOnGround(False))
        self.addTransition(StateID.Jab3, StateID.Rolling, self.transFns.checkAttackEnd(), self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(StateID.Jab3, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.right))
        self.addTransition(StateID.Jab3, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.left))
        self.addTransition(StateID.Jab3, StateID.Standing, self.transFns.checkAttackEnd())

        self.addTransition(StateID.RunAttack1, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(StateID.RunAttack1, StateID.RunAttack2, self.transFns.checkAttackEnd(),  self.transFns.checkFollowupAttack())
        self.addTransition(StateID.RunAttack1, StateID.Rolling, self.transFns.checkAttackEnd(), self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(StateID.RunAttack1, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.right))
        self.addTransition(StateID.RunAttack1, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.left))
        self.addTransition(StateID.RunAttack1, StateID.Standing, self.transFns.checkAttackEnd())

        self.addTransition(StateID.RunAttack2, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(StateID.RunAttack2, StateID.Rolling, self.transFns.checkAttackEnd(), self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(StateID.RunAttack2, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.right))
        self.addTransition(StateID.RunAttack2, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.left))
        self.addTransition(StateID.RunAttack2, StateID.Standing, self.transFns.checkAttackEnd())

        self.addTransition(StateID.Jumping, StateID.Falling,self.transFns.checkFalling())

        self.addTransition(StateID.Falling, StateID.Jumping, self.transFns.checkGraceJump(), self.transFns.checkOnGround())
        self.addTransition(StateID.Falling, StateID.Running, self.transFns.checkOnGround(), self.transFns.checkAction(Actions.right))
        self.addTransition(StateID.Falling, StateID.Running, self.transFns.checkOnGround(), self.transFns.checkAction(Actions.left))
        self.addTransition(StateID.Falling, StateID.Standing, self.transFns.checkOnGround())


    class TransFns:
        def __init__(self, player, pressed, previouslyPressed):
            self.checkOnGround = lambda eval = True : lambda : player.onGround == eval
            self.checkGraceJump = lambda eval = True : lambda :player.graceJumpBool == eval
            self.checkFollowupAttack = lambda eval = True : lambda : player.followUpAttackBool == eval
            self.checkAttackEnd = lambda eval = True : lambda : player.attackEndBool == eval
            self.checkDodging = lambda eval = True : lambda : player.dodgingBool == eval
            self.checkAction = lambda action, eval = True : lambda : pressed[action] == eval
            self.checkActionPressed = lambda action, eval = True : lambda : (pressed[action] and not previouslyPressed[action]) == eval
            self.checkActionHeld = lambda  action, eval = True: lambda : (pressed[action] and previouslyPressed[action]) == eval
            self.checkFalling =  lambda eval = True: lambda : (player.yJumpSpeed >= 0 or player.startFalling) == eval


def updateChangeDirection(player, pressed, previouslyPressed):
    if pressed[Actions.left] and not previouslyPressed[Actions.left] and player.dir != direction.left:
        player.changeDirection *= -1
    if not pressed[Actions.left] and previouslyPressed[Actions.left] and player.dir != direction.left:
        player.changeDirection *= -1
    if pressed[Actions.right] and not previouslyPressed[Actions.right] and player.dir != direction.right:
        player.changeDirection *= -1
    if not pressed[Actions.right] and previouslyPressed[Actions.right] and player.dir != direction.right:
        player.changeDirection *= -1

def updateDirection(player, pressed, previouslyPressed):
    if pressed[Actions.left] and not previouslyPressed[Actions.left]:
        player.dir = direction.left
    if not pressed[Actions.left] and previouslyPressed[Actions.left] and pressed[Actions.right]:
        player.dir = direction.right
    if pressed[Actions.right] and not previouslyPressed[Actions.right]:
        player.dir = direction.right
    if not pressed[Actions.right] and previouslyPressed[Actions.right] and pressed[Actions.left]:
        player.dir = direction.left


class StateFactory(object):
    

    class Standing(object):
        def __init__(self):
            pass

        def internal(self, player, pressed, previouslyPressed):
            updateDirection(player, pressed, previouslyPressed)


        def enter(self, player):
            print "enter standing"
            player.gSpeed = 0  
            player.changeDirection = 1
            player.applyChangeDir()

        def exit(self, player):
            pass    

    class Running(object):
        def __init__(self):
            pass

        def internal(self, player, pressed, previouslyPressed):
            updateDirection(player, pressed, previouslyPressed)

        def enter(self, player):
            print "enter running"
            player.gSpeed = PlayerConsts.maxRunSpeed
            player.applyChangeDir()

        def exit(self, player):
            pass

    class Rolling(object):
        def __init__(self, timerController):
            self.rollTimer = timerController[TimerIDs.rollTimer]

        def internal(self, player, pressed, previouslyPressed):
            if self.rollTimer.ended():
                player.dodgingBool = False

            updateChangeDirection(player, pressed, previouslyPressed)

        def enter(self, player):
            print "enter rolling"
            self.rollTimer.start()
            player.gSpeed = PlayerConsts.Roll.maxSpeed
            player.hurtBool = False 
            player.dodgingBool = True
            player.changeDirection = 1

        def exit(self, player):
            player.hurtBool = True
            player.gSpeed = 0                        


    class Jab1(object):
        def __init__(self, timerController):
            self.attackTimer = timerController[TimerIDs.jab1]

        def internal(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == PlayerConsts.Jab1.hitBoxStart:
                player.hitBool = True
            if self.attackTimer.elapsed == PlayerConsts.Jab1.hitBoxEnd:
                player.hitBool = False
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                player.followUpAttackBool = True
            if self.attackTimer.ended():
                player.attackEndBool = True

            updateChangeDirection(player, pressed, previouslyPressed)


        def enter(self, player):
            print "enter jab 1"
            self.attackTimer.start()
            player.gSpeed = 0
            player.followUpAttackBool = False
            player.attackEndBool = False
            player.changeDirection = 1

        def exit(self, player):
            player.hitBool = False
            player.followUpAttackBool = False

    class Jab2(object):
        def __init__(self, timerController):
            self.attackTimer = timerController[TimerIDs.jab2]

        def internal(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == PlayerConsts.Jab2.hitBoxStart:
                player.hitBool = True
            if self.attackTimer.elapsed == PlayerConsts.Jab2.hitBoxEnd:
                player.hitBool = False
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                player.followUpAttackBool = True
            if self.attackTimer.ended():
                player.attackEndBool = True

            updateChangeDirection(player, pressed, previouslyPressed)


        def enter(self, player):
            print "enter jab 2"
            self.attackTimer.start()
            player.gSpeed = 0
            player.followUpAttackBool = False
            player.attackEndBool = False

        def exit(self, player):
            player.hitBool = False
            player.followUpAttackBool = False

    class Jab3(object):
        def __init__(self, timerController):
            self.attackTimer = timerController[TimerIDs.jab3]

        def internal(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == PlayerConsts.Jab3.hitBoxStart:
                player.hitBool = True
            if self.attackTimer.elapsed == PlayerConsts.Jab3.hitBoxEnd:
                player.hitBool = False
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                player.followUpAttackBool = True
            if self.attackTimer.ended():
                player.attackEndBool = True

            updateChangeDirection(player, pressed, previouslyPressed)


        def enter(self, player):
            print "enter jab 3"
            self.attackTimer.start()
            player.gSpeed = 0
            player.followUpAttackBool = False
            player.attackEndBool = False

        def exit(self, player):
            player.hitBool = False
            player.followUpAttackBool = False


    class RunAttack1(object):
        def __init__(self, timerController):
            self.attackTimer = timerController[TimerIDs.runAttack1]

        def internal(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == PlayerConsts.RunAttack1.hitBoxStart:
                player.hitBool = True
            if self.attackTimer.elapsed == PlayerConsts.RunAttack1.hitBoxEnd:
                player.hitBool = False
            if self.attackTimer.elapsed == PlayerConsts.RunAttack1.runEnd:
                player.gSpeed = 0
            if pressed[Actions.attack] and not previouslyPressed[Actions.attack]:
                player.followUpAttackBool = True
            if self.attackTimer.ended():
                player.attackEndBool = True

            updateChangeDirection(player, pressed, previouslyPressed)


        def enter(self, player):
            print "enter runAttack 1"
            self.attackTimer.start()
            player.followUpAttackBool = False
            player.attackEndBool = False
            player.gSpeed = PlayerConsts.RunAttack1.speed
            player.changeDirection = 1

        def exit(self, player):
            player.hitBool = False
            player.followUpAttackBool = False
            player.attackEndBool = False

    class RunAttack2(object):
        def __init__(self, timerController):
            self.attackTimer = timerController[TimerIDs.runAttack2]

        def internal(self, player, pressed, previouslyPressed):
            if self.attackTimer.elapsed == PlayerConsts.RunAttack2.hitBoxStart:
                player.hitBool = True
            if self.attackTimer.elapsed == PlayerConsts.RunAttack2.hitBoxEnd:
                player.hitBool = False
            if self.attackTimer.elapsed == PlayerConsts.RunAttack2.runEnd:
                player.gSpeed = 0
            if self.attackTimer.ended():
                player.attackEndBool = True

            updateChangeDirection(player, pressed, previouslyPressed)


        def enter(self, player):
            print "enter runAttack 2"
            self.attackTimer.start()
            player.followUpAttackBool = False
            player.attackEndBool = False
            player.gSpeed = PlayerConsts.RunAttack2.speed

        def exit(self, player):
            player.hitBool = False
            player.followUpAttack = False
            player.followUpAttackBool = False

    class Jumping(object):
        """ need to fix moving when jumping from still chanign landing direction """
        def __init__(self, timerController):   
            self.graceJumpTimer = timerController[TimerIDs.graceJump]


        def internal(self, player, pressed, previouslyPressed):
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                self.graceJumpTimer.start()
                player.graceJumpBool = True
            if not pressed[Actions.jump] and player.highJumpBool:
                player.Dgrav = PlayerConsts.Jumping.lowJumpDgrav
                player.highJumpBool = False

            if pressed[Actions.left] and not pressed[Actions.right]:
                player.gSpeed = clamp(PlayerConsts.Air.minSpeed, PlayerConsts.Air.maxSpeed, player.gSpeed + direction.left*player.dir*PlayerConsts.Air.xImpulseMagnitude)
            if pressed[Actions.right] and not pressed[Actions.left]:
                player.gSpeed = clamp(PlayerConsts.Air.minSpeed, PlayerConsts.Air.maxSpeed, player.gSpeed + direction.right*player.dir*PlayerConsts.Air.xImpulseMagnitude)

            updateChangeDirection(player, pressed, previouslyPressed)

        def enter(self, player):
            print "enter jumping"
            player.onGround = False
            player.startFalling = False
            player.yJumpSpeed = PlayerConsts.Jumping.initialJumpSpeed - player.gDir[y]*player.gSpeed
            player.Dgrav = PlayerConsts.Jumping.highJumpDgrav
            player.highJumpBool = True
            player.graceJumpBool = False
            player.applyChangeDir()

        def exit(self, player):
            player.yJumpSpeed = 0
            player.highJumpBool = True

    class Falling(object):
        def __init__(self, timerController):
            self.graceJumpTimer = timerController[TimerIDs.graceJump]

        def internal(self, player, pressed, previouslyPressed):
            if pressed[Actions.jump] and not previouslyPressed[Actions.jump]:
                self.graceJumpTimer.start()
                player.graceJumpBool = True
            if self.graceJumpTimer.ended():
                player.graceJumpBool = False

            if pressed[Actions.left] and not pressed[Actions.right]:
                #print "falling left", PlayerConsts.Air.minSpeed, PlayerConsts.Air.maxSpeed, player.gSpeed + direction.left*player.dir*PlayerConsts.Air.xImpulseMagnitude
                player.gSpeed = clamp(PlayerConsts.Air.minSpeed,PlayerConsts.Air.maxSpeed, player.gSpeed + direction.left*player.dir*PlayerConsts.Air.xImpulseMagnitude)
            else:
                if pressed[Actions.right] and not pressed[Actions.left]:
                    player.gSpeed = clamp(PlayerConsts.Air.minSpeed,PlayerConsts.Air.maxSpeed, player.gSpeed + direction.right*player.dir*PlayerConsts.Air.xImpulseMagnitude)

            updateChangeDirection(player, pressed, previouslyPressed)

        def enter(self, player):
            print "enter falling"
            player.Dgrav = 0
            player.startFalling = False
            player.onGround = False

        def exit(self, player):
            player.yJumpSpeed = 0
            player.Dgrav = -1
            player.graceJumpBool = False
            self.graceJumpTimer.end()
