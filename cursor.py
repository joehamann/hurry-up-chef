import pygame
from image import *
from const import *

class Cursor(pygame.sprite.Sprite):
    def __init__(self, playfield):
        pygame.sprite.Sprite.__init__(self)
        self.col = 2
        self.row = 8
        
        self._images = Image.load_sliced_sprites(124, 72, 'cursorsprite.png')

        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._delay = playfield.tick.delay
        self._last_time = playfield.tick.last_time
        self._frame = playfield.tick.frame
        self.image = self._images[self._frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.col * GRID_WIDTH + OFFSET_X - 11, self.row * GRID_HEIGHT + OFFSET_Y - 11)
        
    def move_up(self):
        if self.row - 1 >= 0:
            self.row -= 1
            
    def move_down(self):
        if self.row + 1 <= ROWS - 2:
            self.row += 1
            
    def move_left(self):
        if self.col - 1 >= 0:
            self.col -= 1
            
    def move_right(self):
        if self.col + 1 <= COLS - 2:
            self.col += 1
            
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
        self.rect.topleft = (self.col * GRID_WIDTH + OFFSET_X - 11, self.row * GRID_HEIGHT + OFFSET_Y - 11)
        
    ###def draw(self, screen):
        ###screen.blit(self.image, self.rect)
        