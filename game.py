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
    
    #------Pertains to Swap Animation
    SWAP_X = 0
    START_LEFT_BLOCK = 0
    START_RIGHT_BLOCK = 0
    YCOORD = 0
    SWAP_ANIM = False
    COL = 0
    ROW = 0
    ORIGINAL_LEFT_BLOCK = 0
    ORIGINAL_RIGHT_BLOCK = 0
    LOCK = True
    LEFTBLOCK = 0
    RIGHTBLOCK = 0
    SWAP_SPEED = 6.5
    #-------Pertains to Swap Animation
    
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
        self.ingredient = Ingredient()
        
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
                    #self.playfield.init_playfield(4)
                    self.playfield.startState()
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
                    if not self.game_over and Game.SWAP_ANIM == False:
                        Game.START_LEFT_BLOCK = self.playfield.cursor_x * Playfield.GRID_WIDTH + Game.FRIDGE_X
                        Game.START_RIGHT_BLOCK = Game.START_LEFT_BLOCK + 50
                        Game.YCOORD = self.playfield.cursor_y * Playfield.GRID_HEIGHT + Game.FRIDGE_Y                            
                        Game.SWAP_ANIM = True
                        Game.ROW = self.playfield.cursor_x
                        Game.COL = self.playfield.cursor_y
                elif event.type == UPDATE_PLAYFIELD or (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
                    self.check_game() ## check for game over
                    if not self.game_over and Game.SWAP_ANIM != True:
                        print 'move up and update playfield after manual move up'
                        self.playfield.cursor_y -= 1
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
            
            #swap animation. the reason why I have it called every loop is because this
            #allows the animation to be in parallel with the game, instead of having the animation
            #freeze the game until the animation is over
            
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            
            if Game.SWAP_ANIM == True:
                self.swap()
            # display everything in the screen
            pygame.display.flip()
            
            # limit the framerate
            self.clock.tick(Game.FPS)
            
        # quit the game
        pygame.quit()
        sys.exit()
        
    def swap(self):
        #less than 50 means that move the ingredients no more than 50 pixels
        if Game.SWAP_X < 50:
            #the purpose of LOCK is to keep the original swapped ingredients while the game
            #loop is still running
            if Game.LOCK == True:
                Game.LOCK = False
                
                #LEFT and RIGHT BLOCK fetches and stores the ingredients in the cursor to blit
                Game.LEFTBLOCK = self.playfield.getIngredients(Game.COL, Game.ROW)         
                Game.RIGHTBLOCK = self.playfield.getIngredients(Game.COL, Game.ROW+1)
                
                #ORIGINALS that stores the original ingredients. The purpose of this is to restore
                #the original ingredients after the animation is done
                Game.ORIGINAL_LEFT_BLOCK = self.playfield.gridbox[Game.COL][Game.ROW]
                Game.ORIGINAL_RIGHT_BLOCK = self.playfield.gridbox[Game.COL][Game.ROW+1]                
            
            self.blitSwap()

            Game.START_LEFT_BLOCK += Game.SWAP_SPEED
            Game.START_RIGHT_BLOCK -= Game.SWAP_SPEED
            Game.SWAP_X += Game.SWAP_SPEED
            
            #this part of the code erases the original ingredient that is locked on the board
            #during the animation. If this code isn't here, during that animation, there will be one
            #ingredient moving across, and the same ingredient still sitting in it's original place
            self.playfield.gridbox[Game.COL][Game.ROW] = Ingredient.EMPTY
            self.playfield.gridbox[Game.COL][Game.ROW+1] = Ingredient.EMPTY    
            
        else:
            #this occurs when the animation is finished
            if Game.SWAP_ANIM == True:
                #it needs one last blitSwap or else there will be a flicker after the animation is finished
                self.blitSwap()
                self.playfield.gridbox[Game.COL][Game.ROW] = Game.ORIGINAL_RIGHT_BLOCK
                self.playfield.gridbox[Game.COL][Game.ROW+1] = Game.ORIGINAL_LEFT_BLOCK             
                self.playfield.update_playfield()         
                
                #reset all animation values for the next swap
                Game.SWAP_X = 0
                Game.SWAP_ANIM = False
                Game.LOCK = True
    
    def blitSwap(self):
        if (Game.LEFTBLOCK == "blue"):
            self.screen.blit(self.ingredient.blue_img, [Game.START_LEFT_BLOCK, Game.YCOORD])
        elif (Game.LEFTBLOCK == "red"):
            self.screen.blit(self.ingredient.red_img, [Game.START_LEFT_BLOCK, Game.YCOORD])
        elif (Game.LEFTBLOCK == "carrot"):
            self.screen.blit(self.ingredient.carrot_img, [Game.START_LEFT_BLOCK, Game.YCOORD])
        elif (Game.LEFTBLOCK == "teal"):
            self.screen.blit(self.ingredient.teal_img, [Game.START_LEFT_BLOCK, Game.YCOORD])
        elif (Game.LEFTBLOCK == "purple"):
            self.screen.blit(self.ingredient.purple_img, [Game.START_LEFT_BLOCK, Game.YCOORD])
        elif (Game.LEFTBLOCK == "tomato"):
            self.screen.blit(self.ingredient.tomato_img, [Game.START_LEFT_BLOCK, Game.YCOORD])
        elif (Game.LEFTBLOCK == "green"):
            self.screen.blit(self.ingredient.green_img, [Game.START_LEFT_BLOCK, Game.YCOORD])

        if (Game.RIGHTBLOCK == "blue"):
            self.screen.blit(self.ingredient.blue_img, [Game.START_RIGHT_BLOCK, Game.YCOORD])
        elif (Game.RIGHTBLOCK == "red"):
            self.screen.blit(self.ingredient.red_img, [Game.START_RIGHT_BLOCK, Game.YCOORD])
        elif (Game.RIGHTBLOCK == "carrot"):
            self.screen.blit(self.ingredient.carrot_img, [Game.START_RIGHT_BLOCK, Game.YCOORD])
        elif (Game.RIGHTBLOCK == "teal"):
            self.screen.blit(self.ingredient.teal_img, [Game.START_RIGHT_BLOCK, Game.YCOORD])
        elif (Game.RIGHTBLOCK == "purple"):
            self.screen.blit(self.ingredient.purple_img, [Game.START_RIGHT_BLOCK, Game.YCOORD])
        elif (Game.RIGHTBLOCK == "tomato"):
            self.screen.blit(self.ingredient.tomato_img, [Game.START_RIGHT_BLOCK, Game.YCOORD])
        elif (Game.RIGHTBLOCK == "green"):
            self.screen.blit(self.ingredient.green_img, [Game.START_RIGHT_BLOCK, Game.YCOORD])         

        

# run the game
if __name__ == "__main__":
    Game().run()
