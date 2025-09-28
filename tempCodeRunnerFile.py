import pygame
import sys
from os.path import join
import random
from lib.Core import Player, Ball, Game, Interface

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
    # pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)

    # Variables del juego
    game = Game()
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

    numbers = [
        pygame.image.load(join("sprite", f"{i}.png")).convert_alpha() for i in range(10)
    ]

    level_image = pygame.image.load(join("sprite", "nivel.png")).convert_alpha()
    level_rect = level_image.get_rect(topright=(Var.WIDTH - 100, 70))

    top_menu = pygame.image.load(join("sprite", "menu-superior.png"))
    top_menu_rect = top_menu.get_rect(
        center=(Var.WIDTH // 2, top_menu.get_height() // 2)
    )
    background = pygame.image.load(join("sprite", "background.png"))
    background_rect = background.get_rect(topleft=(0, 0))

    interface = Interface(display)
    play = f.menu(interface.get_display())

    while play:
        interface.reset_sprites((all_sprites, ball_sprites, player_sprite))
        level_number_image = numbers[game.get_level()]
        level_number_rect = level_number_image.get_rect(
            topleft=(Var.WIDTH - level_number_image.get_width() - 20, 70)
        )
        player = Player((all_sprites, player_sprite))
        player.reset_colors()
        player.reset_lifes()
        game.reset_pattern()
        game.make_pattern((all_sprites, ball_sprites))
        play = f.pattern_menu(interface.get_display(), game.get_balls())
        player.set_in_position((Var.WIDTH // 2, Var.HEIGHT - player.get_image_height()))
        game.set_balls_in_position()
        print(game.get_pattern())

        in_game = True
        while in_game and play:
            dt = clock.tick(Var.FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    in_game = False

            # Detecta colisiones entre las bolas y el jugador
            collided_ball = pygame.sprite.spritecollide(
                player, ball_sprites, False, pygame.sprite.collide_mask
            )

            if collided_ball:
                for ball in collided_ball:
                    index = len(player.get_colors())
                    # Si la bola es del color que sigue en el patrón
                    if ball.get_color() == game.get_pattern()[index]:
                        # Ahora agrega la bola al array del jugador
                        player.add_color(ball)
                        sound_good.play()
                        all_sprites.remove(ball)
                        ball_sprites.remove(ball)
                        # Si ya completó todo el patrón, gana
                        if len(player.get_colors()) >= len(game.get_pattern()):
                            sound_win.play()
                            play = f.final_menu(interface.get_display(), True)
                            game.increment_level()
                            game.increment_balls_quantity()
                            Var.BALL_SPEED += 5
                            in_game = False
                    else:
                        ball.move_to_random_position()
                        sound_wrong.play()
                        player.lose_life()
                        # Si llega a cero vidas, pierde
                        if player.get_lives() == 0:
                            sound_fail.play()
                            # Pone el menú
                            play = f.final_menu(interface.get_display(), False)
                            in_game = False
                            game.reset_balls_quantity()
                            game.reset_level()

            # Actualizar y dibujar
            all_sprites.update(dt)
            interface.show_background(background, background_rect)
            all_sprites.draw(interface.get_display())
            interface.show_top_menu(top_menu, top_menu_rect)
            interface.show_balls(player.get_colors())
            interface.show_lives(player)
            interface.show_level(
                level_image, level_rect, level_number_image, level_number_rect
            )
            pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
