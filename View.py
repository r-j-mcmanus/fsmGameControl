

class View(object):
    def __init__(self, size):
        self.size = size
        self.position = (0,0)
        self.offset = 150
        self.center = 0
        self.centerLambda = lambda : (0,0)

    def centerView(self):
        self.center = self.centerLambda() - self.offset

    def apply(self, rect):
        return rect.move(-self.center[0],0)

    def hook(self, centerLambda):
    	self.centerLambda = centerLambda