

from PlayerConsts import PlayerConsts

class IDMaker():
    def __init__(self):
        self.num = 0
    def __call__(self):
        self.num+=1
        return self.num

idMaker = IDMaker()

class TimerIDs:
    graceJump = idMaker()
    jab1 = idMaker()
    jab2 = idMaker()
    jab3 = idMaker()
    runAttack1 = idMaker()
    runAttack2 = idMaker()
    rollTimer = idMaker()
    rollCooldown = idMaker()

class TimerController:
    """
        maintains a dict of all timers and a list of timers of 
        active timers that are decrimented by tick() called 
        each frame.

        The timers are given a duration of 
    """
    class Timer:
        __slots__  = "duration", "elapsed"
        def __init__(self, duration, startFn):
            self.duration = duration
            self.elapsed = 0
            self.start = startFn # hack lol

        def end(self):
            self.elapsed = self.duration

        def ended(self):
            return self.elapsed == self.duration



    def __init__(self):
        self.activeTimers = []
        self.timers = dict()

        self.addTimer(PlayerConsts.Falling.endGracePeriod, TimerIDs.graceJump)

        self.addTimer(PlayerConsts.Jab1.duration, TimerIDs.jab1)
        self.addTimer(PlayerConsts.Jab2.duration, TimerIDs.jab2)
        self.addTimer(PlayerConsts.Jab3.duration, TimerIDs.jab3)

        self.addTimer(PlayerConsts.RunAttack1.duration, TimerIDs.runAttack1)
        self.addTimer(PlayerConsts.RunAttack2.duration, TimerIDs.runAttack2)

        self.addTimer(PlayerConsts.Roll.duration, TimerIDs.rollTimer)
        self.addTimer(PlayerConsts.Roll.cooldown, TimerIDs.rollCooldown)


    def __getitem__(self,index):
        try:
            return self.timers[index]
        except KeyError:
            print index, "not found in timers"
            raise KeyError

    def addTimer(self, duration, timerID):
        self.timers[timerID] = self.Timer(duration, lambda : self.startTimer(timerID))

    def tick(self):
        for timerID in self.activeTimers:
            self.timers[timerID].elapsed += 1
            if self.timers[timerID].elapsed == self.timers[timerID].duration:
                self.activeTimers.remove(timerID)

    def startTimer(self, timerID):
        try:
            self.timers[timerID].elapsed = 0
        except KeyError:
            print index,"not found in timers"
            raise SystemExit
        self.activeTimers.append(timerID)

    def endTimer(self, timerID):
        try:
            self.timers[timerID].end()
        except KeyError:
            print index,"not found in timers"
            raise SystemExit
        if timerID in self.activeTimers:
            self.activeTimers.remove(timerID)

