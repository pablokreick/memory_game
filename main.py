import pygame
import sys
from os.path import join
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

    game = Game()
    interface = Interface(display)
    play = f.menu(display)

    # ---------------------------------------------------------------------------- #
    #                              WHILE DEL PROGRAMA                              #
    # ---------------------------------------------------------------------------- #
    while play:
        interface.reset_sprites((all_sprites, ball_sprites, player_sprite))
        level_number_image = numbers[game.get_level()]
        level_number_rect = level_number_image.get_rect(
            topleft=(Var.WIDTH - level_number_image.get_width() - 20, 70)
        )
        player = Player((all_sprites, player_sprite))
        game.make_pattern((all_sprites, ball_sprites))
        play = f.pattern_menu(display, game.get_balls())
        player.spawn_to_bottom()
        game.set_balls_in_position()
        in_game = True
        # ---------------------------------------------------------------------------- #
        #                                WHILE DEL JUEGO                               #
        # ---------------------------------------------------------------------------- #
        while in_game and play:
            dt = clock.tick(Var.FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    in_game = False

            # ---------------------------------------------------------------------------- #
            #                                  COLISIONES                                  #
            # ---------------------------------------------------------------------------- #
            collided_ball = pygame.sprite.spritecollide(
                player, ball_sprites, False, pygame.sprite.collide_mask
            )

            if collided_ball:
                for ball in collided_ball:
                    index = player.count_colors()
                    if ball.is_color(game.get_pattern_color(index)):
                        player.catch_ball(ball)
                        sound_good.play()
                        interface.remove_from_sprites(ball, (all_sprites, ball_sprites))

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
                        if player.has_no_lives():
                            sound_fail.play()
                            play = f.final_menu(display, False)
                            if play:
                                in_game = False
                                game.restart()

            # ---------------------------------------------------------------------------- #
            #                                DISPLAY SPRITES                               #
            # ---------------------------------------------------------------------------- #
            all_sprites.update(dt)
            interface.show_background(background, background_rect)
            all_sprites.draw(display)
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
