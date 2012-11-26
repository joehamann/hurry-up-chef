import pygame, os

class Sound(object):
    def __init__(self):
        self.moveSound = pygame.mixer.Sound(os.path.join('sound', "move.wav"))
        self.criticalMusic = pygame.mixer.Sound(os.path.join('sound', "critical.ogg"))
        self.clearSound = pygame.mixer.Sound(os.path.join('sound', "clear.wav"))
        self.introMusic = pygame.mixer.Sound(os.path.join('sound', "intro.ogg"))
        self.dropSound = pygame.mixer.Sound(os.path.join('sound', "drop.wav"))
        pygame.mixer.music.load(os.path.join('sound', "yoshi world.ogg"))