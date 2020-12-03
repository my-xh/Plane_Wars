import pygame

IMAGE_PATH = 'images/'


class MyPlane(pygame.sprite.Sprite):

    def __init__(self, bg_size):
        super().__init__()
        self.width, self.height = bg_size
        self.speed = 10
        self.active = True

        self.image_1 = pygame.image.load(
            IMAGE_PATH + 'me1.png').convert_alpha()
        self.image_2 = pygame.image.load(
            IMAGE_PATH + 'me2.png').convert_alpha()
        self.destroy_images = [
            pygame.image.load(IMAGE_PATH + 'me_destroy_1.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'me_destroy_2.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'me_destroy_3.png').convert_alpha(),
            pygame.image.load(IMAGE_PATH + 'me_destroy_4.png').convert_alpha(),
        ]

        self.rect = self.image_1.get_rect()
        self.rect.left, self.rect.bottom = (
            self.width - self.rect.width) // 2, self.height - 60
        self.image = self.image_1

    def move_up(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def move_down(self):
        if self.rect.bottom < self.height - 60:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height - 60

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width
