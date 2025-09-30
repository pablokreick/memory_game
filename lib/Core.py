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
    __ball_speed = None

    def __init__(self):
        self.__level = 1
        self.__balls_quantity = 2
        self.__pattern = []
        self.__balls = []
        self.__ball_speed = Var.INITIAL_BALL_SPEED
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

    def get_ball_images(self):
        return self.__ball_images

    def get_level(self):
        return self.__level

    def get_balls_quantity(self):
        return self.__balls_quantity

    def get_pattern(self):
        return self.__pattern

    def get_balls(self):
        return self.__balls

    def get_ball_speed(self):
        return self.__ball_speed

    def set_ball_images(self, ball_images):
        self.__ball_images = ball_images

    def set_level(self, level):
        self.__level = level

    def set_balls_quantity(self, balls_quantity):
        self.__balls_quantity = balls_quantity

    def set_pattern(self, pattern):
        self.__pattern = pattern

    def set_balls(self, balls):
        self.__balls = balls

    def set_ball_speed(self, speed):
        self.__ball_speed = speed

    ball_images = property(get_ball_images, set_ball_images)
    level = property(get_level, set_level)
    balls_quantity = property(get_balls_quantity, set_balls_quantity)
    pattern = property(get_pattern, set_pattern)
    balls = property(get_balls, set_balls)
    ball_speed = property(get_ball_speed, set_ball_speed)

    def check_collisions(self, objetive, sprite):
        return pygame.sprite.spritecollide(
            objetive, sprite, False, pygame.sprite.collide_mask
        )

    def create_ball(self, speed, color_name, sprites):
        surf = self.ball_images[color_name]
        ball = Ball(surf, speed, color_name, sprites)
        return ball

    def make_pattern(self, sprites):
        self.pattern = []
        self.balls = []
        for _ in range(self.balls_quantity):
            color = random.choice(list(self.ball_images.keys()))
            self.pattern.append(color)
        for color in self.pattern:
            self.balls.append(self.create_ball(self.ball_speed, color, sprites))

    def set_balls_in_position(self):
        balls_sprites = pygame.sprite.Group()
        for ball in self.balls:
            ball.set_position(
                (
                    random.randint(0, Var.WIDTH - ball.image.get_width()),
                    random.randint(0, Var.HEIGHT // 4),
                )
            )
            while pygame.sprite.spritecollide(ball, balls_sprites, False):
                ball.set_position(
                    (
                        random.randint(0, Var.WIDTH - ball.image.get_width()),
                        random.randint(0, Var.HEIGHT // 4),
                    )
                )
            balls_sprites.add(ball)


class Player(pygame.sprite.Sprite):
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
        self.__image = pygame.image.load(join("sprite", "car.png")).convert_alpha()
        self.__rect = self.__image.get_rect(
            center=(Var.WIDTH // 2, Var.HEIGHT - self.__image.get_height())
        )
        self.__direction = pygame.math.Vector2(0, 0)
        self.__speed = Var.CAR_SPEED
        self.__colors = []
        self.__lives = 3
        self.__score = 0
        self.__life_image = pygame.image.load(
            join("sprite", "life.png")
        ).convert_alpha()

    def get_image(self):
        return self.__image

    def get_rect(self):
        return self.__rect

    def get_direction(self):
        return self.__direction

    def get_speed(self):
        return self.__speed

    def get_colors(self):
        return self.__colors

    def get_lives(self):
        return self.__lives

    def get_life_image(self):
        return self.__life_image

    def get_score(self):
        return self.__score

    def set_image(self, image):
        self.__image = image

    def set_rect(self, rect):
        self.__rect = rect

    def set_direction(self, direction):
        self.__direction = direction

    def set_speed(self, speed):
        self.__speed = speed

    def set_colors(self, colors):
        self.__colors = colors

    def set_lives(self, lives):
        self.__lives = lives

    def set_life_image(self, life_image):
        self.__life_image = life_image

    def set_score(self, score):
        if score <= 0:
            self.__score = 0
        else:
            self.__score = score

    image = property(get_image, set_image)
    rect = property(get_rect, set_rect)
    direction = property(get_direction, set_direction)
    speed = property(get_speed, set_speed)
    colors = property(get_colors, set_colors)
    lives = property(get_lives, set_lives)
    life_image = property(get_life_image, set_life_image)
    score = property(get_score, set_score)

    def has_no_lives(self):
        return self.lives == 0

    def has_completed_pattern(self, game):
        return len(self.colors) >= len(game.pattern)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (
            keys[pygame.K_a] or keys[pygame.K_LEFT]
        )
        self.direction.y = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (
            keys[pygame.K_w] or keys[pygame.K_UP]
        )
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        self.rect.center += self.direction * self.speed * dt

        if self.rect.bottom >= Var.HEIGHT:
            self.rect.bottom = Var.HEIGHT
        if self.rect.top <= Var.TOP_MARGIN:
            self.rect.top = Var.TOP_MARGIN
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= Var.WIDTH:
            self.rect.right = Var.WIDTH


class Ball(pygame.sprite.Sprite):
    __image = None
    __rect = None
    __direction = None
    __speed = None
    __color = None
    __move = None

    def __init__(self, surf, speed, color, groups):
        super().__init__(groups)
        self.__image = surf
        self.__rect = self.__image.get_rect()
        self.__direction = pygame.math.Vector2(random.choice([-1, 1]), 1)
        self.__speed = speed
        self.__color = color
        self.__move = False

    def get_image(self):
        return self.__image

    def get_rect(self):
        return self.__rect

    def get_direction(self):
        return self.__direction

    def get_speed(self):
        return self.__speed

    def get_color(self):
        return self.__color

    def get_move(self):
        return self.__move

    def set_image(self, image):
        self.__image = image

    def set_rect(self, rect):
        self.__rect = rect

    def set_direction(self, direction):
        self.__direction = direction

    def set_speed(self, speed):
        self.__speed = speed

    def set_color(self, color):
        self.__color = color

    def set_move(self, move):
        self.__move = move

    image = property(get_image, set_image)
    rect = property(get_rect, set_rect)
    direction = property(get_direction, set_direction)
    speed = property(get_speed, set_speed)
    color = property(get_color, set_color)
    move = property(get_move, set_move)

    def is_color(self, color):
        return self.color == color

    def set_position(self, pos):
        self.rect.center = pos

    def move_to_random_position(self):
        self.rect.center = (
            random.randint(0, Var.WIDTH),
            random.randint(0, Var.HEIGHT),
        )

    def update(self, dt):
        if self.move:
            self.rect.center += self.direction * self.speed * dt

            if self.rect.bottom >= Var.HEIGHT:
                self.direction.y *= -1
                self.rect.bottom = Var.HEIGHT
            if self.rect.top <= Var.TOP_MARGIN:
                self.direction.y *= -1
                self.rect.top = Var.TOP_MARGIN
            if self.rect.left <= 0:
                self.direction.x *= -1
                self.rect.left = 0
            if self.rect.right >= Var.WIDTH:
                self.direction.x *= -1
                self.rect.right = Var.WIDTH


class Button(pygame.sprite.Sprite):
    __image = None
    __rect = None

    def __init__(self, image, x, y):
        super().__init__()
        self.__image = pygame.image.load(join("sprite", image)).convert_alpha()
        self.__rect = self.__image.get_rect(center=(x, y))

    def get_image(self):
        return self.__image

    def get_rect(self):
        return self.__rect

    def set_image(self, image):
        self.__image = image

    def set_rect(self, rect):
        self.__rect = rect

    image = property(get_image, set_image)
    rect = property(get_rect, set_rect)
