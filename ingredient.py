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
        
        self.speed = 5
        self.moving_left = False
        self.moving_right = False
        self.ingredient_to_left = None
        self.ingredient_to_right = None
        self.dest_left = self.x - GRID_WIDTH
        self.dest_right = self.x + GRID_WIDTH
        
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
        self.moving_left = True
        self.ingredient_to_right = right_ingredient
        
    def move_left(self, left_ingredient):
        self.moving_right = True
        self.ingredient_to_left = left_ingredient
        
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
        
        # swapping logic
        if (self.moving_left):
            if (self.x < self.dest_right):
                self.x += self.speed
            else:
                self.moving_left = False
                print "swappingleft: ",self.row, ",", self.col
                if (self.ingredient_to_right is not None):
                    if (not self.ingredient_to_right.moving_right):
                        if (self.playfield.animating):
                            print 'FROM LEFT done swapping'
                            row = self.row
                            col = self.col
                            temp = self.playfield.gridbox[row][col]
                            self.playfield.gridbox[row][col] = self.playfield.gridbox[row][col+1]
                            self.playfield.gridbox[row][col+1] = temp
                            self.playfield.remove_ingredient(self.row, self.col)
                            self.playfield.remove_ingredient(self.row, self.col+1)
                            self.playfield.add_ingredient(self.name, self.row, self.col+1)
                            self.playfield.add_ingredient(self.ingredient_to_right.name, self.row, self.col)
                            """
                            """
                        self.playfield.animating = False
        """
                else:
                    print 'done moving left to right and nothing was on right'
        """
        
        if (self.moving_right):
            if (self.x > self.dest_left):
                self.x -= self.speed
            else:
                self.moving_right = False
                print "swappingright: ",self.row, ",", self.col
                if (self.ingredient_to_left is not None):
                    if (not self.ingredient_to_left.moving_left):
                        if (self.playfield.animating):
                            print 'FROM RIGHT done swapping'
                            row = self.row
                            col = self.col
                            #print self.row, ",", self.col
                            temp = self.playfield.gridbox[row][col]
                            self.playfield.gridbox[row][col] = self.playfield.gridbox[row][col-1]
                            self.playfield.gridbox[row][col-1] = temp
                            self.playfield.remove_ingredient(self.row, self.col)
                            self.playfield.remove_ingredient(self.row, self.col-1)
                            self.playfield.add_ingredient(self.name, self.row, self.col-1)
                            self.playfield.add_ingredient(self.ingredient_to_left.name, self.row, self.col)
                            """
                            """
                        self.playfield.animating = False
        """
                else:
                    print 'done moving left to right and nothing was on right'
        """
        
        
        
        
        
    """
        #self.swapping = False
        #self.other_ingredient = None
        #self.dest_x = self.x
        
        
    def swap(self, other_ingredient):
        self.swapping = True
        self.dest_x += GRID_WIDTH
        self.other_ingredient = other_ingredient
        if (self.other_ingredient is not None):
            self.other_ingredient.dest_x -= GRID_WIDTH
            
            
    # self.playfield.animating and self.swapping
    if (self.x < self.dest_x): 
        self.x += self.speed
        if (self.x < self.col * GRID_WIDTH + OFFSET_X + 1): 
            self.x = self.col * GRID_WIDTH + OFFSET_X + 1
        if (self.other_ingredient is not None):
            if (self.other_ingredient.x > self.other_ingredient.dest_x): 
                self.other_ingredient.x = self.other_ingredient.speed
                if (self.other_ingredient.x < self.other_ingredient.col * GRID_WIDTH + OFFSET_X + 1): 
                    self.other_ingredient.x = self.other_ingredient.col * GRID_WIDTH + OFFSET_X + 1
    """
    
    
    ###def draw(self, screen):
        ###screen.blit(self.image, self.rect)
        