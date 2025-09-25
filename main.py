import pygame
import sys
from os.path import join
import random
import lib.constants as constant

import lib.classes as c
import lib.fun as f

pygame.init()

# Configuración
display = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))
pygame.display.set_caption("Memory")

# Fuentes

# Reloj
clock = pygame.time.Clock()


# Sonidos
sound_good = pygame.mixer.Sound(join("sounds", "bubble.mp3"))
sound_wrong = pygame.mixer.Sound(join("sounds", "wrong.mp3"))
sound_win = pygame.mixer.Sound(join("sounds", "win.mp3"))
sound_fail = pygame.mixer.Sound(join("sounds", "fail.mp3"))


music = pygame.mixer.music.load(join("sounds", "music.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)


# Variables del juego
balls_quantity = 2
level = 1


# ---------------------------------- IMPORTS --------------------------------- #
# ---------------------------------- CLASSES --------------------------------- #
class Player(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "car.png")).convert_alpha()
        self.rect = self.image.get_rect(
            center=(constant.WIDTH // 2, constant.HEIGHT // 2)
        )
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 300
        self.colors = []
        self.lifes = 3

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        self.rect.center += self.direction * self.speed * dt
        if self.rect.bottom >= constant.HEIGHT:
            self.direction.y *= -1
            self.rect.bottom = constant.HEIGHT
        if self.rect.top <= 60:
            self.direction.y *= -1
            self.rect.top = 60
        if self.rect.left <= 0:
            self.direction.x *= -1
            self.rect.left = 0
        if self.rect.right >= constant.WIDTH:
            self.direction.x *= -1
            self.rect.right = constant.WIDTH


class Ball(pygame.sprite.Sprite):

    def __init__(self, surf, color, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), 1)
        self.speed = 100
        self.color = color

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.bottom >= constant.HEIGHT:
            self.direction.y *= -1
            self.rect.bottom = constant.HEIGHT
        if self.rect.top <= 60:
            self.direction.y *= -1
            self.rect.top = 60
        if self.rect.left <= 0:
            self.direction.x *= -1
            self.rect.left = 0
        if self.rect.right >= constant.WIDTH:
            self.direction.x *= -1
            self.rect.right = constant.WIDTH


# ---------------------------------- SPRITES --------------------------------- #
player_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
ball_sprites = pygame.sprite.Group()

ball_images = {
    "blue": pygame.image.load(join("images", "ball-blue.png")).convert_alpha(),
    "lightblue": pygame.image.load(
        join("images", "ball-lightblue.png")
    ).convert_alpha(),
    "green": pygame.image.load(join("images", "ball-green.png")).convert_alpha(),
    "red": pygame.image.load(join("images", "ball-red.png")).convert_alpha(),
    "violet": pygame.image.load(join("images", "ball-violet.png")).convert_alpha(),
    "yellow": pygame.image.load(join("images", "ball-yellow.png")).convert_alpha(),
}
top_menu = pygame.image.load(join("images", "menu-superior.png"))
top_menu_rect = top_menu.get_rect(
    center=(constant.WIDTH // 2, top_menu.get_height() // 2)
)
life = pygame.image.load(join("images", "life.png")).convert_alpha()
balls = []
pattern = []
background = pygame.image.load(join("images", "background.jpg"))
background_rect = background.get_rect(topleft=(0, 0))
looser_background = pygame.image.load(join("images", "looser.png"))
winner_background = pygame.image.load(join("images", "winner.png"))


def choose_ball():
    color_name = random.choice(list(ball_images.keys()))
    surf = ball_images[color_name]
    x = random.randint(0, constant.WIDTH - surf.get_width())
    y = random.randint(0, constant.HEIGHT - surf.get_height())
    ball = Ball(surf, color_name, (x, y), (all_sprites, ball_sprites))
    return ball


for i in range(balls_quantity):
    ball = choose_ball()
    balls.append(ball)
    pattern.append(ball.color)

for i in range(level):
    ball = choose_ball()
    balls.append(ball)
print(pattern)
player = Player((all_sprites, player_sprite))


def show_lifes():
    for i in range(player.lifes):
        display.blit(life, (30 + i * 48, 10))


def show_balls(balls):
    for i, ball in enumerate(balls):
        surf = ball_images[ball.color]
        rect = surf.get_rect(topleft=(200 + i * 50, 7))
        display.blit(surf, rect)


play = f.menu(display, clock)

while play:
    dt = clock.tick(30) / 1000
    display.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    collided_ball = pygame.sprite.spritecollide(
        player, ball_sprites, True, pygame.sprite.collide_mask
    )
    if collided_ball:
        balls.append(choose_ball())
        for ball in collided_ball:
            index = len(player.colors)
            if ball.color == pattern[index]:
                player.colors.append(ball)
                print(f"Bien")
                sound_good.play()
                if len(player.colors) >= len(pattern):
                    level += 1
                    sound_win.play()
                    f.final_menu(display, clock, True)

            else:
                print("mal")
                sound_wrong.play()
                player.lifes -= 1
                if player.lifes == 0:
                    print("Perdiste")
                    sound_fail.play()
                    f.final_menu(display, clock, False)
    all_sprites.update(dt)
    display.blit(background, background_rect)
    all_sprites.draw(display)
    display.blit(top_menu, top_menu_rect)
    show_balls(player.colors)
    show_lifes()
    pygame.display.update()
pygame.quit()
sys.exit()
