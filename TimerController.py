

from PlayerConsts import PlayerConsts

class TimerIDs:
    graceJump = 1

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

    def __getitem__(self,index):
        return self.timers[index]

    def addTimer(self, duration, timerID):
        self.timers[timerID] = self.Timer(duration)

    def tick(self):
        for timerID in self.activeTimers:
            self.timers[timerID].elapsed += 1
            if self.timers[timerID].elapsed == self.timers[timerID].duration:
                self.activeTimers.remove(timerID)

    def startTimer(self, timerID):
        self.timers[timerID].elapsed = 0
        self.activeTimers.append(timerID)

    def endTimer(self, timerID):
        self.timers[timerID].end()
        if timerID in self.activeTimers:
            self.activeTimers.remove(timerID)

