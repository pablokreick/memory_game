import pygame
from os.path import join


class Button(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(join("images", image)).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
