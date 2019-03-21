
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


class AIFSM(object):
    """
    Will control the state of the player object, making minimal 
    changes to Player member variables e.g. state, direction, 
    speed and various bools
    """

    def __init__(self,timerController):

        self.currentStateID = StateID.Standing

        self.states = {
                        StateID.Standing :  StateFactory.Standing(),
                        StateID.Falling  :  StateFactory.Falling(timerController),
                    }

        self.stateTransitions = {
                        StateID.Standing :  [],
                        StateID.Falling  :  [],

                    }

        self.transFns = self.TransFns()
        self.populateStateTransitions()

    def __call__(self, entities):
        for e in entities:
            for transition in self.stateTransitions[e.stateID]:
                if transition.check(e):
                    self.states[e.stateID].exit(e)
                    e.stateID = transition.endID
                    self.states[e.stateID].enter(e)
                    continue

    class Transition(object):
        def __init__(self, endID, transitionFns):
            self.endID = endID
            self.transitionFns = transitionFns

        def check(self,entity):
            transBool = True
            for transFn in self.transitionFns:
                transBool *= transFn(entity)
            if transBool:
                return transBool


    def addTransition(self, startStateID, endStateID, *transitionFn):
        assert startStateID in self.states.keys(), "startStateID %s not in dict of states" % startStateID
        assert endStateID in self.states.keys(), "endStateID %s not in dict of states" % endStateID
        self.stateTransitions[startStateID].append(self.Transition(endStateID,transitionFn))

    def populateStateTransitions(self):
        """Note that the order we add transitions is the order they are checked, and first one true is the result"""
        self.addTransition(StateID.Standing, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(StateID.Falling, StateID.Standing, self.transFns.checkOnGround(True))

    class TransFns:
        def __init__(self):
            self.checkOnGround = lambda eval = True : lambda entity : entity.onGround == eval
            self.checkFalling =  lambda eval = True : lambda entity : (entity.yJumpSpeed >= 0 or entity.startFalling) == eval


class StateFactory(object):
    

    class Standing(object):
        def __init__(self):
            pass

        def internal(self, entity):
            pass


        def enter(self, entity):
            print "enter ai standing"
            entity.gSpeed = 0  
            entity.changeDirection = 1
            entity.applyChangeDir()

        def exit(self, entity):
            pass

    class Falling(object):
        def __init__(self, timerController):
            pass

        def internal(self, entity):
            pass

        def enter(self, entity):
            print "enter ai falling"
            entity.Dgrav = 0
            entity.startFalling = False
            entity.onGround = False

        def exit(self, entity):
            entity.yJumpSpeed = 0
            entity.Dgrav = -1
            entity.graceJumpBool = False