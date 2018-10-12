
FPS = 60
timePerFrameInms = 1.0/FPS*1000

class PlayerConsts:
	#All times in fraimes
    maxRunSpeed = 0.15
    maxRunAttackSpeed = 0.3
    class Roll:
        duration = 10 
        cooldown = 10 
        maxSpeed = 0.3
    class Jab_1:
    	duration = 26
    	hitBoxStart = 5
    	hitBoxEnd = 16
    class Jab_2:
    	duration = 29
    	hitBoxStart =3
    	hitBoxEnd =19
    class RunAttack:
    	duration = 20
    	hitBoxStart =5
    	hitBoxEnd =15
        runEnd = 10
    class Jumping:
        initialJumpSpeed = -0.5
        highJumpDgrav = -0
        lowJumpDgrav = 0
    class Falling:
        pass

