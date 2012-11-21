"""
 Hurry Up Chef
 Developed by Team Super Group

 http://icecreamcola.com/CS113/Design_Document_Draft.pdf
"""
import os, sys, pygame
from playfield import *
from timeboard import *

# Game class to run() the game
class Game(object):
    # initialize PyGame
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1' # center display
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        pygame.init() # initialize all imported pygame modules
        self.screen = pygame.display.set_mode(SIZE) # initialize a window or screen for display
        pygame.display.set_caption("Hurry Up Chef") # set the current window caption
        pygame.display.set_icon(Image.load_image('joystick.png')) # change the system image for the display window
        self.font = pygame.font.Font(os.path.join('font', 'freesansbold.ttf'), 25) # create a new Font object from a file
        #pygame.mouse.set_visible(False) # hide the mouse cursor
        pygame.key.set_repeat(20,120) # generate multiple KEYDOWN events from keys held down
        self.clock = pygame.time.Clock() # create an object to help track time
        self.timeboard = Timeboard(pygame.time.get_ticks())
        ###pygame.time.set_timer(UPDATE_PLAYFIELD, INTERVAL) # call UPDATE_PLAYFIELD event every 5 seconds
        pygame.time.set_timer(UPDATE_TIMEBOARD, 1000) # call UPDATE_TIMEBOARD event every 1 seconds
        self.init() # initialize the game
        
    # initialize the game
    def init(self):
        self.BACKGROUND = Image.load_image('background.png') # load background image
        self.OVERLAY = Image.load_image('background_overlay.png') # load background overlay image
        self.SCORE = Image.load_image('score.png') # load score board image
        self.TIME = Image.load_image('time.png') # load time board image
        self.CHEF = Image.load_image('chef.png') # load chef image
        self.playfield = Playfield() # load playfield
        self.game_over = False
        self.game_quit = False
        
    # quit the game
    def quit(self):
        self.game_over = True
        self.game_quit = True
        
    # run the game
    def run(self):
        while not self.game_quit:
            # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.init()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.playfield.cursor.move_up()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.playfield.cursor.move_down()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.playfield.cursor.move_left()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.playfield.cursor.move_right()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.key.set_repeat(20,120) # prevent multiple KEYDOWN event for K_SPACE
                    if not self.game_over and not self.playfield.animating:
                        self.playfield.swap()
                elif event.type == UPDATE_PLAYFIELD or (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
                    if not self.game_over:
                        print 'moveup'
                        ###self.playfield.move_up()
                elif event.type == UPDATE_TIMEBOARD:
                    self.timeboard.update()
                    self.timeboard.print_time()
            # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
            
            
            
            # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
            self.playfield.tick.update(pygame.time.get_ticks())
            self.playfield.ingredient_group.update(pygame.time.get_ticks())
            self.playfield.cursor_group.update(pygame.time.get_ticks())
            # check for game over
            ###if not self.playfield.top_row_empty():
                ###self.game_over = True
            # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
            
            
            
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            self.screen.fill(COLOR) # clear the screen
            self.screen.blit(self.BACKGROUND, POSITION) # draw background
            ###self.playfield.draw(self.screen) # draw playfield
            self.playfield.ingredient_group.draw(self.screen)
            self.screen.blit(self.OVERLAY, POSITION) # draw background_overlay
            self.playfield.cursor_group.draw(self.screen) # draw cursor
            self.screen.blit(self.SCORE, (SCORE_X, SCORE_Y)) # draw score board
            self.screen.blit(self.TIME, (TIME_X, TIME_Y)) # draw time board
            self.screen.blit(self.CHEF, (CHEF_X, CHEF_Y)) # draw chef
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            
            
            
            pygame.display.flip() # display everything in the screen
            self.clock.tick(FPS) # limit the framerate
            #self.clock.tick_busy_loop(FPS) # limit the framerate
            
        pygame.quit() # quit the game
        sys.exit() # exit the system

# run the game
if __name__ == "__main__":
    Game().run()
