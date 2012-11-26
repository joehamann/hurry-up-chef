import pygame
from image import *
from const import *



class Digit(pygame.sprite.Sprite):
    def __init__(self, x, y, digit):
            pygame.sprite.Sprite.__init__(self)
            self._images = Image.load_sliced_sprites(DIGIT_WIDTH, DIGIT_HEIGHT, 'OCR-B-Digits.png')
            self.x = x
            self.y = y
            self._frame = digit
            self.image = self._images[self._frame]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)            
            