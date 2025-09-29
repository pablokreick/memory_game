import pygame
import sys
from os.path import join
from lib.Core import Player, Game, Interface

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

    # Grupos de sprites
    player_sprite = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    ball_sprites = pygame.sprite.Group()

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

    score_image = pygame.image.load(join("sprite", "puntos.png")).convert_alpha()
    score_rect = score_image.get_rect(topleft=(20, 70))

    game = Game()
    interface = Interface(display)
    play = f.menu(display)

    # Crear la superficie de estáticos
    static_surface = pygame.Surface((Var.WIDTH, Var.HEIGHT), pygame.SRCALPHA)

    # Dibujar todo sobre esa superficie solo una vez
    static_surface.blit(background, background_rect)
    static_surface.blit(top_menu, top_menu_rect)
    static_surface.blit(level_image, level_rect)
    player = Player((all_sprites, player_sprite))
    COUNTDOWN_EVENT = pygame.USEREVENT + 1
    # ---------------------------------------------------------------------------- #
    #                              WHILE DEL PROGRAMA                              #
    # ---------------------------------------------------------------------------- #
    while play:
        player.get_colors().clear()
        level_number_image = numbers[game.get_level()]
        level_number_rect = level_number_image.get_rect(
            topleft=(Var.WIDTH - level_number_image.get_width() - 20, 70)
        )
        static_surface.blit(level_number_image, level_number_rect)
        game.make_pattern((all_sprites, ball_sprites))
        play = f.pattern_menu(display, game)
        pygame.time.set_timer(COUNTDOWN_EVENT, 100, False)
        in_game = True
        game.place_elements_in_position(player)
        # ---------------------------------------------------------------------------- #
        #                                WHILE DEL JUEGO                               #
        # ---------------------------------------------------------------------------- #
        while in_game and play:
            dt = clock.tick(Var.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    in_game = False
                elif event.type == COUNTDOWN_EVENT:
                    print("Empieza el juego")
                    # pygame.time.set_timer(COUNTDOWN_EVENT, 0)
                    # game.make_balls((all_sprites, ball_sprites))
                    for ball in game.get_balls():
                        ball.set__move(True)

                    # game.place_elements_in_position(player)
                    # pygame.display.update()
            score_list = f.transform_int_to_list(player.get_score())
            # ---------------------------------------------------------------------------- #
            #                                  COLISIONES                                  #
            # ---------------------------------------------------------------------------- #
            collided_ball = game.check_collisions(player, ball_sprites)

            if collided_ball:
                for ball in collided_ball:
                    index = player.count_colors()
                    if ball.is_color(game.get_pattern_color(index)):
                        player.catch_ball(ball)
                        sound_good.play()
                        ball.kill()
                        player.add_score(10)
                        # level_number_image = numbers[game.get_level()]

                        if player.has_completed_pattern(game):
                            sound_win.play()
                            play = f.final_menu(display, True)
                            if play:
                                game.level_up()
                                in_game = False
                    else:
                        ball.move_to_random_position()
                        sound_wrong.play()
                        player.lose_life()
                        player.add_score(-1)
                        if player.has_no_lives():
                            sound_fail.play()
                            play = f.final_menu(display, False)
                            if play:
                                in_game = False
                                game.restart(ball_sprites)
                                player.restart()

            # ---------------------------------------------------------------------------- #
            #                                DISPLAY SPRITES                               #
            # ---------------------------------------------------------------------------- #
            all_sprites.update(dt)
            display.blit(background, background_rect)
            display.blit(top_menu, top_menu_rect)
            display.blit(background, background_rect)
            display.blit(top_menu, top_menu_rect)
            all_sprites.draw(display)
            interface.show_balls(player.get_colors())
            interface.show_lives(player)
            display.blit(level_image, level_rect)
            display.blit(level_number_image, level_number_rect)
            display.blit(score_image, score_rect)
            for value in score_list:
                display.blit(
                    numbers[int(value)], (300 + score_list.index(value) * 30, 70)
                )
            pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
