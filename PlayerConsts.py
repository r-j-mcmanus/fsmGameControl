
FPS = 60
timePerFrameInms = 1.0/FPS*1000

class PlayerConsts:
	#All times in fraimes
    maxRunSpeed = 0.15
    class Roll:
        duration = 10 
        cooldown = 10 
        maxSpeed = 0.3
    class Jab:
    	duration =     [26,    29]
    	hitBoxStart =  [ 5,     3]
    	hitBoxEnd =    [16,    19]
    class RunAttack:
    	duration =     [10,     5,    15]
    	hitBoxStart =  [ 3,     1,     5] 
    	hitBoxEnd =    [ 8,     5,    15]
        runEnd =       [ 5,     3,     0]
        speed =        [0.2,   0.2,   0.2]
    class Jumping:
        initialJumpSpeed = -0.3
        highJumpDgrav = -0.6
        lowJumpDgrav = -0.2
    class Falling:
        endGracePeriod = 20 # in fraimes
        startGracePeriod = 0.1

