import pygame
import random
from os.path import join
import lib.Var as Var


class Player(pygame.sprite.Sprite):
    # Atributos privados declarados fuera del constructor
    __image = None
    __rect = None
    __direction = None
    __speed = None
    __colors = None
    __lifes = None

    def __init__(self, groups):
        super().__init__(groups)
        # 👇 ahora carga car.png desde sprite/
        self.__image = pygame.image.load(join("sprite", "car.png")).convert_alpha()
        self.__rect = self.__image.get_rect(
            center=(Var.WIDTH // 2, Var.HEIGHT - self.__image.get_height())
        )
        self.__direction = pygame.math.Vector2(0, 0)
        self.__speed = Var.INITIAL_SPEED
        self.__colors = []
        self.__lifes = 3

    # Métodos de acceso y modificación
    def get_image(self):
        return self.__image

    def get_image_height(self):
        return self.__image.get_height()

    def get_rect(self):
        return self.__rect

    def set_rect_pos(self, pos):
        self.__rect.center = pos

    def get_colors(self):
        return self.__colors

    def add_color(self, ball):
        self.__colors.append(ball)

    def reset_colors(self):
        self.__colors = []

    def get_lifes(self):
        return self.__lifes

    def lose_life(self):
        self.__lifes -= 1

    def reset_lifes(self):
        self.__lifes = 3

    # Propiedades públicas requeridas por pygame.sprite.Group
    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    # Movimiento
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.__direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.__direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        self.__direction = (
            self.__direction.normalize() if self.__direction else self.__direction
        )
        self.__rect.center += self.__direction * self.__speed * dt

        # límites de pantalla
        if self.__rect.bottom >= Var.HEIGHT:
            self.__rect.bottom = Var.HEIGHT
        if self.__rect.top <= Var.TOP_MARGIN:
            self.__rect.top = Var.TOP_MARGIN
        if self.__rect.left <= 0:
            self.__rect.left = 0
        if self.__rect.right >= Var.WIDTH:
            self.__rect.right = Var.WIDTH


class Ball(pygame.sprite.Sprite):
    # Atributos privados
    __image = None
    __rect = None
    __direction = None
    __speed = None
    __color = None

    def __init__(self, surf, color, pos, groups):
        super().__init__(groups)
        self.__image = surf
        self.__rect = self.__image.get_rect(center=pos)
        self.__direction = pygame.math.Vector2(random.choice([-1, 1]), 1)
        self.__speed = Var.BALL_SPEED
        self.__color = color

    # Métodos de acceso
    def get_image(self):
        return self.__image

    def get_rect(self):
        return self.__rect

    def get_color(self):
        return self.__color

    # Propiedades públicas requeridas por pygame.sprite.Group
    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    # Movimiento
    def update(self, dt):
        self.__rect.center += self.__direction * self.__speed * dt

        # rebotes contra bordes
        if self.__rect.bottom >= Var.HEIGHT:
            self.__direction.y *= -1
            self.__rect.bottom = Var.HEIGHT
        if self.__rect.top <= Var.TOP_MARGIN:
            self.__direction.y *= -1
            self.__rect.top = Var.TOP_MARGIN
        if self.__rect.left <= 0:
            self.__direction.x *= -1
            self.__rect.left = 0
        if self.__rect.right >= Var.WIDTH:
            self.__direction.x *= -1
            self.__rect.right = Var.WIDTH


class Button(pygame.sprite.Sprite):
    # Atributos privados
    __image = None
    __rect = None

    def __init__(self, image, x, y):
        super().__init__()
        # 👇 ahora carga los botones desde sprite/
        self.__image = pygame.image.load(join("sprite", image)).convert_alpha()
        self.__rect = self.__image.get_rect(center=(x, y))

    # Métodos de acceso
    def get_image(self):
        return self.__image

    def get_rect(self):
        return self.__rect

    # Propiedades públicas requeridas por pygame.sprite.Group
    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect
