import numpy as np

class SceneGraph(object):
    '''All instances of nodes should only be referanced by THIS class'''
    
    class SceneNode(object):
        def __init__(self):
            self.children = []
            self.parent = None
            self.transform = 1
            #Contains the transformation reative to parent

        def getWorldTransformation(self):
            transform = 1
            while node == None:
                transform = node.transform*transform 
                node = node.parent
            return transform

        def getWorldPosition(self):
            return self.getWorldTransformation()

        def giveBB(self, bb):
            self.bb = bb

        def Destroy(self):
            '''destroy all chidren'''
            self.children = []

        def addChild(self, child):
            assert child not in self.children, "adding child twice"
            child.parent = self
            self.children.append(child)

        def removeChild(self, child):
            self.children.remove(child)

        def draw(self, surface, transform):

            transform *= self.transform
            # transform contains the absolute world transform

            self.drawCurrent(surface, transform)

            for child in self.children:
                child.draw(surface, transform)

        def __drawCurrent(self, surface, transform):
            pass

    class PlayerCharNode(object, SceneNode):
        def __init__(self, playerBB):
            super.__init__(self)
            self.bb = playerBB

        def __drawCurrent(Self, surface, transform):
            surface.draw(transform, bb.textureID)

    class CameraNode(object, SceneNode):
        def __init__(self, cameraBB):
            super.__init__(self)
            self.bb = cameraBB

    class SpriteNode(object):
        def __init__(self, textureID, position);
            super.__init__(self)
            self.textureID = textureID
            self.textureID = position

