

import numpy as np

import StateID

from InputHandler import Actions
from StateFactory import StateFactory


class FSMs(object):
    """
    Will control the state of the player object, making minimal 
    changes to Player member variables e.g. state, direction, 
    speed and various bools
    """

    def __init__(self, timerController, pressed, previouslyPressed):

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

        self.playerStateTransitions = {
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

        self.yBoxStateTransitions = {
                StateID.Standing :  [],
                StateID.Falling  :  [],
            }

        self.FSMMap = { 
                "player" : self.playerStateTransitions,
                "yBox" : self.yBoxStateTransitions
            }


        self.transitionsPopulateMap = { 
                "player" : self.populatePlayerStateTransitions,
                "yBox" : self.populateYBoxStateTransitions
            }

        self.__currentTransID = None

        self.transFns = self.TransFns(pressed, previouslyPressed)
        self.populateStateTransitions()


    def changeState(self, entity, newID):
        self.states[entity.stateID].exit(entity)
        entity.stateID = newID
        self.states[entity.stateID].enter(entity)

    def __call__(self, entities, pressed, previouslyPressed):
        for entity in entities:
            #run internal state logic
            self.states[entity.stateID].internal(entity, pressed, previouslyPressed)
            for transition in self.FSMMap[entity.entityType][entity.stateID]:
                if transition.check(entity):
                    self.changeState(entity, transition.endID)
                    break

    class Transition(object):
        def __init__(self, endID, transitionFns):
            self.endID = endID
            self.transitionFns = transitionFns

        def check(self, e):
            transBool = True
            for transFn in self.transitionFns:
                transBool *= transFn(e)
            if transBool:
                return transBool


    def addTransition(self, FSMID, startStateID, endStateID, *transitionFn):
        assert startStateID in self.states.keys(), "startStateID %s not in dict of states" % startStateID
        assert endStateID in self.states.keys(), "endStateID %s not in dict of states" % endStateID
        self.FSMMap[FSMID][startStateID].append(self.Transition(endStateID,transitionFn))

    def populateStateTransitions(self):
        for FSM_ID in self.FSMMap.keys():
            self.transitionsPopulateMap[FSM_ID]()

    def populateYBoxStateTransitions(self):
        FSMID = "yBox"

        self.addTransition(FSMID, StateID.Standing, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(FSMID, StateID.Falling, StateID.Standing, self.transFns.checkOnGround())


    def populatePlayerStateTransitions(self):
        """Note that the order we add transitions is the order they are checked, and first one true is the result"""
        FSMID = "player"

        self.addTransition(FSMID, StateID.Standing, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(FSMID, StateID.Standing, StateID.Rolling, self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(FSMID, StateID.Standing, StateID.Running, self.transFns.checkActionPressed(Actions.right))
        self.addTransition(FSMID, StateID.Standing, StateID.Running, self.transFns.checkActionPressed(Actions.left))
        self.addTransition(FSMID, StateID.Standing, StateID.Jab1, self.transFns.checkAction(Actions.attack))
        self.addTransition(FSMID, StateID.Standing, StateID.Jumping, self.transFns.checkActionPressed(Actions.jump))

        self.addTransition(FSMID, StateID.Running, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(FSMID, StateID.Running, StateID.Rolling, self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(FSMID, StateID.Running, StateID.RunAttack1, self.transFns.checkAction(Actions.attack))
        self.addTransition(FSMID, StateID.Running, StateID.Jumping, self.transFns.checkActionPressed(Actions.jump))
        self.addTransition(FSMID, StateID.Running, StateID.Standing, self.transFns.checkAction(Actions.right, False), self.transFns.checkAction(Actions.left, False))

        self.addTransition(FSMID, StateID.Rolling, StateID.Falling, self.transFns.checkDodging(False), self.transFns.checkOnGround(False))
        self.addTransition(FSMID, StateID.Rolling, StateID.Running, self.transFns.checkDodging(False), self.transFns.checkAction(Actions.right))
        self.addTransition(FSMID, StateID.Rolling, StateID.Running, self.transFns.checkDodging(False), self.transFns.checkAction(Actions.left))
        self.addTransition(FSMID, StateID.Rolling, StateID.Standing, self.transFns.checkDodging(False))

        self.addTransition(FSMID, StateID.Jab1, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(FSMID, StateID.Jab1, StateID.Jab2, self.transFns.checkAttackEnd(), self.transFns.checkFollowupAttack())
        self.addTransition(FSMID, StateID.Jab1, StateID.Rolling, self.transFns.checkAttackEnd(), self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(FSMID, StateID.Jab1, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.right), self.transFns.checkAction(Actions.left))
        self.addTransition(FSMID, StateID.Jab1, StateID.Standing, self.transFns.checkAttackEnd())

        self.addTransition(FSMID, StateID.Jab2, StateID.Falling, self.transFns.checkAttackEnd(), self.transFns.checkOnGround(False))
        self.addTransition(FSMID, StateID.Jab2, StateID.Jab3, self.transFns.checkAttackEnd(), self.transFns.checkFollowupAttack())
        self.addTransition(FSMID, StateID.Jab2, StateID.Rolling, self.transFns.checkAttackEnd(), self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(FSMID, StateID.Jab2, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.right))
        self.addTransition(FSMID, StateID.Jab2, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.left))
        self.addTransition(FSMID, StateID.Jab2, StateID.Standing, self.transFns.checkAttackEnd())

        self.addTransition(FSMID, StateID.Jab3, StateID.Falling, self.transFns.checkAttackEnd(), self.transFns.checkOnGround(False))
        self.addTransition(FSMID, StateID.Jab3, StateID.Rolling, self.transFns.checkAttackEnd(), self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(FSMID, StateID.Jab3, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.right))
        self.addTransition(FSMID, StateID.Jab3, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.left))
        self.addTransition(FSMID, StateID.Jab3, StateID.Standing, self.transFns.checkAttackEnd())

        self.addTransition(FSMID, StateID.RunAttack1, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(FSMID, StateID.RunAttack1, StateID.RunAttack2, self.transFns.checkAttackEnd(),  self.transFns.checkFollowupAttack())
        self.addTransition(FSMID, StateID.RunAttack1, StateID.Rolling, self.transFns.checkAttackEnd(), self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(FSMID, StateID.RunAttack1, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.right))
        self.addTransition(FSMID, StateID.RunAttack1, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.left))
        self.addTransition(FSMID, StateID.RunAttack1, StateID.Standing, self.transFns.checkAttackEnd())

        self.addTransition(FSMID, StateID.RunAttack2, StateID.Falling, self.transFns.checkOnGround(False))
        self.addTransition(FSMID, StateID.RunAttack2, StateID.Rolling, self.transFns.checkAttackEnd(), self.transFns.checkActionPressed(Actions.dodge))
        self.addTransition(FSMID, StateID.RunAttack2, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.right))
        self.addTransition(FSMID, StateID.RunAttack2, StateID.Running, self.transFns.checkAttackEnd(), self.transFns.checkAction(Actions.left))
        self.addTransition(FSMID, StateID.RunAttack2, StateID.Standing, self.transFns.checkAttackEnd())

        self.addTransition(FSMID, StateID.Jumping, StateID.Falling, self.transFns.checkFalling())

        self.addTransition(FSMID, StateID.Falling, StateID.Jumping, self.transFns.checkGraceJump(), self.transFns.checkOnGround())
        self.addTransition(FSMID, StateID.Falling, StateID.Running, self.transFns.checkOnGround(), self.transFns.checkAction(Actions.right))
        self.addTransition(FSMID, StateID.Falling, StateID.Running, self.transFns.checkOnGround(), self.transFns.checkAction(Actions.left))
        self.addTransition(FSMID, StateID.Falling, StateID.Standing, self.transFns.checkOnGround())


    class TransFns:
        def __init__(self, pressed, previouslyPressed):
            self.checkOnGround = lambda condition = True : lambda e : e.onGround == condition
            self.checkGraceJump = lambda condition = True : lambda e :e.graceJumpBool == condition
            self.checkFollowupAttack = lambda condition = True : lambda e : e.followUpAttackBool == condition
            self.checkAttackEnd = lambda condition = True : lambda e : e.attackEndBool == condition
            self.checkDodging = lambda condition = True : lambda e : e.dodgingBool == condition
            self.checkAction = lambda action, condition = True : lambda e : pressed[action] == condition
            self.checkActionPressed = lambda action, condition = True : lambda e : (pressed[action] and not previouslyPressed[action]) == condition
            self.checkActionHeld = lambda  action, condition = True: lambda e : (pressed[action] and previouslyPressed[action]) == condition
            self.checkFalling =  lambda condition = True: lambda e : (e.yJumpSpeed >= 0 or e.startFalling) == condition
