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
        # init swap
        self.swap_speed = 5
        self.moving_right = False
        self.moving_left = False
        self.ingredient_to_left = None
        self.ingredient_to_right = None
        self.dest_left = self.x - GRID_WIDTH
        self.dest_right = self.x + GRID_WIDTH
        # init move down
        self.move_down_speed = 50
        self.dest_row = self.row
        self.dest_y = self.y
        self.move_down_list = []
        # init clear
        self.clearing = False
        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._delay = playfield.tick.delay
        self._last_time = playfield.tick.last_time
        self._frame = playfield.tick.frame
        self._images = self.load_animate_image()
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
        
    def clear(self):
        self.clearing = True
        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._delay = 25
        self._last_time = self.playfield.tick.last_time
        self._frame = -1
        self._images = self.load_clear_image()
        self.image = self._images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
    def inanimate(self):
        self._images = self.load_inanimate_image()
            
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
        # clearing logic
        if self.clearing and self._frame == len(self._images) - 1:
            self.playfield.remove_ingredient(self.row, self.col)
            self.playfield.clear_set.discard((self.row, self.col))
            if not self.playfield.clear_set:
                self.playfield.move_down()
        # move down logic
        if (self.y < self.dest_y):
            self.y += self.move_down_speed
            if self.y > self.dest_y:
                self.y = self.dest_y
            if self.y == self.dest_y:
                self.playfield.move_down_set.discard((self.row, self.dest_row, self.col, self.name))
                if not self.playfield.move_down_set:
                    self.playfield.update_move_down(self.move_down_list)
        # swapping logic (move right)
        if (self.moving_right):
            if (self.x < self.dest_right):
                self.x += self.swap_speed
            else:
                self.moving_right = False
                if (not isinstance(self.ingredient_to_right, Ingredient) or (isinstance(self.ingredient_to_right, Ingredient) and not self.ingredient_to_right.moving_left)):
                    self.playfield.update_swap(self.row, self.col)
        # swapping logic (move left)
        if (self.moving_left):
            if (self.x > self.dest_left):
                self.x -= self.swap_speed
            else:
                self.moving_left = False
                if (not isinstance(self.ingredient_to_left, Ingredient) or (isinstance(self.ingredient_to_left, Ingredient) and not self.ingredient_to_left.moving_right)):
                    self.playfield.update_swap(self.row, self.col-1)
                    
    def load_animate_image(self):
        if self.playfield.level == 1:
            if self.name == INGRED_1:
                return Image.load_sliced_sprites(50, 50, 'baconsprite.png')
            elif self.name == INGRED_2:
                return Image.load_sliced_sprites(50, 50, 'berrysprite.png')
            elif self.name == INGRED_3:
                return Image.load_sliced_sprites(50, 50, 'breadsprite.png')
            elif self.name == INGRED_4:
                return Image.load_sliced_sprites(50, 50, 'cheesesprite.png')
            elif self.name == INGRED_5:
                return Image.load_sliced_sprites(50, 50, 'eggsprite.png')
        elif self.playfield.level == 2:
            if self.name == INGRED_1:
                return Image.load_sliced_sprites(50, 50, 'greenpeppersprite.png')
            elif self.name == INGRED_2:
                return Image.load_sliced_sprites(50, 50, 'carrotsprite.png')
            elif self.name == INGRED_3:
                return Image.load_sliced_sprites(50, 50, 'chickensprite.png')
            elif self.name == INGRED_4:
                return Image.load_sliced_sprites(50, 50, 'eggplantsprite.png')
            elif self.name == INGRED_5:
                return Image.load_sliced_sprites(50, 50, 'tomatosprite.png')
        elif self.playfield.level == 3:
            if self.name == INGRED_1:
                return Image.load_sliced_sprites(50, 50, 'asparagussprite.png')
            elif self.name == INGRED_2:
                return Image.load_sliced_sprites(50, 50, 'beetsprite.png')
            elif self.name == INGRED_3:
                return Image.load_sliced_sprites(50, 50, 'yellowpeppersprite.png')
            elif self.name == INGRED_4:
                return Image.load_sliced_sprites(50, 50, 'mushroomsprite.png')
            elif self.name == INGRED_5:
                return Image.load_sliced_sprites(50, 50, 'steaksprite.png')
        
    def load_clear_image(self):
        if self.playfield.level == 1:
            if self.name == INGRED_1:
                return Image.load_sliced_sprites(50, 50, 'bacon-exp.png')
            elif self.name == INGRED_2:
                return Image.load_sliced_sprites(50, 50, 'berry-exp.png')
            elif self.name == INGRED_3:
                return Image.load_sliced_sprites(50, 50, 'bread-exp.png')
            elif self.name == INGRED_4:
                return Image.load_sliced_sprites(50, 50, 'cheese-exp.png')
            elif self.name == INGRED_5:
                return Image.load_sliced_sprites(50, 50, 'egg-exp.png')
        elif self.playfield.level == 2:
            if self.name == INGRED_1:
                return Image.load_sliced_sprites(50, 50, 'greenpepper-exp.png')
            elif self.name == INGRED_2:
                return Image.load_sliced_sprites(50, 50, 'carrot-exp.png')
            elif self.name == INGRED_3:
                return Image.load_sliced_sprites(50, 50, 'chicken-exp.png')
            elif self.name == INGRED_4:
                return Image.load_sliced_sprites(50, 50, 'eggplant-exp.png')
            elif self.name == INGRED_5:
                return Image.load_sliced_sprites(50, 50, 'tomato-exp.png')
        elif self.playfield.level == 3:
            if self.name == INGRED_1:
                return Image.load_sliced_sprites(50, 50, 'asparagus-exp.png')
            elif self.name == INGRED_2:
                return Image.load_sliced_sprites(50, 50, 'beet-exp.png')
            elif self.name == INGRED_3:
                return Image.load_sliced_sprites(50, 50, 'yellowpepper-exp.png')
            elif self.name == INGRED_4:
                return Image.load_sliced_sprites(50, 50, 'mushroom-exp.png')
            elif self.name == INGRED_5:
                return Image.load_sliced_sprites(50, 50, 'steak-exp.png')
        
    def load_inanimate_image(self):
        if self.playfield.level == 1:
            if self.name == INGRED_1:
                return Image.load_sliced_sprites(50, 50, 'bacon-dead.png')
            elif self.name == INGRED_2:
                return Image.load_sliced_sprites(50, 50, 'berry-dead.png')
            elif self.name == INGRED_3:
                return Image.load_sliced_sprites(50, 50, 'bread-dead.png')
            elif self.name == INGRED_4:
                return Image.load_sliced_sprites(50, 50, 'cheese-dead.png')
            elif self.name == INGRED_5:
                return Image.load_sliced_sprites(50, 50, 'egg-dead.png')
        elif self.playfield.level == 2:
            if self.name == INGRED_1:
                return Image.load_sliced_sprites(50, 50, 'greenpepper-dead.png')
            elif self.name == INGRED_2:
                return Image.load_sliced_sprites(50, 50, 'carrot-dead.png')
            elif self.name == INGRED_3:
                return Image.load_sliced_sprites(50, 50, 'chicken-dead.png')
            elif self.name == INGRED_4:
                return Image.load_sliced_sprites(50, 50, 'eggplant-dead.png')
            elif self.name == INGRED_5:
                return Image.load_sliced_sprites(50, 50, 'tomato-dead.png')
        elif self.playfield.level == 3:
            if self.name == INGRED_1:
                return Image.load_sliced_sprites(50, 50, 'asparagus-dead.png')
            elif self.name == INGRED_2:
                return Image.load_sliced_sprites(50, 50, 'beet-dead.png')
            elif self.name == INGRED_3:
                return Image.load_sliced_sprites(50, 50, 'yellowpepper-dead.png')
            elif self.name == INGRED_4:
                return Image.load_sliced_sprites(50, 50, 'mushroom-dead.png')
            elif self.name == INGRED_5:
                return Image.load_sliced_sprites(50, 50, 'steak-dead.png')
        