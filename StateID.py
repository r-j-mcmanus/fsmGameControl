
class __IDMaker():
    def __init__(self):
        self.num = 0
    def __call__(self):
        self.num+=1
        return self.num

idMaker = __IDMaker()

#IDs

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
