
FPS = 60
timePerFrameInms = 1.0/FPS*1000

class PlayerConsts:
	#All times in fraimes
    maxRunSpeed = 0.15
    maxAirSpeed = 0.15
    class Roll:
        duration = 10 
        cooldown = 10 
        maxSpeed = 0.3
    class Jab1:
    	duration =     26
    	hitBoxStart =  5
    	hitBoxEnd =    16
    class Jab2:
        duration =     29
        hitBoxStart =  3
        hitBoxEnd =    19
    class Jab3:
        duration =     26
        hitBoxStart =  5
        hitBoxEnd =    16
    class RunAttack1:
    	duration =     10
    	hitBoxStart =  3 
    	hitBoxEnd =    8
        runEnd =       5
        speed =        0.2
    class RunAttack2:
        duration =     5
        hitBoxStart =  1 
        hitBoxEnd =    5
        runEnd =       3
        speed =        0.2
    class Jumping:
        initialJumpSpeed = -0.3
        highJumpDgrav = -0.6
        lowJumpDgrav = -0.2
    class Falling:
        endGracePeriod = 17 # in fraimes
        startGracePeriod = 0.1
    class Air:
        xImpulseMagnitude = 0.005
        maxSpeed = 0.15
        minSpeed = 0.05
    class Ground:
        maxSpeed = 0.15
        minSpeed = 0.07
        xImpulseMagnitude = 0.01
