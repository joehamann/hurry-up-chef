import pygame
from image import *

class Tick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._images = 2
        self.delay = 500
        self.last_time = 0
        self.frame = 0
        
        # Call update to set our first image.
        #self.update(pygame.time.get_ticks())
        self.frame += 1
        if self.frame >= self._images: self.frame = 0
        
    def update(self, t):
        # Note that this doesn't work if it's been more that self.delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.
        if t - self.last_time > self.delay:
            self.frame += 1
            if self.frame >= self._images: self.frame = 0
            self.last_time = t
            