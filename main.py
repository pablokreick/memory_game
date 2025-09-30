import pygame
import sys
from os.path import join
from lib.Core import Player, Game

# Nuestros módulos
import lib.Var as Var
import lib.fun as f


def main():
    pygame.init()

    # Configuración de la ventana
    pygame.display.set_caption(Var.TITLE)
    pygame.display.set_icon(pygame.image.load(join("sprite", "car_icon.png")))
    display = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))

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

    instructions_image = pygame.image.load(
        join("sprite", "teclado.png")
    ).convert_alpha()
    instructions_rect = instructions_image.get_rect(
        topleft=((Var.WIDTH - instructions_image.get_width()) // 2, 70)
    )

    game = Game()
    play = f.menu(display)

    surface = pygame.Surface((Var.WIDTH, Var.HEIGHT))

    surface.blit(background, background_rect)
    surface.blit(top_menu, top_menu_rect)
    surface.blit(level_image, level_rect)
    player = Player((all_sprites, player_sprite))

    COUNTDOWN_EVENT = pygame.USEREVENT + 1
    INSTRUCTIONS_EVENT = pygame.USEREVENT + 2

    while play:
        player.colors = []
        level_number_image = numbers[game.level]
        level_number_rect = level_number_image.get_rect(
            topleft=(Var.WIDTH - level_number_image.get_width() - 20, 70)
        )
        surface.blit(level_number_image, level_number_rect)

        game.make_pattern((all_sprites, ball_sprites))
        play = f.pattern_menu(display, game)
        pygame.time.set_timer(COUNTDOWN_EVENT, 100, False)

        in_game = True
        player.rect.center = (Var.WIDTH // 2, Var.HEIGHT - player.image.get_height())
        game.set_balls_in_position()
        show_instructions = False
        if game.level == 1:
            show_instructions = True
            pygame.time.set_timer(INSTRUCTIONS_EVENT, Var.COUNTDOWN * 1000, False)
        while in_game and play:
            dt = clock.tick(Var.FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    in_game = False
                elif event.type == COUNTDOWN_EVENT:
                    for ball in game.balls:
                        ball.move = True
                elif event.type == INSTRUCTIONS_EVENT:
                    show_instructions = False
            score_list = f.transform_int_to_list(player.score)

            collided_ball = game.check_collisions(player, ball_sprites)

            if collided_ball:
                for ball in collided_ball:
                    index = len(player.colors)
                    if ball.is_color(game.pattern[index]):
                        player.colors.append(ball)
                        sound_good.play()
                        ball.kill()
                        player.score = player.score + 10
                        if player.has_completed_pattern(game):
                            sound_win.play()
                            if game.level >= 9:
                                play = f.menu_congratulations(display)
                                if play:
                                    in_game = False
                                    game.level = 1
                                    game.ball_speed = Var.INITIAL_BALL_SPEED
                                    game.balls_quantity = Var.INITIAL_BALLS
                                    for ball in ball_sprites:
                                        ball.kill()
                                    player.lives = 3
                                    player.score = 0
                                    player.colors = []
                            else:
                                play = f.final_menu(display, True)
                                if play:
                                    game.level = game.level + 1
                                    game.balls_quantity = game.balls_quantity + 1
                                    game.ball_speed += 5
                                    in_game = False
                    else:
                        ball.move_to_random_position()
                        sound_wrong.play()
                        player.lives -= 1
                        player.score = player.score - 1
                        if player.has_no_lives():
                            sound_fail.play()
                            play = f.final_menu(display, False)
                            if play:
                                in_game = False
                                game.level = 1
                                game.ball_speed = Var.INITIAL_BALL_SPEED
                                game.balls_quantity = Var.INITIAL_BALLS
                                for ball in ball_sprites:
                                    ball.kill()
                                player.lives = 3
                                player.score = 0
                                player.colors = []

            all_sprites.update(dt)
            display.blit(background, background_rect)
            display.blit(top_menu, top_menu_rect)
            display.blit(background, background_rect)
            display.blit(top_menu, top_menu_rect)
            all_sprites.draw(display)
            for i, ball in enumerate(player.colors):
                ball.set_position((200 + i * 50, 30))
                display.blit(ball.image, ball.rect)
            for i in range(player.lives):
                display.blit(player.life_image, (30 + i * 48, 10))
            display.blit(level_image, level_rect)
            display.blit(level_number_image, level_number_rect)
            display.blit(score_image, score_rect)
            for i, value in enumerate(score_list):
                display.blit(numbers[int(value)], (300 + i * 35, 70))
            if show_instructions:
                display.blit(instructions_image, instructions_rect)

            pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
