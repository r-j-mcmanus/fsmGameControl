

class TimerController:
    """
        maintains a dict of all timers and a list of timers of 
        active timers that are decrimented by tick() called 
        each frame.

        The timers are given a duration of 
    """
    class Timer:
        def __init__(self, duration):
            self.duration = duration
            self.elapsed = 0

    def __init__(self):
        self.activeTimers = []
        self.timers = dict()

    def addTimer(self, duration, timerID):
        self.timers[timerID] = self.Timer(duration)
        return self.timers[timerID]

    def tick(self):
        for timer in self.activeTimers:
            timer.elapsed += 1
            if timer.elapsed == timer.duration:
                self.activeTimers.remove(timer)

    def startTimer(self, timer):
        timer.elapsed = 0
        self.activeTimers.append(timer)
