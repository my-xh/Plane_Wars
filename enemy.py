import pygame
from random import *

IMAGE_PATH = 'images/'


class Enemy(pygame.sprite.Sprite):

    def __init__(self, bg_size):
        super().__init__()
        self.width, self.height = bg_size
        self.active = True
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        pass


class Small_Enemy(Enemy):

    def __init__(self, bg_size):
        super().__init__(bg_size)
        self.speed = 2

        self.image = pygame.image.load(
            IMAGE_PATH + 'enemy1.png').convert_alpha()
        self.destroy_images = [
            pygame.image.load(IMAGE_PATH + 'enemy1_down1.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy1_down2.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy1_down3.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy1_down4.png').convert_alpha(),
        ]

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = randint(
            0, self.width - self.rect.width), randint(-5 * self.height, 0)

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(
            0, self.width - self.rect.width), randint(-5 * self.height, 0)


class Middle_Enemy(Enemy):
    energy = 8

    def __init__(self, bg_size):
        super().__init__(bg_size)
        self.speed = 1
        self.energy = __class__.energy

        self.image = pygame.image.load(
            IMAGE_PATH + 'enemy2.png').convert_alpha()
        self.destroy_images = [
            pygame.image.load(IMAGE_PATH + 'enemy2_down1.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy2_down2.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy2_down3.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy2_down4.png').convert_alpha(),
        ]
        self.image_hit = pygame.image.load(
            IMAGE_PATH + 'enemy2_hit.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = randint(
            0, self.width - self.rect.width), randint(-10 * self.height, -1 * self.height)

    def reset(self):
        self.active = True
        self.energy = __class__.energy
        self.rect.left, self.rect.bottom = randint(
            0, self.width - self.rect.width), randint(-10 * self.height, -1 * self.height)


class Big_Enemy(Enemy):
    energy = 20

    def __init__(self, bg_size):
        super().__init__(bg_size)
        self.speed = 1
        self.energy = __class__.energy

        self.image_1 = pygame.image.load(
            IMAGE_PATH + 'enemy3_n1.png').convert_alpha()
        self.image_2 = pygame.image.load(
            IMAGE_PATH + 'enemy3_n2.png').convert_alpha()
        self.destroy_images = [
            pygame.image.load(IMAGE_PATH + 'enemy3_down1.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy3_down2.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy3_down3.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy3_down4.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy3_down5.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'enemy3_down6.png').convert_alpha(),
        ]
        self.image_hit = pygame.image.load(
            IMAGE_PATH + 'enemy3_hit.png').convert_alpha()

        self.rect = self.image_1.get_rect()
        self.rect.left, self.rect.bottom = randint(
            0, self.width - self.rect.width), randint(-15 * self.height, -5 * self.height)
        self.mask = pygame.mask.from_surface(self.image_1)

    def reset(self):
        self.active = True
        self.energy = __class__.energy
        self.rect.left, self.rect.bottom = randint(
            0, self.width - self.rect.width), randint(-15 * self.height, -5 * self.height)


class Enemies(pygame.sprite.Group):

    def __init__(self, name='all'):
        super().__init__()
        self.name = name.strip().lower()


class AllEnemies(Enemies):

    def add_enemies(self, group, num, bg_size):
        if group.name == 'small':
            NewEnemy = Small_Enemy
        elif group.name == 'middle':
            NewEnemy = Middle_Enemy
        elif group.name == 'big':
            NewEnemy = Big_Enemy
        for i in range(num):
            enemy = NewEnemy(bg_size)
            self.add(enemy)
            group.add(enemy)
