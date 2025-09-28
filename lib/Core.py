import pygame
import random
from os.path import join
import lib.Var as Var


class Game(pygame.sprite.Sprite):
    __ball_images = None
    __level = None
    __balls_quantity = None
    __pattern = None
    __balls = None

    def __init__(self):
        self.__level = 1
        self.__balls_quantity = 2
        self.__pattern = []
        self.__balls = []
        self.__ball_images = {
            "blue": pygame.image.load(join("sprite", "ball-blue.png")).convert_alpha(),
            "lightblue": pygame.image.load(
                join("sprite", "ball-lightblue.png")
            ).convert_alpha(),
            "green": pygame.image.load(
                join("sprite", "ball-green.png")
            ).convert_alpha(),
            "red": pygame.image.load(join("sprite", "ball-red.png")).convert_alpha(),
            "violet": pygame.image.load(
                join("sprite", "ball-violet.png")
            ).convert_alpha(),
            "yellow": pygame.image.load(
                join("sprite", "ball-yellow.png")
            ).convert_alpha(),
        }

    def get_level(self):
        return self.__level

    def set_level(self, level):
        self.__level = level

    def increment_level(self):
        self.__level += 1

    def reset_level(self):
        self.__level = 1

    def restart(self, balls):
        self.reset_level()
        self.reset_balls_quantity()
        Var.BALL_SPEED = 100
        for ball in balls:
            ball.kill()

    def reset_pattern(self):
        self.__pattern = []

    def level_up(self):
        self.increment_level()
        self.increment_balls_quantity()
        Var.BALL_SPEED += 5

    def get_pattern_color(self, index):
        return self.__pattern[index]

    def count_pattern_colors(self):
        return len(self.__pattern)

    def get_balls_quantity(self):
        return self.__balls_quantity

    def increment_balls_quantity(self):
        self.__balls_quantity += 1

    def reset_balls_quantity(self):
        self.__balls_quantity = 2

    def set_balls_quantity(self, quantity):
        self.__balls_quantity = quantity

    def get_pattern(self):
        return self.__pattern

    def get_balls(self):
        return self.__balls

    def check_collisions(self, objetive, sprite):
        return pygame.sprite.spritecollide(
            objetive, sprite, False, pygame.sprite.collide_mask
        )

    def add_to_pattern(self, color):
        self.__pattern.append(color)

    def place_elements_in_position(self, player):
        player.spawn_to_bottom()
        self.set_balls_in_position()

    def get__balls_images(self):
        return self.get__balls_images

    def create_ball(self, color_name, sprites):
        surf = self.__ball_images[color_name]
        # x = random.randint(0, Var.WIDTH - surf.get_width())
        # y = random.randint(0, Var.HEIGHT // 4)
        # ball = Ball(surf, color_name, (x, y), sprites)
        ball = Ball(surf, color_name, sprites)
        return ball

    def make_pattern(self, sprites):
        self.__pattern = []
        self.__balls = []
        for _ in range(self.get_balls_quantity()):
            color = random.choice(list(self.__ball_images.keys()))
            self.__pattern.append(color)
        for color in self.__pattern:
            self.__balls.append(self.create_ball(color, sprites))

    def set_balls_in_position(self):
        for ball in self.__balls:
            ball.set_position(
                (
                    random.randint(0, Var.WIDTH - ball.get_image().get_width()),
                    random.randint(0, Var.HEIGHT // 4),
                )
            )


class Interface:
    __display = None

    def __init__(self, display):
        self.__display = display

    def get_display(self):
        return self.__display

    def reset_sprites(self, sprites):
        for sprite in sprites:
            sprite.empty()

    def remove_from_sprites(self, object, sprites):
        for sprite in sprites:
            sprite.remove(object)

    def show_lives(self, player):
        for i in range(player.get_lives()):
            self.__display.blit(player.get_life_image(), (30 + i * 48, 10))

    def show_balls(self, balls):
        for i, ball in enumerate(balls):
            ball.set_position((200 + i * 50, 30))
            self.__display.blit(ball.get_image(), ball.get_rect())


class Player(pygame.sprite.Sprite):
    # Atributos privados declarados fuera del constructor
    __image = None
    __rect = None
    __direction = None
    __speed = None
    __colors = None
    __lives = None
    __life_image = None
    __score = None

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
        self.__lives = 3
        self.__score = 0
        self.__life_image = pygame.image.load(
            join("sprite", "life.png")
        ).convert_alpha()

    # Métodos de acceso y modificación
    def get_image(self):
        return self.__image

    def get_score(self):
        return self.__score

    def add_score(self, points):
        self.__score += points
        if self.__score < 0:
            self.__score = 0

    def restart(self):
        self.__score = 0
        self.__colors = []
        self.__lives = 3

    def get_image_height(self):
        return self.__image.get_height()

    def get_rect(self):
        return self.__rect

    def has_no_lives(self):
        return self.get_lives() == 0

    def count_colors(self):
        return len(self.__colors)

    def spawn_to_bottom(self):
        self.__rect.center = (Var.WIDTH // 2, Var.HEIGHT - self.__image.get_height())

    def get_colors(self):
        return self.__colors

    def catch_ball(self, ball):
        self.__colors.append(ball)

    def has_completed_pattern(self, game):
        return self.count_colors() >= game.count_pattern_colors()

    def get_lives(self):
        return self.__lives

    def lose_life(self):
        self.__lives -= 1

    def get_life_image(self):
        return self.__life_image

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

    def __init__(self, surf, color, groups):
        super().__init__(groups)
        self.__image = surf
        self.__rect = self.__image.get_rect()
        self.__direction = pygame.math.Vector2(random.choice([-1, 1]), 1)
        self.__speed = Var.BALL_SPEED
        self.__color = color

    # Métodos de acceso
    def get_image(self):
        return self.__image

    def is_color(self, color):
        return self.__color == color

    def get_rect(self):
        return self.__rect

    def get_color(self):
        return self.__color

    def set_position(self, pos):
        self.__rect.center = pos

    def move_to_random_position(self):
        self.__rect.center = (
            random.randint(0, Var.WIDTH),
            random.randint(0, Var.HEIGHT),
        )

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
