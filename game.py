"""
 Hurry Up Chef
 Developed by Team Super Group

 http://icecreamcola.com/CS113/Design_Document_Draft.pdf
"""
import os, sys, random, pygame, playfield, ingredient
from pygame.locals import *
from playfield import *
from ingredient import *

#import random
#from pygame.locals import *
#from ingredient import *
#from playfield import *

class Game(object):
    # static variables
    FPS = 60
    INTERVAL = 5000
    SCREEN_SIZE = 800, 800
    BACKGROUND_X, BACKGROUND_Y = 0, 0
    BACKGROUND_COLOR = (255, 255, 255) #(250, 174, 122)
    FRIDGE_X, FRIDGE_Y = 313, 158
    SCORE_X, SCORE_Y = 624, 199
    TIME_X, TIME_Y = 100, 171
    CHEF_X, CHEF_Y = 16, 402
    
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
        self.screen = pygame.display.set_mode(Game.SCREEN_SIZE)
        
        # create a new Font object from a file
        self.font = pygame.font.Font(os.path.join('font', 'freesansbold.ttf'), 25)
        
        # create an object to help track time
        self.clock = pygame.time.Clock()
        
        # initialize game
        self.init_game()
        
    # intialize game
    def init_game(self):
        self.game_quit = False
        self.game_over = False
        
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
        
        # initialize the playfield gridbox
        self.playfield.init_playfield(4)
        #self.playfield.startState()
        #self.playfield.test_init_playfield()
        self.playfield.update_playfield()
        
    def check_input(self):
        keys = pygame.key.get_pressed()
        
        #if keys[pygame.K_UP]:
        
        #if keys[pygame.K_DOWN]:
        
        #if keys[pygame.K_LEFT]:
        
        #if keys[pygame.K_RIGHT]:
        
    def check_game(self):
        if self.playfield.is_top_not_empty():
            self.game_over = True
        
    def run(self):
        # update playfield event
        UPDATE_PLAYFIELD = USEREVENT+1
        pygame.time.set_timer(UPDATE_PLAYFIELD, Game.INTERVAL) # creates a user event that occurs every 3000ms/3seconds
        
        while not self.game_quit:
            # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
            #self.check_input()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.game_quit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.game_over = False
                    self.playfield.init_playfield(4)
                    #self.playfield.startState()
                    #self.playfield.test_init_playfield()
                    self.playfield.update_playfield()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if self.playfield.cursor_x - 1 >= 0:
                        self.playfield.cursor_x -= 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    if self.playfield.cursor_x + 1 <= Playfield.ROW - 2:
                        self.playfield.cursor_x += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if self.playfield.cursor_y - 1 >= 0:
                        self.playfield.cursor_y -= 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if self.playfield.cursor_y + 1 <= Playfield.COL - 2:
                        self.playfield.cursor_y += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not self.game_over:
                        row = self.playfield.cursor_x
                        col = self.playfield.cursor_y
                        if self.playfield.gridbox[col][row] != Ingredient.EMPTY or self.playfield.gridbox[col][row+1] != Ingredient.EMPTY:
                            temp = self.playfield.gridbox[col][row]
                            self.playfield.gridbox[col][row] = self.playfield.gridbox[col][row+1]
                            self.playfield.gridbox[col][row+1] = temp
                        print 'update playfield after swap'
                        self.playfield.update_playfield()
                elif event.type == UPDATE_PLAYFIELD or (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
                    self.check_game() ## check for game over
                    if not self.game_over:
                        print 'move up and update playfield after manual move up'
                        self.playfield.move_up_playfield()
                        self.playfield.update_playfield()
            # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
            
            
            
            # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
            """
            if self.game_over:
                self.playfield.gridbox = [
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT],
                    [Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT, Ingredient.CARROT]
                ]
            """
            # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
            
            
            
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            # clear the screen
            self.screen.fill(Game.BACKGROUND_COLOR)
            # draw background
            self.screen.blit(self.background_img, (Game.BACKGROUND_X, Game.BACKGROUND_Y))
            # draw playfield
            self.playfield.draw_playfield(self.screen)
            # draw background_overlay
            self.screen.blit(self.background_overlay_img, (Game.BACKGROUND_X, Game.BACKGROUND_Y))
            #draw and move the cursor
            self.playfield.draw_cursor(self.screen, self.playfield.cursor_x, self.playfield.cursor_y)
            # draw score board
            self.screen.blit(self.score_img, (Game.SCORE_X, Game.SCORE_Y))
            # draw time board
            self.screen.blit(self.time_img, (Game.TIME_X, Game.TIME_Y))
            # draw chef
            self.screen.blit(self.chef_img, (Game.CHEF_X, Game.CHEF_Y))
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            
            
            
            # display everything in the screen
            pygame.display.flip()
            
            # limit the framerate
            self.clock.tick(Game.FPS)
            
        # quit the game
        pygame.quit()
        sys.exit()

# run the game
if __name__ == "__main__":
    Game().run()
