import pygame
from image import *
from const import *



class Digit(pygame.sprite.Sprite):
    def __init__(self, x, y, digit, colon=0):
            pygame.sprite.Sprite.__init__(self)
            self.colon = colon
            if (self.colon):
                self._images = Image.load_sliced_sprites(COLON_WIDTH, DIGIT_HEIGHT, 'colon.png')
                self._frame = 0
            else:      
                self._images = Image.load_sliced_sprites(DIGIT_WIDTH, DIGIT_HEIGHT, 'OCR-B-Digits.png')
                self._frame = digit
                
            self.x = x
            self.y = y
            
            self.image = self._images[self._frame]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)            
            
    def set_digit(self,digit):
        self._frame = digit
        self.image = self._images[self._frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)          
    