import random, pygame
from ingredient import *
from cursor import *
from const import *
from tick import *

from explode import *

class Playfield(object):
    # initialize the cursor and ingredients on an empty 6 x 13 playfield
    def __init__(self):
        
        self.animating = False
        self.tick = Tick() # needed for synchronous animation
        self.clear_set = set()
        self.move_down_set = set()
        
        # playfield has cursor
        self.cursor = Cursor(self)
        self.cursor_group = pygame.sprite.RenderPlain()
        self.cursor_group.add(self.cursor)
        
        # playfield initially has no ingredients
        self.ingredient_group = pygame.sprite.RenderPlain()
        self.ingredient_dict = {}
        for row in xrange(ROWS):
            for col in xrange(COLS):
                key = str(col) + ',' + str(row)
                self.ingredient_dict[key] = None
                
        # initialize playfield with random ingredients
        init_rows = 5
        start_row = ROWS - init_rows
        for row in reversed(xrange(start_row, ROWS)):
            for col in xrange(COLS):
                ingredients = set([BACON, BELLPEPPER, CARROT, STEAK, TOMATO])
                if row + 2 < ROWS:
                    row1 = self.get_ingredient(row + 2, col)
                    row2 = self.get_ingredient(row + 1, col)
                    if row1.name == row2.name:
                        ingredients.discard(row1.name)
                if col - 2 >= 0:
                    col1 = self.get_ingredient(row, col - 2)
                    col2 = self.get_ingredient(row, col - 1)
                    if col1.name == col2.name:
                        ingredients.discard(col1.name)
                random_ingredient = list(ingredients)[random.randrange(len(ingredients))]
                self.add_ingredient(random_ingredient, row, col)
        self.test_move_down()
        
    def get_ingredient(self, row, col):
        return self.ingredient_dict[str(col)+','+str(row)]
        
    def add_ingredient(self, name, row, col):
        key = str(col) + ',' + str(row)
        self.ingredient_dict[key] = Ingredient(self, name, col, row)
        self.ingredient_group.add(self.ingredient_dict[key])
        
    def remove_ingredient(self, row, col):
        key = str(col) + ',' + str(row)
        self.ingredient_group.remove(self.ingredient_dict[key])
        self.ingredient_dict[key] = None
        
    def clear_ingredient(self, row, col):
        self.remove_ingredient(row, col)
        key = str(col) + ',' + str(row)
        self.ingredient_dict[key] = Explode(self, col, row)
        self.ingredient_group.add(self.ingredient_dict[key])
    
    def swap(self): # swap grids
        row, col = self.cursor.row, self.cursor.col
        left_ingredient, right_ingredient = self.get_ingredient(row, col), self.get_ingredient(row, col+1)
        if left_ingredient != None or right_ingredient != None:
            if not isinstance(left_ingredient, Explode) and not isinstance(right_ingredient, Explode):
                self.animating = True
                if isinstance(left_ingredient, Ingredient):
                    left_ingredient.move_right(right_ingredient)
                if isinstance(right_ingredient, Ingredient):
                    right_ingredient.move_left(left_ingredient)
                
    def update_swap(self, row, col):
        left_ingredient = self.get_ingredient(row, col)
        right_ingredient = self.get_ingredient(row, col+1)
        
        left_name = -1
        if isinstance(left_ingredient, Ingredient):
            left_name = left_ingredient.name
        right_name = -1
        if isinstance(right_ingredient, Ingredient):
            right_name = right_ingredient.name
        
        self.remove_ingredient(row, col)
        self.remove_ingredient(row, col+1)
        
        if left_name >= 0:
            self.add_ingredient(left_name, row, col+1)
        if right_name >= 0:
            self.add_ingredient(right_name, row, col)
        
        self.test_move_down()
        
    def clear_matches(self): # clear matches of 3 or more
        clear_set = set()
        for row in xrange(ROWS - 1):
            for col in xrange(COLS):
                match_ingredient = self.get_ingredient(row, col)
                if isinstance(match_ingredient, Ingredient):
                    hor_match_set = set()
                    hor_match_set.add((row, col))
                    match_num = 1
                    next_col = col + 1
                    while match_num > 0 and next_col < COLS:
                        next_ingredient = self.get_ingredient(row, next_col)
                        if isinstance(next_ingredient, Ingredient) and match_ingredient.name == next_ingredient.name:
                            match_num += 1
                            hor_match_set.add((row, next_col))
                        else:
                            break
                        next_col += 1
                    if match_num >= 3:
                        clear_set = clear_set.union(hor_match_set)
                        
                    ver_match_set = set()
                    ver_match_set.add((row, col))
                    match_num = 1
                    next_row = row + 1
                    while match_num > 0 and next_row < ROWS - 1:
                        next_ingredient = self.get_ingredient(next_row, col)
                        if isinstance(next_ingredient, Ingredient) and match_ingredient.name == next_ingredient.name:
                            match_num += 1
                            ver_match_set.add((next_row, col))
                        else:
                            break
                        next_row += 1
                    if match_num >= 3:
                        clear_set = clear_set.union(ver_match_set)
        if clear_set:
            self.clear_set = clear_set
            for row, col in clear_set:
                self.clear_ingredient(row, col)
        else:
            self.animating = False
        
    def test_move_down(self): # move ingredients down
        self.animating = True
        move_down_set = set()
        for col in xrange(COLS):
            for row in reversed(xrange(ROWS - 1)):
                if self.get_ingredient(row, col) is None:
                    dest_row = row
                    for _ in reversed(xrange(dest_row)):
                        if self.get_ingredient(_, col) is not None:
                            for src_row in reversed(xrange(_ + 1)):
                                src_ingred = self.get_ingredient(src_row, col)
                                if isinstance(src_ingred, Ingredient):
                                    move_down_set.add((src_row, dest_row, col, src_ingred.name))
                                    dest_row -= 1
                            break
                    break
        if move_down_set:
            self.move_down_set = move_down_set
            for src_row, dest_row, col, _ in move_down_set:
                ingred = self.get_ingredient(src_row, col)
                ingred.move_down(dest_row, list(move_down_set))
        else:
            self.animating = False
            self.clear_matches()
        
        
    def update_move_down(self, move_down_list): # update move down ingredient
        for src_row, dest_row, col, _ in move_down_list:
            self.remove_ingredient(src_row, col)
        for src_row, dest_row, col, src_name in move_down_list:
            self.add_ingredient(src_name, dest_row, col)
        self.animating = False
        self.clear_matches()
        
    def move_up(self): # move up playfield
        self.animating = True
        for row in xrange(ROWS - 1):
            for col in xrange(COLS):
                ingredient = self.get_ingredient(row + 1, col)
                if isinstance(ingredient, Ingredient):
                    ingredient_name = ingredient.name
                    self.remove_ingredient(row, col)
                    self.add_ingredient(ingredient_name, row, col)
        for row in xrange(ROWS - 1, ROWS):
            for col in xrange(COLS):
                ingredients = set([BACON, BELLPEPPER, CARROT, STEAK, TOMATO])
                row1 = self.get_ingredient(row - 2, col)
                row2 = self.get_ingredient(row - 1, col)
                if row1 is not None and row2 is not None and row1.name == row2.name:
                    ingredients.discard(row1.name)
                if col - 2 >= 0:
                    col1 = self.get_ingredient(row, col - 2)
                    col2 = self.get_ingredient(row, col - 1)
                    if col1.name == col2.name:
                        ingredients.discard(col1.name)
                self.remove_ingredient(row, col)
                random_ingredient = list(ingredients)[random.randrange(len(ingredients))]
                self.add_ingredient(random_ingredient, row, col)
        self.animating = False
        
    def top_row_empty(self): # is top row empty
        top_row_empty = True
        for col in xrange(COLS):
            if self.get_ingredient(0, col) is not None:
                top_row_empty = False  
                break
        return top_row_empty
    
    def print_dictionary(self):
        for row in xrange(ROWS):
            for col in xrange(COLS):
                ingredient = self.get_ingredient(row, col)
                if isinstance(ingredient, Ingredient):
                    print ingredient.name,
                elif isinstance(ingredient, Explode):
                    print 'E',
                elif ingredient is None:
                    print "_",
                else:
                    print '#',
            print