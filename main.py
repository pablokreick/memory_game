import pygame
import sys
from os.path import join
import random
from lib.Core import Player, Ball

# Nuestros módulos
import lib.Var as Var
import lib.Color as Color
import lib.fun as f


def main():
    pygame.init()

    # Configuración de la ventana
    display = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
    pygame.display.set_caption(Var.TITLE)

    clock = pygame.time.Clock()

    # Sonidos
    sound_good = pygame.mixer.Sound(join("sounds", "bubble.mp3"))
    sound_wrong = pygame.mixer.Sound(join("sounds", "wrong.mp3"))
    sound_win = pygame.mixer.Sound(join("sounds", "win.mp3"))
    sound_fail = pygame.mixer.Sound(join("sounds", "fail.mp3"))

    pygame.mixer.music.load(join("sounds", "music.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)

    # Variables del juego
    balls_quantity = 2
    level = 1
    balls = []
    pattern = []

    # Grupos de sprites
    player_sprite = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    ball_sprites = pygame.sprite.Group()

    # Imágenes (desde carpeta sprite/)
    ball_images = {
        "blue": pygame.image.load(join("sprite", "ball-blue.png")).convert_alpha(),
        "lightblue": pygame.image.load(join("sprite", "ball-lightblue.png")).convert_alpha(),
        "green": pygame.image.load(join("sprite", "ball-green.png")).convert_alpha(),
        "red": pygame.image.load(join("sprite", "ball-red.png")).convert_alpha(),
        "violet": pygame.image.load(join("sprite", "ball-violet.png")).convert_alpha(),
        "yellow": pygame.image.load(join("sprite", "ball-yellow.png")).convert_alpha(),
    }
    top_menu = pygame.image.load(join("sprite", "menu-superior.png"))
    top_menu_rect = top_menu.get_rect(center=(Var.WIDTH // 2, top_menu.get_height() // 2))
    life = pygame.image.load(join("sprite", "life.png")).convert_alpha()
    background = pygame.image.load(join("sprite", "background.jpg"))
    background_rect = background.get_rect(topleft=(0, 0))

    # Función auxiliar para elegir bola
    def choose_ball():
        color_name = random.choice(list(ball_images.keys()))
        surf = ball_images[color_name]
        x = random.randint(0, Var.WIDTH - surf.get_width())
        y = random.randint(0, Var.HEIGHT - surf.get_height())
        ball = Ball(surf, color_name, (x, y), (all_sprites, ball_sprites))
        return ball

    # Crear bolas iniciales y patrón
    for _ in range(balls_quantity):
        ball = choose_ball()
        balls.append(ball)
        pattern.append(ball.get_color())

    for _ in range(level):
        ball = choose_ball()
        balls.append(ball)

    print(pattern)

    # Crear jugador
    player = Player((all_sprites, player_sprite))

    # Funciones auxiliares para HUD
    def show_lifes():
        for i in range(player.get_lifes()):
            display.blit(life, (30 + i * 48, 10))

    def show_balls(balls):
        for i, ball in enumerate(balls):
            surf = ball_images[ball.get_color()]
            rect = surf.get_rect(topleft=(200 + i * 50, 7))
            display.blit(surf, rect)

    # Menú inicial
    play = f.menu(display, clock)

    # Bucle principal del juego
    while play:
        dt = clock.tick(Var.FPS) / 1000
        display.fill(Color.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

        collided_ball = pygame.sprite.spritecollide(
            player, ball_sprites, True, pygame.sprite.collide_mask
        )
        if collided_ball:
            balls.append(choose_ball())
            for ball in collided_ball:
                index = len(player.get_colors())
                if ball.get_color() == pattern[index]:
                    player.add_color(ball)
                    print("Bien")
                    sound_good.play()
                    if len(player.get_colors()) >= len(pattern):
                        level += 1
                        sound_win.play()
                        f.final_menu(display, clock, True)
                else:
                    print("Mal")
                    sound_wrong.play()
                    player.lose_life()
                    if player.get_lifes() == 0:
                        print("Perdiste")
                        sound_fail.play()
                        f.final_menu(display, clock, False)

        # Actualizar y dibujar
        all_sprites.update(dt)
        display.blit(background, background_rect)
        all_sprites.draw(display)
        display.blit(top_menu, top_menu_rect)
        show_balls(player.get_colors())
        show_lifes()
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()