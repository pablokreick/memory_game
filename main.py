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
    level = 1
    balls_quantity = 2
    # Grupos de sprites
    player_sprite = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    ball_sprites = pygame.sprite.Group()

    # Imágenes (desde carpeta sprite/)
    ball_images = {
        "blue": pygame.image.load(join("sprite", "ball-blue.png")).convert_alpha(),
        "lightblue": pygame.image.load(
            join("sprite", "ball-lightblue.png")
        ).convert_alpha(),
        "green": pygame.image.load(join("sprite", "ball-green.png")).convert_alpha(),
        "red": pygame.image.load(join("sprite", "ball-red.png")).convert_alpha(),
        "violet": pygame.image.load(join("sprite", "ball-violet.png")).convert_alpha(),
        "yellow": pygame.image.load(join("sprite", "ball-yellow.png")).convert_alpha(),
    }

    top_menu = pygame.image.load(join("sprite", "menu-superior.png"))
    top_menu_rect = top_menu.get_rect(
        center=(Var.WIDTH // 2, top_menu.get_height() // 2)
    )
    life = pygame.image.load(join("sprite", "life.png")).convert_alpha()
    background = pygame.image.load(join("sprite", "background.jpg"))
    background_rect = background.get_rect(topleft=(0, 0))

    # Función auxiliar para elegir bola
    def create_ball(color_name):
        surf = ball_images[color_name]
        x = random.randint(0, Var.WIDTH - surf.get_width())
        y = random.randint(0, Var.HEIGHT // 4)
        ball = Ball(surf, color_name, (x, y), (all_sprites, ball_sprites))
        return ball

    # Crear jugador
    player = Player((all_sprites, player_sprite))

    # Funciones auxiliares para HUD
    # Muestra las vidas
    def show_lifes():
        for i in range(player.get_lifes()):
            display.blit(life, (30 + i * 48, 10))

    # Muestra en pantalla las bolas elegidas
    def show_balls(balls):
        for i, ball in enumerate(balls):
            surf = ball_images[ball.get_color()]
            rect = surf.get_rect(topleft=(200 + i * 50, 7))
            display.blit(surf, rect)

    # Menú inicial
    play = f.menu(display)

    # Bucle principal del juego
    while play:
        all_sprites.empty()
        ball_sprites.empty()
        player_sprite.empty()

        balls = []
        pattern = []
        player.reset_colors()
        player.reset_lifes()
        player = Player((all_sprites, player_sprite))
        player.set_rect_pos((Var.WIDTH // 2, Var.HEIGHT - player.get_image_height()))
        # Crear bolas iniciales y patrón
        for _ in range(balls_quantity):
            color = random.choice(list(ball_images.keys()))
            pattern.append(color)
            balls.append(create_ball(color))

        print(pattern)

        in_game = True
        while in_game and play:
            # clock para no tener problemas de velocidad
            dt = clock.tick(Var.FPS) / 1000
            display.fill(Color.BLACK)
            # Evento para salir
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    in_game = False

            # Detecta colisiones entre las bolas y el jugador
            collided_ball = pygame.sprite.spritecollide(
                player, ball_sprites, False, pygame.sprite.collide_mask
            )
            # Si alguna colisiona, se determina si pierde o no
            if collided_ball:
                # Podés llegar a agarrar varias simultáneamente, por eso el for
                for ball in collided_ball:
                    # Obtiene el índice final del array del jugador que coincide con el índice que tiene que consultar del patrón
                    # Así no agrega la bola si no es correcta
                    index = len(player.get_colors())
                    # Si la bola es del color que sigue en el patrón
                    if ball.get_color() == pattern[index]:
                        # Ahora agrega la bola al array del jugador
                        player.add_color(ball)
                        sound_good.play()
                        all_sprites.remove(ball)
                        ball_sprites.remove(ball)
                        # Si ya completó todo el patrón, gana
                        if len(player.get_colors()) >= len(pattern):
                            sound_win.play()
                            # Pone el menú
                            play = f.final_menu(display, True)
                            level += 1
                            balls_quantity += 1
                            Var.BALL_SPEED += 5
                            in_game = False
                    else:
                        # Si la bola no era correcta:
                        ball.rect.center = (
                            random.randint(0, Var.WIDTH),
                            random.randint(0, Var.HEIGHT),
                        )
                        sound_wrong.play()
                        # pierde una vida
                        player.lose_life()
                        # Si llega a cero vidas, pierde
                        if player.get_lifes() == 0:
                            sound_fail.play()
                            # Pone el menú
                            play = f.final_menu(display, False)
                            in_game = False

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
