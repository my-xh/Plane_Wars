import pygame

IMAGE_PATH = 'images/'


class NormalBullet(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(
            IMAGE_PATH + 'bullet1.png').convert_alpha()
        self.speed = 12
        self.active = True

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.active = True
        self.rect.left, self.rect.top = position
