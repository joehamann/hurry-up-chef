import pygame
from image import *
from const import *

class Explode(pygame.sprite.Sprite):
    def __init__(self, playfield, col, row):
        pygame.sprite.Sprite.__init__(self)
        self.playfield = playfield
        self.playfield.animating = True
        self.col = col
        self.row = row
        self.x = self.col * GRID_WIDTH + OFFSET_X + 1
        self.y = self.row * GRID_HEIGHT + OFFSET_Y + 1
        
        self._images = Image.load_sliced_sprites(20, 20, 'explosed-sprite.png')
        
        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._delay = 25 #25 500
        self._last_time = playfield.tick.last_time
        self._frame = -1
        self.image = self._images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
    def update(self, t):
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.
        if t - self._last_time > self._delay:
            self._frame += 1
            if self._frame >= len(self._images): self._frame = 0
            self.image = self._images[self._frame]
            self._last_time = t
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        if self._frame == len(self._images) - 1:
            self.playfield.remove_ingredient(self.row, self.col)
            self.playfield.clear_set.discard((self.row, self.col))
            if not self.playfield.clear_set:
                self.playfield.test_move_down()
        