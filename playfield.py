import random, pygame
from ingredient import *
from cursor import *
from const import *
from tick import *

from explode import *

class Playfield(object):
    # initialize ingredients an empty 6 x 13 gridbox and the cursor
    def __init__(self):
        
        self.animating = False
        self.tick = Tick() # needed for synchronous animation
        
        # playfield has cursor
        self.cursor = Cursor(self)
        self.cursor_group = pygame.sprite.RenderPlain()
        self.cursor_group.add(self.cursor)
        
        # playfield initially has no ingredients
        self.gridbox = [[None for _ in xrange(COLS)] for _ in xrange(ROWS)]
        self.ingredient_group = pygame.sprite.RenderPlain()
        self.ingredient_dict = {}
        for row in xrange(ROWS):
            for col in xrange(COLS):
                self.gridbox[row][col] = None
                self.ingredient_dict[str(col) + ',' + str(row)] = None
                
        # add 4 random rows of ingredients to playfield
        init_rows = 4
        for row in reversed(xrange(ROWS - init_rows - 1, ROWS)):
            for col in xrange(COLS):
                random_ingredient = random.randrange(INGREDIENT_SIZE)
                self.add_ingredient(random_ingredient, row, col)
        #self.remove_ingredient(8, 3)
        ###self.move_down_and_clear()
        #self.add_ingredient(1, 0, 0)
        #self.add_explosed_sprite(0, 0)
        
        self.print_matches()
        
    def add_ingredient(self, name, row, col):
        self.gridbox[row][col] = name
        key = str(col) + ',' + str(row)
        self.ingredient_dict[key] = Ingredient(self, name, col, row)
        self.ingredient_group.add(self.ingredient_dict[key])
        
    def add_ingredient_sprite(self, name, row, col):
        #self.gridbox[row][col] = name
        key = str(col) + ',' + str(row)
        self.ingredient_dict[key] = Ingredient(self, name, col, row)
        self.ingredient_group.add(self.ingredient_dict[key])
        
    def add_explosed_sprite(self, row, col):
        #self.gridbox[row][col] = name
        key = str(col) + ',' + str(row)
        self.ingredient_dict[key] = Explode(self, col, row)
        self.ingredient_group.add(self.ingredient_dict[key])
        
    def remove_ingredient(self, row, col):
        self.gridbox[row][col] = None
        key = str(col) + ',' + str(row)
        if (self.ingredient_dict[key] is not None):
            self.ingredient_group.remove(self.ingredient_dict[key])
            self.ingredient_dict[key] = None
        
    def remove_ingredient_sprite(self, row, col):
        #self.gridbox[row][col] = None
        key = str(col) + ',' + str(row)
        if (self.ingredient_dict[key] is not None):
            self.ingredient_group.remove(self.ingredient_dict[key])
            self.ingredient_dict[key] = None
        
    def get_ingredient(self, row, col):
        return self.ingredient_dict[str(col)+','+str(row)]
    
    # swap grids
    def swap(self):
        row, col = self.cursor.row, self.cursor.col
        if self.gridbox[row][col] != None or self.gridbox[row][col+1] != None:
            self.animating = True
            left_ingredient = self.get_ingredient(row, col)
            right_ingredient = self.get_ingredient(row, col+1)
            if (isinstance(left_ingredient, Ingredient)):
                print 'left ingredient is instance of Ingredient'
            if (isinstance(left_ingredient, Explode)):
                print 'left ingredient is instance of Explode'
            if (isinstance(right_ingredient, Ingredient)):
                print 'right ingredient is instance of Ingredient'
            if (isinstance(right_ingredient, Explode)):
                print 'right ingredient is instance of Explode'
            
            #if (not isinstance(left_ingredient, Explode) and not isinstance(right_ingredient, Explode)):
            #    if (left_ingredient is not None):
            if (left_ingredient is not None):
                left_ingredient.move_right(right_ingredient)
            if (right_ingredient is not None):
                right_ingredient.move_left(left_ingredient)
                
    def update_swap(self, row, col):
        self.remove_ingredient_sprite(row, col)
        self.remove_ingredient_sprite(row, col+1)
        if (self.gridbox[row][col] is not None):
            self.add_ingredient_sprite(self.gridbox[row][col], row, col+1)
        if (self.gridbox[row][col+1] is not None):
            self.add_ingredient_sprite(self.gridbox[row][col+1], row, col)
            
        temp = self.gridbox[row][col]
        self.gridbox[row][col] = self.gridbox[row][col+1]
        self.gridbox[row][col+1] = temp
        
        self.animating = False
        
        self.print_matches()
        
    # is top row empty
    def top_row_empty(self):
        top_row_empty = True
        for col in xrange(COLS):
            if(self.gridbox[0][col] != None):
                top_row_empty = False  
                break
        return top_row_empty
        
    # move up playfield
    def move_up(self):
        for row in xrange(ROWS - 1):
            for col in xrange(COLS):
                self.gridbox[row][col]  = self.gridbox[row+1][col]
        self._add_row()
        self.move_down_and_clear()
        
    # add random row to the bottom of the playfield
    def _add_row(self):
        for row in xrange(ROWS - 1, ROWS):
            for col in xrange(COLS):
                self.gridbox[row][col] = random.randrange(SIZE)
                
    # recursively move ingredients down and clear matches of 3 or more
    def move_down_and_clear(self):
        self._move_down(True)
        while (self._clear()):
            self._move_down(True)
            
    # move ingredients down
    def _move_down(self, is_moved):
        if is_moved:
            is_moved = False
            for row in reversed(xrange(ROWS - 1)):
                for col in xrange(COLS):
                    if (self.gridbox[row][col] == None):
                        #print 'empty -- row: ', row, ' col: ', col, '\n'
                        for check_row in reversed(xrange(row)):
                            #print 'check row: ', check_row, ' col: ', col, '\n'
                            if self.gridbox[check_row][col] != None:
                                is_moved = True
                                #print 'found row: ', check_row, ' col: ', col, '\n'
                                #print 'move ', check_row, ', ', col, ' to ', row, ', ', col, '\n'
                                self.gridbox[row][col] = self.gridbox[check_row][col]
                                self.gridbox[check_row][col] = None
                                self._move_down(is_moved)
                                break
                            break
                            
    # clear matches of 3 or more
    def _clear(self):
        is_cleared = False
        clear_set = set()
        for row in xrange(ROWS - 1):
            for col in xrange(COLS):
                match_ingredient = self.gridbox[row][col]
                if (match_ingredient != None):
                    #print 'match_ingredient: ', match_ingredient
                    hor_match_set = set()
                    hor_match_set.add((row, col))
                    match_num = 1
                    next_col = col + 1
                    while (match_num > 0 and next_col < COLS):
                        #print next_rows
                        next_ingredient = self.gridbox[row][next_col]
                        #print 'hor next_ingredient: ', next_ingredient
                        if (match_ingredient == next_ingredient):
                            match_num += 1
                            hor_match_set.add((row, next_col))
                        else:
                            break
                        next_col += 1
                    if (match_num >= 3):
                        clear_set = clear_set.union(hor_match_set)
                        
                    ver_match_set = set()
                    ver_match_set.add((row, col))
                    match_num = 1
                    next_row = row + 1
                    while (match_num > 0 and next_row < ROWS - 1):
                        #print next_row
                        next_ingredient = self.gridbox[next_row][col]
                        #print 'ver next_ingredient: ', next_ingredient
                        if (match_ingredient == next_ingredient):
                            match_num += 1
                            ver_match_set.add((next_row, col))
                        else:
                            break
                        next_row += 1
                    if (match_num >= 3):
                        clear_set = clear_set.union(ver_match_set)
        #print 'clear_set:', len(clear_set), clear_set
        if len(clear_set) > 0:
            is_cleared = True
            for row, col in clear_set:
                self.gridbox[row][col] = None
        return is_cleared
    
    # clear matches of 3 or more
    def print_matches(self):
        is_cleared = False
        clear_set = set()
        for row in xrange(ROWS - 1):
            for col in xrange(COLS):
                match_ingredient = self.gridbox[row][col]
                if (match_ingredient != None):
                    #print 'match_ingredient: ', match_ingredient
                    hor_match_set = set()
                    hor_match_set.add((row, col))
                    match_num = 1
                    next_col = col + 1
                    while (match_num > 0 and next_col < COLS):
                        #print next_rows
                        next_ingredient = self.gridbox[row][next_col]
                        #print 'hor next_ingredient: ', next_ingredient
                        if (match_ingredient == next_ingredient):
                            match_num += 1
                            hor_match_set.add((row, next_col))
                        else:
                            break
                        next_col += 1
                    if (match_num >= 3):
                        clear_set = clear_set.union(hor_match_set)
                        
                    ver_match_set = set()
                    ver_match_set.add((row, col))
                    match_num = 1
                    next_row = row + 1
                    while (match_num > 0 and next_row < ROWS - 1):
                        #print next_row
                        next_ingredient = self.gridbox[next_row][col]
                        #print 'ver next_ingredient: ', next_ingredient
                        if (match_ingredient == next_ingredient):
                            match_num += 1
                            ver_match_set.add((next_row, col))
                        else:
                            break
                        next_row += 1
                    if (match_num >= 3):
                        clear_set = clear_set.union(ver_match_set)
        print 'clear_set:', len(clear_set), clear_set
        if len(clear_set) > 0:
            is_cleared = True
            for row, col in clear_set:
                self.gridbox[row][col] = None
                self.remove_ingredient_sprite(row, col)
                self.add_explosed_sprite(row, col)
                key = str(col) + ',' + str(row)
                self.ingredient_dict[key] = None
            #for row, col in clear_set:
            #    self.gridbox[row][col] = None
            """
            self.remove_ingredient_sprite(8, 3)
            """
        return is_cleared