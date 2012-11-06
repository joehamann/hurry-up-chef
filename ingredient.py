import os, sys, random, pygame, game, playfield
from pygame.locals import *
from game import *
from playfield import *

#import os, pygame

class Ingredient(object):
    # static variables
    EMPTY = -1
    SIZE = 7
    CARROT, TOMATO, BLUE, GREEN, PURPLE, RED, TEAL = xrange(SIZE)
    
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
    