


import pygame
from pygame.locals import *

class InputEvent:
    def __init__(self, key, down):
        self.key = key
        self.down = down
        self.up = not down

class controlerConfig:
	def __init__(self, id, index, state):
		self.id = id
		self.index = index


class ControllerManager:
	def __init__(self):
        self.buttons = ['up', 'down', 'left', 'right', 'start', 'A', 'B', 'X', 'Y', 'L', 'R']
        self.key_map = {
            K_UP : 'up',
            K_DOWN : 'down',
            K_LEFT : 'left',
            K_RIGHT : 'right',
            K_RETURN : 'start',
            K_a : 'A',
            K_b : 'B',
            K_x : 'X',
            K_y : 'Y',
            K_l : 'L',
            K_r : 'R'
        }
        self.keysPressed = {}
        for button in self.buttons:
        	self.keysPressed[button] = False

		pygame.joystick.init()
		if pygame.joystick.get_count() > 0:
			self.joystickConected = True
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()
		else:
			self.joystickConected = False

        # a map from buttons to controlerConfig
        self.joystick_config = {}

        self.quit = False

    def isPressed(self,button):
    	return self.keysPressed[button]

    def getEvents(self):
    	events = []
    	self.keyboard_getEvents(events)
    	self.controler_getEvents(events)
    	return events

    def keyboard_getEvents(self, events)
    	# looks at pygame.events and translates them into 
    	# InputEvent objects and stores in events
    	for event in pygame.event.get():
    		if event,type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
    			self.quit = True

    		if event.type == KEYDOWN or event.type == KEYUP:
                key_pushed_down = event.type == KEYDOWN
                button = self.key_map.get(event.key)
                if button != None:
                    events.append(InputEvent(button, key_pushed_down))
                    self.keysPressed[button] = key_pushed_down

    def controler_getEvents(self, events):
    	for button in self.buttons:
    		config = self.joystick_config.get(button)
    		if config != None:
    			if config.id = "button":
    				qPushed = self.joystick.get_button(config.index)
    				if qPushed != self.keysPressed[button] 
    				#has the state changed from how it is recorded?
    					events.append(InputEvent(button, qPushed))
                    	self.keys_pressed[button] = qPushed

    def is_button_used(self, button_index):
        for button in self.buttons:
            config = self.joystick_config.get(button)
            if config != None and config.id == 'is_button' and config.index == button_index:
                return True
        return False