import pygame
import random
from os.path import join
import lib.Var as Var


class Player(pygame.sprite.Sprite):
    __image = None
    __rect = None
    __direction = None
    __speed = None
    __colors = None
    __lifes = None
    __score = None   # 👈 nuevo atributo privado

    def __init__(self, groups):
        super().__init__(groups)
        self.__image = pygame.image.load(join("sprite", "car.png")).convert_alpha()
        self.__rect = self.__image.get_rect(
            center=(Var.WIDTH // 2, Var.HEIGHT - self.__image.get_height())
        )
        self.__direction = pygame.math.Vector2(0, 0)
        self.__speed = Var.INITIAL_SPEED
        self.__colors = []
        self.__lifes = 3
        self.__score = 0

    # ==== Métodos de acceso ====
    def get_image(self): return self.__image
    def get_rect(self): return self.__rect
    def set_rect(self, rect): self.__rect = rect
    def get_direction(self): return self.__direction
    def set_direction(self, direction): self.__direction = direction
    def get_speed(self): return self.__speed
    def set_speed(self, speed): self.__speed = speed
    def get_colors(self): return self.__colors
    def set_colors(self, colors): self.__colors = colors
    def get_lifes(self): return self.__lifes
    def set_lifes(self, lifes): self.__lifes = lifes

    # ==== Score ====
    def get_score(self): return self.__score
    def add_score(self, points): self.__score += points
    def reset_score(self): self.__score = 0

    # ==== Properties ====
    image = property(get_image)
    rect = property(get_rect, set_rect)
    direction = property(get_direction, set_direction)
    speed = property(get_speed, set_speed)
    colors = property(get_colors, set_colors)
    lifes = property(get_lifes, set_lifes)
    score = property(get_score)

    # ==== Movimiento ====
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.__direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.__direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        self.__direction = (
            self.__direction.normalize() if self.__direction else self.__direction
        )
        self.__rect.center += self.__direction * self.__speed * dt

        if self.__rect.bottom >= Var.HEIGHT: self.__rect.bottom = Var.HEIGHT
        if self.__rect.top <= Var.TOP_MARGIN: self.__rect.top = Var.TOP_MARGIN
        if self.__rect.left <= 0: self.__rect.left = 0
        if self.__rect.right >= Var.WIDTH: self.__rect.right = Var.WIDTH


class Ball(pygame.sprite.Sprite):
    __image = None
    __rect = None
    __direction = None
    __speed = None
    __color = None

    def __init__(self, surf, color, groups):
        super().__init__(groups)
        self.__image = surf
        x = random.randint(0, Var.WIDTH - surf.get_width())
        y = random.randint(0, Var.HEIGHT // 4)
        self.__rect = self.__image.get_rect(center=(x, y))
        self.__direction = pygame.math.Vector2(random.choice([-1, 1]), -1)
        self.__speed = Var.BALL_SPEED
        self.__color = color

    def get_image(self): return self.__image
    def get_rect(self): return self.__rect
    def get_color(self): return self.__color

    image = property(get_image)
    rect = property(get_rect)
    color = property(get_color)

    def update(self, dt):
        self.__rect.center += self.__direction * self.__speed * dt
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
    __image = None
    __rect = None

    def __init__(self, image, x, y):
        super().__init__()
        self.__image = pygame.image.load(join("sprite", image)).convert_alpha()
        self.__rect = self.__image.get_rect(center=(x, y))

    def get_image(self): return self.__image
    def set_image(self, image): self.__image = image
    def get_rect(self): return self.__rect
    def set_rect(self, rect): self.__rect = rect

    image = property(get_image, set_image)
    rect = property(get_rect, set_rect)


class HUDLifes:
    __image = None
    __lifes = None

    def __init__(self, image, max_lifes=3):
        self.__image = image
        self.__lifes = max_lifes

    def lose(self): self.__lifes = max(0, self.__lifes - 1)
    def reset(self, value=3): self.__lifes = value

    def draw(self, display):
        for i in range(self.__lifes):
            display.blit(self.__image, (30 + i * 48, 10))

    def get_lifes(self): return self.__lifes
    def set_lifes(self, lifes): self.__lifes = lifes
    lifes = property(get_lifes, set_lifes)


class SoundManager:
    def __init__(self):
        self.__sound_good = pygame.mixer.Sound(join("sounds", "bubble.mp3"))
        self.__sound_wrong = pygame.mixer.Sound(join("sounds", "wrong.mp3"))
        self.__sound_win = pygame.mixer.Sound(join("sounds", "win.mp3"))
        self.__sound_fail = pygame.mixer.Sound(join("sounds", "fail.mp3"))

        pygame.mixer.music.load(join("sounds", "music.mp3"))
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)

    def play_good(self): self.__sound_good.play()
    def play_wrong(self): self.__sound_wrong.play()
    def play_win(self): self.__sound_win.play()
    def play_fail(self): self.__sound_fail.play()


class AssetManager:
    def __init__(self):
        self.__ball_images = {
            "blue": pygame.image.load(join("sprite", "ball-blue.png")).convert_alpha(),
            "lightblue": pygame.image.load(join("sprite", "ball-lightblue.png")).convert_alpha(),
            "green": pygame.image.load(join("sprite", "ball-green.png")).convert_alpha(),
            "red": pygame.image.load(join("sprite", "ball-red.png")).convert_alpha(),
            "violet": pygame.image.load(join("sprite", "ball-violet.png")).convert_alpha(),
            "yellow": pygame.image.load(join("sprite", "ball-yellow.png")).convert_alpha(),
        }

        self.__numbers = [
            pygame.image.load(join("sprite", f"{i}.png")).convert_alpha()
            for i in range(10)
        ]

        self.__level_image = pygame.image.load(join("sprite", "nivel.png")).convert_alpha()
        self.__top_menu = pygame.image.load(join("sprite", "menu-superior.png")).convert_alpha()
        self.__life = pygame.image.load(join("sprite", "life.png")).convert_alpha()
        self.__background = pygame.image.load(join("sprite", "background.png")).convert_alpha()

    def get_ball(self, color): return self.__ball_images[color]
    def get_numbers(self): return self.__numbers
    def get_level_image(self): return self.__level_image
    def get_top_menu(self): return self.__top_menu
    def get_life(self): return self.__life
    def get_background(self): return self.__background