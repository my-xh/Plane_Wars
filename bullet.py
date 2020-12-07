import pygame

IMAGE_PATH = 'images/'


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.active = False

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False
    
    def reset(self, position):
        self.active = True
        self.rect.left, self.rect.top = position


class NormalBullet(Bullet):

    def __init__(self, position):
        super().__init__()
        self.speed = 12

        self.image = pygame.image.load(
            IMAGE_PATH + 'bullet1.png').convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
    
class SuperBullet(Bullet):
    def __init__(self, position):
        super().__init__()
        self.speed = 14
        self.image = pygame.image.load(
            IMAGE_PATH + 'bullet2.png').convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
    
