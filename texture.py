import pygame

class IDMaker():
    def __init__(self):
        self.num = 0
    def __call__(self):
        self.num+=1
        return self.num

idMaker = IDMaker()


class TextureID:
	none = idMaker()
	player = idMaker()

class RenderHandler(object)
	def __init__(self):

		self.textures = 
			{ 
			TextureID.player : pygame.image.load("myimage.bmp") 
			}

    	self.surface = pygame.display.set_mode(view.size)
    	self.


    def draw(self, graphics, geometries):
    	for eID in graphics:
    		self.surface.blit(self.textures[graphics[eID].tID], geometries[g.id], graphics[eID].area)

class Graphic(object):
	def __init__(self, TextureID, area = None):
		self.tID = TextureID
		self.area = area

class Geometry(object):
	def __init__(self):
		self.pos = np.array([0,0])

class Movement(object):
	def __init__(self):
		self.vel = np.array([0,0])
		self.__dir = direction.right

class Physic(object):
	def __init__(self):
		self.vel = np.array([0,0])
		self.__dir = direction.right
		self.colBox = pygame.Rect(0, 0, 10, 10)
		self.active = True

class Gravity(object):
	def __init__(self):
		

