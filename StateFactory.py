
from PlayerConsts import PlayerConsts
from TimerController import TimerIDs
from InputHandler import Actions
from HelperFns import clamp

x = 0
y = 1

class direction:
    right = 1
    left = -1
    noChange = 0
    none = 0

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
            #print "enter standing"
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
            #print "enter running"
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
            #print "enter rolling"
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
            #print "enter jab 1"
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
            #print "enter jab 2"
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
            #print "enter jab 3"
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
            #print "enter runAttack 1"
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
            #print "enter runAttack 2"
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
            #print "enter jumping"
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
                ##print "falling left", PlayerConsts.Air.minSpeed, PlayerConsts.Air.maxSpeed, player.gSpeed + direction.left*player.dir*PlayerConsts.Air.xImpulseMagnitude
                player.gSpeed = clamp(PlayerConsts.Air.minSpeed,PlayerConsts.Air.maxSpeed, player.gSpeed + direction.left*player.dir*PlayerConsts.Air.xImpulseMagnitude)
            else:
                if pressed[Actions.right] and not pressed[Actions.left]:
                    player.gSpeed = clamp(PlayerConsts.Air.minSpeed,PlayerConsts.Air.maxSpeed, player.gSpeed + direction.right*player.dir*PlayerConsts.Air.xImpulseMagnitude)

            updateChangeDirection(player, pressed, previouslyPressed)

        def enter(self, player):
            #print "enter falling"
            player.Dgrav = 0
            player.startFalling = False
            player.onGround = False

        def exit(self, player):
            player.yJumpSpeed = 0
            player.Dgrav = -1
            player.graceJumpBool = False
            self.graceJumpTimer.end()
