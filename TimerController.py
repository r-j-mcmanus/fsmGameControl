

from PlayerConsts import PlayerConsts

class TimerIDs:
    graceJump = 1
    jab1 = 2
    jab2 = 3
    runAttack1 = 4
    runAttack2 = 5
    runAttack3 = 6
    rollTimer = 7
    rollCooldown = 8

class TimerController:
    """
        maintains a dict of all timers and a list of timers of 
        active timers that are decrimented by tick() called 
        each frame.

        The timers are given a duration of 
    """
    class Timer:
        __slots__  = "duration", "elapsed"
        def __init__(self, duration):
            self.duration = duration
            self.elapsed = 0

        def end(self):
            self.elapsed = self.duration

        def ended(self):
            return self.elapsed == self.duration

    def __init__(self):
        self.activeTimers = []
        self.timers = dict()

        self.addTimer(PlayerConsts.Falling.endGracePeriod, TimerIDs.graceJump)

        self.addTimer(PlayerConsts.Jab.duration[0], TimerIDs.jab1)
        self.addTimer(PlayerConsts.Jab.duration[1], TimerIDs.jab2)

        self.addTimer(PlayerConsts.Jab.duration[0], TimerIDs.runAttack1)
        self.addTimer(PlayerConsts.Jab.duration[1], TimerIDs.runAttack2)
        self.addTimer(PlayerConsts.Jab.duration[1], TimerIDs.runAttack3)

        self.addTimer(PlayerConsts.Roll.duration, TimerIDs.rollTimer)
        self.addTimer(PlayerConsts.Roll.cooldown, TimerIDs.rollCooldown)


    def __getitem__(self,index):
        try:
            return self.timers[index]
        except KeyError:
            print index, "not found in timers"
            raise SystemExit

    def addTimer(self, duration, timerID):
        self.timers[timerID] = self.Timer(duration)

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

