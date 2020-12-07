import pygame
from random import *

IMAGE_PATH = 'images/'

class Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        super().__init__()
        self.width, self.height = bg_size
        self.speed = 5
        self.active = False
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False
    
    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), -100


class BulletSupply(Supply):
    def __init__(self, bg_size):
        self.image = pygame.image.load(IMAGE_PATH + 'bullet_supply.png').convert_alpha()
        super().__init__(bg_size)

class BombSupply(Supply):
    def __init__(self, bg_size):
        self.image = pygame.image.load(IMAGE_PATH + 'bomb_supply.png').convert_alpha()
        super().__init__(bg_size)
