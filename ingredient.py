import pygame
from image import *
from const import *

class Ingredient(pygame.sprite.Sprite):
    def __init__(self, playfield, name, col, row):
        pygame.sprite.Sprite.__init__(self)
        self.playfield = playfield
        self.name = name
        self.col = col
        self.row = row
        self.x = self.col * GRID_WIDTH + OFFSET_X + 1
        self.y = self.row * GRID_HEIGHT + OFFSET_Y + 1
        
        self.swap_speed = 5
        self.moving_right = False
        self.moving_left = False
        self.ingredient_to_left = None
        self.ingredient_to_right = None
        self.dest_left = self.x - GRID_WIDTH
        self.dest_right = self.x + GRID_WIDTH
        
        self.move_down_speed = 50 #50 1
        self.dest_row = self.row
        self.dest_y = self.y
        self.move_down_list = []
        
        if name == BACON:
            self._images = Image.load_sliced_sprites(50, 50, 'baconsprite.png')
        if name == BELLPEPPER:
            self._images = Image.load_sliced_sprites(50, 50, 'bellpeppersprite.png')
        elif name == CARROT:
            self._images = Image.load_sliced_sprites(50, 50, 'carrotsprite.png')
        elif name == STEAK:
            self._images = Image.load_sliced_sprites(50, 50, 'steaksprite.png')
        elif name == TOMATO:
            self._images = Image.load_sliced_sprites(50, 50, 'tomatosprite.png')

        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._delay = playfield.tick.delay
        self._last_time = playfield.tick.last_time
        self._frame = playfield.tick.frame
        self.image = self._images[self._frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
    def move_right(self, right_ingredient):
        self.moving_right = True
        self.ingredient_to_right = right_ingredient
        
    def move_left(self, left_ingredient):
        self.moving_left = True
        self.ingredient_to_left = left_ingredient
        
    def move_down(self, dest_row, move_down_list):
        self.dest_row = dest_row
        self.dest_y = dest_row * GRID_HEIGHT + OFFSET_Y + 1
        self.move_down_list = move_down_list
        
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
        
        # move down logic
        if (self.y < self.dest_y):
            self.y += self.move_down_speed
            if self.y > self.dest_y:
                self.y = self.dest_y
            if self.y == self.dest_y:
                #print 'done moving from', self.row, 'to', self.dest_row, 'for col', self.col
                # update gridbox
                # remove sprite and add sprite
                self.playfield.move_down_set.discard((self.row, self.dest_row, self.col, self.name))
                if not self.playfield.move_down_set:
                    self.playfield.update_move_down(self.move_down_list)
                #move_down_set.add((src_row, dest_row, col))
        
        # swapping logic
        if (self.moving_right):
            if (self.x < self.dest_right):
                self.x += self.swap_speed
            else:
                self.moving_right = False
                if (not isinstance(self.ingredient_to_right, Ingredient) or (isinstance(self.ingredient_to_right, Ingredient) and not self.ingredient_to_right.moving_left)):
                    self.playfield.update_swap(self.row, self.col)
        
        if (self.moving_left):
            if (self.x > self.dest_left):
                self.x -= self.swap_speed
            else:
                self.moving_left = False
                if (not isinstance(self.ingredient_to_left, Ingredient) or (isinstance(self.ingredient_to_left, Ingredient) and not self.ingredient_to_left.moving_right)):
                    self.playfield.update_swap(self.row, self.col-1)
                    