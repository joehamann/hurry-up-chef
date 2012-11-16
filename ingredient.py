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
    ANIM = -2
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    
    
    # initialize ingredient images
    def __init__(self):
        self.carrot_img = pygame.image.load(os.path.join('image', 'carrot.png')).convert()
        self.carrot_img.set_colorkey(Ingredient.WHITE)
        self.carrot_img.set_colorkey(Ingredient.BLACK)
        self.tomato_img = pygame.image.load(os.path.join('image', 'tomato.png')).convert()
        self.tomato_img.set_colorkey(Ingredient.WHITE)
        self.tomato_img.set_colorkey(Ingredient.BLACK)
        self.blue_img = pygame.image.load(os.path.join('image', 'blue.png')).convert()
        self.blue_img.set_colorkey(Ingredient.WHITE)
        self.green_img = pygame.image.load(os.path.join('image', 'green.png')).convert()
        self.green_img.set_colorkey(Ingredient.WHITE)
        self.purple_img = pygame.image.load(os.path.join('image', 'purple.png')).convert()
        self.purple_img.set_colorkey(Ingredient.WHITE)
        self.red_img = pygame.image.load(os.path.join('image', 'red.png')).convert()
        self.red_img.set_colorkey(Ingredient.WHITE)
        self.teal_img = pygame.image.load(os.path.join('image', 'teal.png')).convert()
        self.teal_img.set_colorkey(Ingredient.WHITE)
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
    