import os, sys, random, pygame, game, ingredient
from pygame.locals import *
from game import *
from ingredient import *

#from game import *

class Playfield(object):
    # static variables
    ROW, COL = 6, 13
    GRID_WIDTH, GRID_HEIGHT = 50, 50
    CURSOR_WIDTH, CURSOR_HEIGHT = 100, 50
    CURSOR_COLOR = (255, 0, 0)
    
    # initialize ingredients an empty 6 x 13 gridbox and the cursor
    def __init__(self):
        self.ingredient = Ingredient()
        self.cursor_offset = self.cursor_x, self.cursor_y = 2, 8
        
    # initialize the playfield gridbox
    def init_playfield(self, row_height):
        self.gridbox = [[Ingredient.EMPTY for row in xrange(Playfield.ROW)] for col in xrange(Playfield.COL)]
        for col in reversed(xrange(Playfield.COL - 1 - row_height, Playfield.COL)):
            for row in xrange(Playfield.ROW):
                self.gridbox[col][row] = random.randrange(Ingredient.SIZE)
                
    # initialize the playfield gridbox
    def startState(self):
        self.gridbox = [[Ingredient.EMPTY for row in xrange(Playfield.ROW)] for col in xrange(Playfield.COL)]
        for col in xrange(Playfield.COL - 7, Playfield.COL):
            for row in xrange(Playfield.ROW):
                self.gridbox[col][row] = random.randrange(Ingredient.SIZE)
                #This part of the code (while loop) makes sure that NO two same colored jewels are generated next to each other
                #This can be improved and make it so that no samed color jewels are generated three in a row
                while self.gridbox[col][row] == self.gridbox[col][row - 1] or self.gridbox[col][row] == self.gridbox[col - 1][row]:
                    self.gridbox[col][row] = random.randrange(Ingredient.SIZE)
                    
    # initialize the playfield gridbox (test)
    def test_init_playfield(self):
        self.gridbox = [[Ingredient.EMPTY for row in xrange(Playfield.ROW)] for col in xrange(Playfield.COL)]
        self.gridbox = [
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
            [Ingredient.TOMATO, Ingredient.TOMATO, Ingredient.TOMATO, Ingredient.TOMATO, Ingredient.TOMATO, Ingredient.TOMATO]
        ]
        
        """
        # a copy of a blank playfield
        self.gridbox = [[Ingredient.EMPTY for row in xrange(Playfield.ROW)] for col in xrange(Playfield.COL)]
        self.gridbox = [
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY],
            [Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY, Ingredient.EMPTY]
        ]
        """
        
    # is top row not empty
    def is_top_not_empty(self):
        top_not_empty = False
        for row in xrange(Playfield.ROW):
            if(self.gridbox[0][row] != Ingredient.EMPTY):
                top_not_empty = True
                break
        return top_not_empty
        
    # move up playfield
    def move_up_playfield(self):
        for col in xrange(Playfield.COL - 1):
            for row in xrange(Playfield.ROW):
                self.gridbox[col][row]  = self.gridbox[col+1][row]
        self._add_row()
        
    # add random row to the bottom of the playfield
    def _add_row(self):
        for col in xrange(Playfield.COL - 1, Playfield.COL):
            for row in xrange(Playfield.ROW):
                self.gridbox[col][row] = random.randrange(Ingredient.SIZE)
                
    # recursively move ingredients down and clear matches of 3 or more
    def update_playfield(self):
        self._move_down(True)
        while (self._clear()):
            self._move_down(True)
            
    # move ingredients down
    def _move_down(self, is_moved):
        if is_moved:
            is_moved = False
            for col in reversed(xrange(Playfield.COL - 1)):
                for row in xrange(Playfield.ROW):
                    ingredient = self.gridbox[col][row]
                    if (ingredient == Ingredient.EMPTY):
                        #print 'empty -- col: ', col, ' row: ', row, '\n'
                        for check_col in reversed(xrange(col)):
                            #print 'check col: ', check_col, ' row: ', row, '\n'
                            if self.gridbox[check_col][row] != Ingredient.EMPTY:
                                is_moved = True
                                #print 'found col: ', check_col, ' row: ', row, '\n'
                                #print 'move ', check_col, ', ', row, ' to ', col, ', ', row, '\n'
                                self.gridbox[col][row] = self.gridbox[check_col][row]
                                self.gridbox[check_col][row] = Ingredient.EMPTY
                                self._move_down(is_moved)
                                break
                            break
                            
    # clear matches of 3 or more
    def _clear(self):
        is_cleared = False
        clear_set = set()
        for col in xrange(Playfield.COL - 1):
            for row in xrange(Playfield.ROW):
                match_ingredient = self.gridbox[col][row]
                if (match_ingredient != Ingredient.EMPTY):
                    #print 'match_ingredient: ', match_ingredient
                    hor_match_set = set()
                    hor_match_set.add((col, row))
                    match_num = 1
                    next_row = row + 1
                    while (match_num > 0 and next_row < Playfield.ROW):
                        #print next_row
                        next_ingredient = self.gridbox[col][next_row]
                        #print 'hor next_ingredient: ', next_ingredient
                        if (match_ingredient == next_ingredient):
                            match_num += 1
                            hor_match_set.add((col, next_row))
                        else:
                            break
                        next_row += 1
                    if (match_num >= 3):
                        clear_set = clear_set.union(hor_match_set)
                        
                    ver_match_set = set()
                    ver_match_set.add((col, row))
                    match_num = 1
                    next_col = col + 1
                    while (match_num > 0 and next_col < Playfield.COL - 1):
                        #print next_col
                        next_ingredient = self.gridbox[next_col][row]
                        #print 'ver next_ingredient: ', next_ingredient
                        if (match_ingredient == next_ingredient):
                            match_num += 1
                            ver_match_set.add((next_col, row))
                        else:
                            break
                        next_col += 1
                    if (match_num >= 3):
                        clear_set = clear_set.union(ver_match_set)
        #print 'clear_set:', len(clear_set), clear_set
        if len(clear_set) > 0:
            is_cleared = True
            for col, row in clear_set:
                self.gridbox[col][row] = Ingredient.EMPTY
        return is_cleared
                
    # draw playfield
    def draw_playfield(self, screen):
        #logic to draw the playfield
        grid_y_offset = Game.FRIDGE_Y + 1
        for col in xrange(Playfield.COL):
            grid_x_offset = Game.FRIDGE_X + 1
            for row in xrange(Playfield.ROW):
                if self.gridbox[col][row] == Ingredient.CARROT:
                    screen.blit(self.ingredient.get_carrot_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.TOMATO:
                    screen.blit(self.ingredient.get_tomato_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.BLUE:
                    screen.blit(self.ingredient.get_blue_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.GREEN:
                    screen.blit(self.ingredient.get_green_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.PURPLE:
                    screen.blit(self.ingredient.get_purple_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.RED:
                    screen.blit(self.ingredient.get_red_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.TEAL:
                    screen.blit(self.ingredient.get_teal_img(), (grid_x_offset, grid_y_offset))
                grid_x_offset += Playfield.GRID_WIDTH
            grid_y_offset += Playfield.GRID_HEIGHT
            
    def draw_cursor(self, screen, x, y):
        pygame.draw.rect(screen, Playfield.CURSOR_COLOR, [x * Playfield.GRID_WIDTH + Game.FRIDGE_X, y * Playfield.GRID_HEIGHT + Game.FRIDGE_Y, Playfield.CURSOR_WIDTH, Playfield.CURSOR_HEIGHT], 5)
        