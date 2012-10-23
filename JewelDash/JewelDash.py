#What needs to be done:
    #Organize the code into OOP style
    #Add animation for the jewels switching
    #Add animation for the jewels dropping
    #Add powerups

import pygame
import os
import random

#this code places the window at the center of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'  

#this code is VERY important if you want to add sound. By default, pygame
#has a bit of delay when an action is called with the sound. This code makes
#the buffer bigger, thus getting rid of sound delay
pygame.mixer.pre_init(44100, -16, 2, 2048)  

pygame.init()

#every 5 seconds, the board will move up
pygame.time.set_timer(pygame.USEREVENT+1, 5000) 

screen = pygame.display.set_mode([600, 800])
done = False
restart = False
clock = pygame.time.Clock()
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
brownScore = (139, 125, 107)

#this is the box that switches the jewels
def drawPlayBox(screen, x, y):
    pygame.draw.rect(screen, red, [x,y,100,50], 5)
    
#this part mostly concern the red play box
xCoord = 250
yCoord = 350
prevXCoord = 250
prevYCoord = 350
#------------------------------------------

frameCount = 0
scoreCount = 0
grid=[]

font = pygame.font.Font('freesansbold.ttf', 25)
score = font.render("Score", True, black)
moveSound = pygame.mixer.Sound("move2.wav")
matchSound = pygame.mixer.Sound("match2.wav")
backGroundMusic = pygame.mixer.Sound("backgroundmusic.ogg")
listOfGems = ["purple", "green", "red", "blue", "teal"]
backgroundImage = pygame.image.load("background.png").convert()
gameOverImage = pygame.image.load("gameover.png").convert()
gameOverSound = pygame.mixer.Sound("gameover.ogg")
drawPlayBox(screen, 250, 350)

#since my game uses a grid board, it is necessary to make a 2D array
#btw, I mised rows with columns and columns with rows. SORRY FOR THE CONFUSIONS
#I got confused myself. So this means that there are 13 rows and 6 columns but again
#I mised it up. Another thing, the play grid is actually row 1-12. Row 0 is the marker
#for when the game ends if the jewel hits that marker
for row in range(6):
    grid.append([])
    for column in range(13):
        grid[row].append(0) # Append a cell

def startState():
    global grid
    backGroundMusic.play(loops = -1)

    #initialize the top half of the empty board with Nulls (meaning the cell is empty)
    for row in range(6):
        for column in range(1,6):   #range is 1-6 because because the top row is a marker for game over
            grid[row][column] = "Null" + str(random.randrange(1,50)) #Why is it Null + random number? This is because if it's just null by itself, then the top half of the board will be a bunch of matched "jewels".
                                                                     #For example, the top row will be Null Null Null Null Null Null. This will make the program thinks there is a match so instead, I made it
                                                                     #Null + random number so that it will be Null3 Null16 Null32 Null1 Null33 Null11. I made it 1-50 because when I had it 1-10, there were still
                                                                     #matching Null's in a row!!
    
    #draw the board for the first time with the bottom half of the board filled with jewels            
    for row in range(6):
        for column in range(6,13):
            randomGem = listOfGems[random.randrange(5)]            
            grid[row][column] = randomGem
            while grid[row][column] == grid[row][column - 1] or grid[row][column] == grid[row - 1][column]:   #This part of the code (while loop) makes sure that NO two same colored jewels are generated next to each other
                randomGem = listOfGems[random.randrange(5)]                                                   #This can be improved and make it so that no samed color jewels are generated three in a row
                grid[row][column] = randomGem                                                                 
            showRanGem = pygame.image.load(grid[row][column] + ".png").convert()    #showRanGem loads a random gem (jewel) into a part of the grid
            screen.blit(showRanGem, [150 + (row * 50), 300 + (column * 50)])  
                
    #initiate top row (invisible) as end marker
    for row in range (6):
        for column in range (1):
            grid[row][column] = "end"

#move the board up with and add a random bottom line at every event second
def moveUp():
    #in python, global variables are treated differently.
    #You have to specifically state it in a function or else that variable will
    #be treated as a local variable. These are the variable that I'm explicitly
    #telling python to treat as a global
    global done, yCoord, xCoord, restart, prevXCoord, prevYCoord, scoreCount, frameCount
    yCoord -= 50
    for row in range(6):
        for column in range(1,13):
            if not "Null" in grid[row][column]:    #if the grid is not null, generate a gem
                if grid[row][column - 1] == "end":    #if the jewel hits the end marker
                    backGroundMusic.stop()
                    screen.fill(black)
                    screen.blit(gameOverImage, [0,0])
                    pygame.display.flip()
                    gameOverSound.play(loops = -1)
                    while 1:                         #this while loops waits for the user to play again or quit
                        event = pygame.event.wait()
                        if event.type == pygame.QUIT:
                            done = True
                            break
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                            done = True
                            break
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_y:  #if play again, reset the game
                            gameOverSound.stop()
                            for row in range(6):
                                for column in range(13):          
                                    grid[row][column] = "clear"
                            startState()
                            restart = True
                            xCoord = 250
                            yCoord = 350
                            prevXCoord = 250
                            prevYCoord = 350
                            scoreCount = 0
                            frameCount = 0
                            break
                if done == True or restart == True:
                    break
                else:
                    grid[row][column - 1] = grid[row][column] 
                    if column == 12:
                        while grid[row][column] == grid[row][column - 1] or grid[row][column] == grid[row - 1][column]:
                            randomGem = listOfGems[random.randrange(5)] 
                            grid[row][column] = randomGem   
                    else:
                        grid[row][column - 1] = grid[row][column]
        if done == True or restart == True:
            break        
                        

# -------- Main Program Loop -----------
global done, scoreCount, xCoord, yCoord, prevXCoord, prevYCoord, frameCount
startState()
while done==False:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT+1:
            matchSound.play()
            moveUp()
            restart = False
            if done == True:
                break
        if event.type == pygame.QUIT: # If user clicked close (the X button)
            done=True 
        if event.type == pygame.KEYDOWN:
            moveSound.play()           
            if event.key == pygame.K_LEFT:
                prevXCoord = xCoord
                xCoord -= 50
            if event.key == pygame.K_RIGHT:
                prevXCoord = xCoord
                xCoord += 50
            if event.key == pygame.K_UP:
                prevYCoord = yCoord
                yCoord -= 50
            if event.key == pygame.K_DOWN:
                prevYCoord = yCoord
                yCoord += 50  
            if event.key == pygame.K_SPACE:
                row = xCoord // 50
                column = yCoord // 50
                temp = grid[row - 3][column - 1]
                grid[row - 3][column - 1] = grid[row - 2][column - 1]
                grid[row - 2][column - 1] = temp
                
    screen.fill(white)
    screen.blit(backgroundImage, [0,0])
    screen.blit(score, [265, 25])
    scoreBoard = font.render("%012d" % scoreCount, True, black)
    screen.blit(scoreBoard, [212, 58])
    
    #draw the board's current state
    for row in range(6):
        for column in range(1,13):
            if not "Null" in grid[row][column]:
                showRanGem = pygame.image.load(grid[row][column] + ".png").convert()
                showRanGem.set_colorkey(white)
                if column < 12:
                    if "Null" in grid[row][column + 1]:
                        grid[row][column + 1] = grid[row][column]
                        grid[row][column] = "Null" + str(random.randrange(1,50))
                screen.blit(showRanGem, [150 + (row * 50), 50 + (column * 50)])     
    
    #draw and move play box (the red rectangle)
    #this block of code also keeps the red play box bounded to the board
    if xCoord >= 150 and xCoord <= 350 and yCoord >= 100 and yCoord <= 650:
        drawPlayBox(screen, xCoord, yCoord)
        prevXCoord = xCoord
        prevYCoord = yCoord
    else:
        drawPlayBox(screen, prevXCoord, prevYCoord)
        xCoord = prevXCoord
        yCoord = prevYCoord
    
    #this block of code is what displays the timer
    totalSeconds = frameCount // 30
    minutes = totalSeconds // 60
    seconds = totalSeconds % 60
    timer = font.render("Time: %02d:%02d" % (minutes,seconds), True, black)
    screen.blit(timer, [225, 745])
     
    # update the screen with what we've drawn.
    frameCount += 1
    pygame.display.flip()
 
    # Limit to 30 frames per second
    clock.tick(30)
    
    #check for matches
    #there is a bug in my code that only matches three jewels. So if 4 or 5 jewels line up, it will only match up three
    #check for horizontal matches
    for row in range(6):
        for column in range(1,11):
            if grid[row][column] == grid[row][column + 1] and grid[row][column] == grid[row][column + 2]:
                grid[row][column] = "Null" + str(random.randrange(1,50))
                grid[row][column + 1] = "Null" + str(random.randrange(1,50))
                grid[row][column + 2] = "Null" + str(random.randrange(1,50))
                matchSound.play()
                scoreCount += 5
                
    
    #check for vertical matches
    for row in range(4):
        for column in range(1,13):
            if grid[row][column] == grid[row + 1][column] and grid[row][column] == grid[row + 2][column]:
                grid[row][column] = "Null" + str(random.randrange(1,50))
                grid[row + 1][column] = "Null" + str(random.randrange(1,50))
                grid[row + 2][column] = "Null" + str(random.randrange(1,50))
                matchSound.play()
                scoreCount += 5

pygame.quit ()