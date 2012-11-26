import pygame, sys, os, random
from sound import *

class title_screen(object):
    
    def __init__(self,title_screen_image):
        self.title_screen_image = pygame.image.load(os.path.join('image', title_screen_image))
        self.image_dimensions = self.title_screen_image.get_rect()
	
	self.tomato_image = pygame.image.load(os.path.join('image', "tomato.png"))
	self.tomato_image2 = pygame.image.load(os.path.join('image', "tomato.png"))
	self.tomato_image3 = pygame.image.load(os.path.join('image', "tomato.png"))
	self.tomato_image4 = pygame.image.load(os.path.join('image', "tomato.png"))	
	self.tomato_image5 = pygame.image.load(os.path.join('image', "tomato.png"))
	self.tomato_image6 = pygame.image.load(os.path.join('image', "tomato.png"))	
	
	self.tomato = bounce(257, 300)
	self.tomato2 = bounce(600, 400)
	self.tomato3 = bounce(185, 368)
	self.tomato4 = bounce(500, 200)	
	self.tomato5 = bounce(675, 250)
	self.tomato6 = bounce(75, 225)
	
    def draw(self,screen):
        runTitleScreen = 1
	
        while runTitleScreen:
            for event in pygame.event.get() :
		if event.type == pygame.QUIT: # If user clicked close (the X button)
		    pygame.quit()     
		    sys.exit()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_SPACE :
                        runTitleScreen = 0
			
	    
			
	    screen.fill((0,0,0))
	    
	    screen.blit(self.title_screen_image, self.image_dimensions)
	    screen.blit(self.tomato_image, (self.tomato.x, self.tomato.y))
	    screen.blit(self.tomato_image2, (self.tomato2.x, self.tomato2.y))
	    screen.blit(self.tomato_image3, (self.tomato3.x, self.tomato3.y))
	    screen.blit(self.tomato_image4, (self.tomato4.x, self.tomato4.y))
	    screen.blit(self.tomato_image5, (self.tomato5.x, self.tomato5.y))
	    screen.blit(self.tomato_image6, (self.tomato6.x, self.tomato6.y))
	    
	    self.tomato.bouncey()
	    self.tomato2.bouncey()
	    self.tomato3.bouncey()
	    self.tomato4.bouncey()
	    self.tomato5.bouncey()
	    self.tomato6.bouncey()
	    
	    pygame.display.flip()

class bounce(object):
    def __init__(self, x, y):
	self.x = x
	self.y = y
	self.speed = random.random() * 3
	self.mainX = 0
	self.maxY = random.randrange(50,100)
	self.lock = True
	
    def bouncey(self):
	if self.mainX < self.maxY and self.mainX >= 0:
	    self.y += self.speed
	    self.mainX += self.speed
	    self.lock = True
	else:
	    if self.lock:
		self.lock = False
		self.mainX = -self.maxY
	    if self.mainX >= -self.maxY and self.mainX < 0:
		self.y -= self.speed
		self.mainX += self.speed
	    
	    
	