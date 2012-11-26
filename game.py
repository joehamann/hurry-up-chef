"""
 Hurry Up Chef
 Developed by Team Super Group
"""
import os, sys, pygame
from playfield import *
from sound import *
from title_screen import *
from scoreboard import *
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
        pygame.display.set_icon(Image.load_image('icon.png')) # change the system image for the display window
        self.sound = Sound()
        self.playIntro()
        self.font = pygame.font.Font(os.path.join('font', 'freesansbold.ttf'), 25) # create a new Font object from a file
        pygame.mouse.set_visible(False) # hide the mouse cursor
        pygame.key.set_repeat(20,120) # generate multiple KEYDOWN events from keys held down
        self.clock = pygame.time.Clock() # create an object to help track time
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
        self.title_screen = title_screen(TITLE_SCREEN)
        self.title_screen.draw(self.screen)
        self.sound.introMusic.stop()
        pygame.mixer.music.play(-1)
        self.timeboard = Timeboard(100,100)
        self.scoreboard = Scoreboard(600,200,0)
        pygame.time.set_timer(UPDATE_TIMEBOARD, SECOND) # call UPDATE_TIMEBOARD event every 1 seconds        
        pygame.time.set_timer(UPDATE_PLAYFIELD, INTERVAL) # call UPDATE_PLAYFIELD event every 5 seconds
        
    # quit the game
    def quit(self):
        self.game_over = True
        self.game_quit = True
        
    def playIntro(self):
        movie = pygame.movie.Movie(os.path.join('image', "intro.mpg"))
        movie_resolution = movie.get_size ()
        pygame.display.set_mode (movie_resolution)
        movie.set_display (pygame.display.get_surface ())
        self.sound.introMusic.play(-1)
        movie.play ()
        while movie.get_busy():
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # If user clicked close (the X button)
                    pygame.quit()
                    sys.exit()
        
    def check_game_over(self): # check if game over
        if not self.playfield.top_row_empty():
            self.game_over = True
        
    # run the game
    def run(self):
        PLAYING = False
        while not self.game_quit:
            # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.init()
                    self.sound.backgroundMusic.stop()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.playfield.cursor.move_up()
                    self.sound.moveSound.play()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.playfield.cursor.move_down()
                    self.sound.moveSound.play()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.playfield.cursor.move_left()
                    self.sound.moveSound.play()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.playfield.cursor.move_right()
                    self.sound.moveSound.play()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.key.set_repeat(20,120) # prevent multiple KEYDOWN event for K_SPACE
                    if not self.game_over:
                        self.playfield.swap()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.playfield.print_dictionary()
                elif event.type == UPDATE_PLAYFIELD or (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
                    self.check_game_over()
                    if not self.game_over:
                        self.playfield.move_up()
                    else:
                        self.playfield.inanimate()
                elif event.type == UPDATE_TIMEBOARD:
                    self.timeboard.update()
                    self.timeboard.print_time()
                    self.scoreboard.set_score(self.scoreboard.score + 100)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    self.scoreboard.set_score(self.scoreboard.score - 1000)                
            # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
            
            
            
            # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
            self.playfield.tick.update(pygame.time.get_ticks())
            self.playfield.ingredient_group.update(pygame.time.get_ticks())
            self.playfield.cursor_group.update(pygame.time.get_ticks())
            
            if self.playfield.critical_point():
                self.sound.criticalMusic.stop()
                pygame.mixer.music.unpause()
                PLAYING = False
            else:
                if PLAYING == False:
                    PLAYING = True
                    self.sound.criticalMusic.play(loops = -1)
                    pygame.mixer.music.pause()
            # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
            
            
            
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            self.screen.fill(COLOR) # clear the screen
            self.screen.blit(self.BACKGROUND, POSITION) # draw background
            self.playfield.ingredient_group.draw(self.screen)
            self.screen.blit(self.OVERLAY, POSITION) # draw background_overlay
            self.playfield.cursor_group.draw(self.screen) # draw cursor
            self.screen.blit(self.SCORE, (SCORE_X, SCORE_Y)) # draw score board
            self.screen.blit(self.TIME, (TIME_X, TIME_Y)) # draw time board
            self.screen.blit(self.CHEF, (CHEF_X, CHEF_Y)) # draw chef
            self.timeboard.digit_group.draw(self.screen)
            self.scoreboard.digit_group.draw(self.screen)
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            
            
            
            pygame.display.flip() # display everything in the screen
            self.clock.tick(FPS) # limit the framerate
            #self.clock.tick_busy_loop(FPS) # limit the framerate
            
        pygame.quit() # quit the game
        sys.exit() # exit the system

# run the game
if __name__ == "__main__":
    Game().run()
