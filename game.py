"""
 Hurry Up Chef
 Developed by Team Super Group

 http://icecreamcola.com/CS113/Design_Document_Draft.pdf
"""
import os, sys, random, pygame

# Object dimensions
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
GRID_SIZE = GRID_ROW, GRID_COL = 6, 13
FOOD_SIZE = FOOD_WIDTH, FOOD_HEIGHT = 50, 50
#BACKGROUND_SIZE = BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 800, 800
#FRIDGE_SIZE = FRIDGE_WIDTH, FRIDGE_HEIGHT = 300, 625
#SCORE_SIZE = SCORE_WIDTH, SCORE_HEIGHT = 162, 256
#TIME_SIZE = TIME_WIDTH, TIME_HEIGHT = 202, 102
#CHEF_SIZE = CHEF_WIDTH, CHEF_HEIGHT = 286, 381
#FOOD_OFFSET = FOOD_X_OFFSET, FOOD_Y_OFFSET = 0, 0

# Object offsets
BACKGROUND_OFFSET = BACKGROUND_X_OFFSET, BACKGROUND_Y_OFFSET = 0, 0
FRIDGE_OFFSET = FRIDGE_X_OFFSET, FRIDGE_Y_OFFSET = 313, 158
SCORE_OFFSET = SCORE_X_OFFSET, SCORE_Y_OFFSET = 624, 199
TIME_OFFSET = TIME_X_OFFSET, TIME_Y_OFFSET = 100, 171
CHEF_OFFSET = CHEF_X_OFFSET, CHEF_Y_OFFSET = 16, 402

# Color constants
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (250, 174, 122)

# Frames Per Second
FPS = 60

# State constants
#STATE_BALL_IN_PADDLE = 0
#STATE_PLAYING = 1
#STATE_WON = 2
#STATE_GAME_OVER = 3
    
class Ingredient(object):
    # enums
    Empty = -1
    Size = 7
    Carrot, Tomato, Blue, Green, Purple, Red, Teal = xrange(Size)
    
    # initialize ingredient images
    def __init__(self):
        self.carrot_img = pygame.image.load(os.path.join('image', 'carrot.png')).convert_alpha()
        self.tomato_img = pygame.image.load(os.path.join('image', 'tomato.png')).convert_alpha()
        self.blue_img = pygame.image.load(os.path.join('image', 'blue.png')).convert_alpha()
        self.green_img = pygame.image.load(os.path.join('image', 'green.png')).convert_alpha()
        self.purple_img = pygame.image.load(os.path.join('image', 'purple.png')).convert_alpha()
        self.red_img = pygame.image.load(os.path.join('image', 'red.png')).convert_alpha()
        self.teal_img = pygame.image.load(os.path.join('image', 'teal.png')).convert_alpha()
        self.ingredient_list = [self.carrot_img, self.tomato_img, self.blue_img, self.green_img, self.purple_img, self.red_img, self.teal_img]
        
    def get_carrot_img(self):
        return self.carrot_img
        
    def get_tomato_img(self):
        return self.tomato_img
        
    def get_blue_img(self):
        return self.blue_img
        
    def get_green_img(self):
        return self.green_img
        
    def get_purple_img(self):
        return self.purple_img
        
    def get_red_img(self):
        return self.red_img
        
    def get_teal_img(self):
        return self.teal_img
        
    def get_ingredient_list(self):
        return self.ingredient_list
        
    def get_ingredient(self, ingredient):
        return self.ingredient_list[ingredient]
    
class Playfield(object):
    # enums
    Row, Col = 6, 13
    
    # testing
    #pygame.draw.rect(screen, WHITE_COLOR, (FRIDGE_X_OFFSET + 1, FRIDGE_Y_OFFSET + 1, 50, 50), 0)
    #pygame.draw.rect(screen, BLACK_COLOR, (FRIDGE_X_OFFSET + 1 + 50, FRIDGE_Y_OFFSET + 1, 50, 50), 0)
    
    # initialize ingredients an empty 6 x 13 gridbox
    def __init__(self):
        self.ingredient = Ingredient()
        self.gridbox = [[Ingredient.Empty for row in xrange(Playfield.Row)] for col in xrange(Playfield.Col)]
        
    # initialize the playfield gridbox with
    # 3 rows of ingredients to the gridbox
    # plus a row previewing the next row to move up
    def init_playfield(self, row_height):
        for col in reversed(xrange(Playfield.Col - 1 - row_height, Playfield.Col)):
            for row in xrange(Playfield.Row):
                self.gridbox[col][row] = random.randrange(Ingredient.Size)
                
    # test initialize playfield gridbox
    def test_init_playfield(self):
        self.gridbox = [
            [Ingredient.Blue, Ingredient.Blue, Ingredient.Blue, Ingredient.Blue, Ingredient.Blue, Ingredient.Blue],
            [Ingredient.Red, Ingredient.Red, Ingredient.Red, Ingredient.Red, Ingredient.Red, Ingredient.Red],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Carrot, Ingredient.Carrot, Ingredient.Carrot, Ingredient.Carrot, Ingredient.Carrot, Ingredient.Carrot],
            [Ingredient.Tomato, Ingredient.Tomato, Ingredient.Tomato, Ingredient.Tomato, Ingredient.Tomato, Ingredient.Tomato]
        ]
        
        """
        # a copy of a blank playfield
        self.gridbox = [
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty],
            [Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty, Ingredient.Empty]
        ]
        """
        
    # clear matches of 3 or more in the playfield
    def clear_matches(self):
        clear_set = set()
        for col in xrange(Playfield.Col - 1):
            for row in xrange(Playfield.Row):
                match_ingredient = self.gridbox[col][row]
                if (match_ingredient != Ingredient.Empty):
                    #print 'match_ingredient: ', match_ingredient
                    hor_match_set = set()
                    hor_match_set.add((col, row))
                    match_num = 1
                    next_row = row + 1
                    while (match_num > 0 and next_row < Playfield.Row):
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
                    while (match_num > 0 and next_col < Playfield.Col - 1):
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
        #print 'clear_set:', clear_set
        for col, row in clear_set:
            self.gridbox[col][row] = Ingredient.Empty
            
    # move ingredients down
    def move_down(self):
        self.move_down_ingredients(Playfield.Col - 1)
        
    # move down ingredient
    def move_down_ingredients(self, count):
        if count > 0:
            for col in reversed(xrange(Playfield.Col - 1)):
                for row in xrange(Playfield.Row):
                    ingredient = self.gridbox[col][row]
                    if (ingredient == Ingredient.Empty):
                        #print 'empty -- col: ', col, ' row: ', row, '\n'
                        for check_col in reversed(xrange(col)):
                            #print 'check col: ', check_col, ' row: ', row, '\n'
                            if self.gridbox[check_col][row] != Ingredient.Empty:
                                #print 'found col: ', check_col, ' row: ', row, '\n'
                                #print 'move ', check_col, ', ', row, ' to ', col, ', ', row, '\n'
                                self.gridbox[col][row] = self.gridbox[check_col][row]
                                self.gridbox[check_col][row] = Ingredient.Empty
                                self.move_down_ingredients(count - 1)
                                break
                            break
                            
    # move up playfield
    def move_up_playfield(self):
        for col in xrange(Playfield.Col - 1):
            for row in xrange(Playfield.Row):
                self.gridbox[col][row]  = self.gridbox[col+1][row]
        self.add_random_row_to_playfield()
        
    # add random row to the bottom of the playfield
    def add_random_row_to_playfield(self):
        for col in xrange(Playfield.Col - 1, Playfield.Col):
            for row in xrange(Playfield.Row):
                self.gridbox[col][row] = random.randrange(Ingredient.Size)
                
    # draw playfield
    def draw_playfield(self, screen):
        #logic to draw the playfield
        grid_y_offset = FRIDGE_Y_OFFSET + 1
        for col in xrange(Playfield.Col):
            grid_x_offset = FRIDGE_X_OFFSET + 1
            for row in xrange(Playfield.Row):
                if self.gridbox[col][row] == Ingredient.Carrot:
                    screen.blit(self.ingredient.get_carrot_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.Tomato:
                    screen.blit(self.ingredient.get_tomato_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.Blue:
                    screen.blit(self.ingredient.get_blue_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.Green:
                    screen.blit(self.ingredient.get_green_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.Purple:
                    screen.blit(self.ingredient.get_purple_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.Red:
                    screen.blit(self.ingredient.get_red_img(), (grid_x_offset, grid_y_offset))
                elif self.gridbox[col][row] == Ingredient.Teal:
                    screen.blit(self.ingredient.get_teal_img(), (grid_x_offset, grid_y_offset))
                grid_x_offset += FOOD_WIDTH
            grid_y_offset += FOOD_HEIGHT
            
    # return the gridbox
    def get_gridbox(self):
        return self.gridbox

class Game(object):
    # initialize PyGame
    def __init__(self):
        # SDL, on which PyGame is based, uses the environment variable SDL_VIDEO_CENTERED
        # to indicate the windows should be centered. Note the environment variable is set
        # before Pygame is initialized by the call to init().
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        # initialize all imported pygame modules
        pygame.init()

        # set the current window caption
        pygame.display.set_caption("Hurry Up Chef")
        # change the system image for the display window
        pygame.display.set_icon(pygame.image.load(os.path.join('image', 'joystick.png')))

        # hide the mouse cursor
        #pygame.mouse.set_visible(False)
        
        # initialize a window or screen for display
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
	
        # create an object to help track time
        self.clock = pygame.time.Clock()
	
        # create a new Font object from a file
        self.font = pygame.font.Font(os.path.join('font', 'freesansbold.ttf'), 25)

        # initialize game
        self.init_game()

    # intialize game
    def init_game(self):
        #self.score
        #self.time
        #self.level
        #self.difficulty
        
        self.game_over = False
        self.fps = FPS
        
        # load background image
        self.background_img = pygame.image.load(os.path.join('image', 'background.png')).convert_alpha()
        # load background overlay image
        self.background_overlay_img = pygame.image.load(os.path.join('image', 'background_overlay.png')).convert_alpha()
        # load score board image
        self.score_img = pygame.image.load(os.path.join('image', 'score.png')).convert_alpha()
        # load time board image
        self.time_img = pygame.image.load(os.path.join('image', 'time.png')).convert_alpha()
        # load chef image
        self.chef_img = pygame.image.load(os.path.join('image', 'chef.png')).convert_alpha()
        
        # instantiate the playfield gridbox
        self.playfield = Playfield()
        # initialize 3 rows of ingredients to the gridbox
        # and preview the next row to move up
        #self.playfield.init_playfield(3)
        
        self.playfield.test_init_playfield()
        
        #gridbox = self.playfield.get_gridbox()
        #print gridbox
        
    def check_input(self):
        keys = pygame.key.get_pressed()
        
        #if keys[pygame.K_UP]:
        
        #if keys[pygame.K_DOWN]:
        
        #if keys[pygame.K_LEFT]:
        
        #if keys[pygame.K_RIGHT]:
        
        #if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
        #elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            #self.init_game()
        
    def run(self):
        while not self.game_over:
            # limit the framerate
            self.clock.tick(self.fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_over = True
                    if event.key == pygame.K_q:
                        print 'Q key has been pressed to clear matches'
                        self.playfield.clear_matches()
                    if event.key == pygame.K_w:
                        print 'W key has been pressed to move_down_ingredients'
                        self.playfield.move_down()
                    if event.key == pygame.K_e:
                        print 'e key has been pressed to move_up_playfield'
                        self.playfield.move_up_playfield()
                        

            # clear the screen
            self.screen.fill(BACKGROUND_COLOR)

            # draw background
            self.screen.blit(self.background_img, (BACKGROUND_X_OFFSET, BACKGROUND_Y_OFFSET))
            # draw refrigerator
            #self.screen.blit(self.refrigerator_img, (FRIDGE_X_OFFSET, FRIDGE_Y_OFFSET))
            # draw playfield
            self.playfield.draw_playfield(self.screen)
            # draw background_overlay
            self.screen.blit(self.background_overlay_img, (BACKGROUND_X_OFFSET, BACKGROUND_Y_OFFSET))
            # draw score board
            self.screen.blit(self.score_img, (SCORE_X_OFFSET, SCORE_Y_OFFSET))
            # draw time board
            self.screen.blit(self.time_img, (TIME_X_OFFSET, TIME_X_OFFSET))
            # draw chef
            self.screen.blit(self.chef_img, (CHEF_X_OFFSET, CHEF_Y_OFFSET))
            
            #self.check_input()
            
            #if self.state == STATE_PLAYING:
            #elif self.state == STATE_BALL_IN_PADDLE:
            #elif self.state == STATE_GAME_OVER:
            #elif self.state == STATE_WON:


            # display everything in the screen
            pygame.display.flip()

        # quit the game
        pygame.quit()
        sys.exit()

# run the game
if __name__ == "__main__":
    Game().run()
