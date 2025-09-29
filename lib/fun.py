import pygame
import math
import lib.Var as Var
import lib.Color as Color
import lib.Core as c
from os.path import join


def transform_int_to_list(score):
    return list(str(score))


def menu(display):
    repeat = True
    play = False
    background = pygame.image.load(
        join("sprite", "main.png")
    ).convert_alpha()

    # Botones
    btn_play = c.Button("btn_play.png", Var.WIDTH // 2, Var.HEIGHT // 2)
    btn_quit = c.Button("btn_quit.png", Var.WIDTH // 2, Var.HEIGHT // 2 + 120)
    lista = pygame.sprite.Group(btn_play, btn_quit)

    while repeat:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                repeat = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.get_rect().collidepoint(event.pos):
                    play = True
                    repeat = False
                if btn_quit.get_rect().collidepoint(event.pos):
                    play = False
                    repeat = False

        display.fill(Color.GREEN)
        display.blit(background, (0, 0))
        lista.draw(display)
        pygame.display.update()

    return play


def final_menu(display, winner):
    repeat = True
    play = False
    background = pygame.image.load(
        join("sprite", "winner.png" if winner else "looser.png")
    ).convert_alpha()

    btn_play = c.Button(
        "btn_again_winner.png" if winner else "btn_again.png",
        Var.WIDTH // 2,
        Var.HEIGHT // 2,
    )
    btn_quit = c.Button("btn_quit.png", Var.WIDTH // 2, Var.HEIGHT // 2 + 120)
    lista = pygame.sprite.Group(btn_play, btn_quit)

    while repeat:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                repeat = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.get_rect().collidepoint(event.pos):
                    play = True
                    repeat = False
                if btn_quit.get_rect().collidepoint(event.pos):
                    play = False
                    repeat = False

        display.blit(background, (0, 0))
        lista.draw(display)
        pygame.display.update()

    return play


def pattern_menu(display, game):
    play = True
    time = pygame.time.get_ticks()
    repeat = True
    background = pygame.image.load(join("sprite", "pattern.png")).convert_alpha()
    numbers = [
        pygame.image.load(join("sprite", f"{i}.png")).convert_alpha()
        for i in range(1, 4)
    ]

    # 👇 ahora usamos HudBall en vez de las bolas reales del juego
    hud_balls = [c.HudBall(ball.get_image(), ball.get_color()) for ball in game.get_balls()]

    while repeat:
        current_time = pygame.time.get_ticks()
        seconds = (current_time - time) // 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                repeat = False
                play = False

        if seconds >= Var.COUNTDOWN:
            repeat = False
        else:
            number_surf = numbers[2 - int(seconds)]
            number_rect = number_surf.get_rect(
                center=(Var.WIDTH // 2, Var.HEIGHT // 2 + 150)
            )
            spacing = 50
            total_width = len(hud_balls) * spacing
            start_x = Var.WIDTH // 2 - total_width // 2
            y = Var.HEIGHT // 2 - 50

            display.blit(background, (0, 0))
            for i, hud_ball in enumerate(hud_balls):
                x = start_x + i * spacing
                hud_ball.set_position((x, y))
                hud_ball.draw(display)

            display.blit(number_surf, number_rect)
            pygame.display.update()

    return play


def menu_congratulations(display):
    repeat = True
    play = False
    background = pygame.image.load(join("sprite", "final.png")).convert_alpha()

    btn_play = c.Button("btn_final.png", Var.WIDTH // 2 + 150, Var.HEIGHT // 2)
    btn_quit = c.Button(
        "btn_quit_final.png", Var.WIDTH // 2 + 150, Var.HEIGHT // 2 + 120
    )
    lista = pygame.sprite.Group(btn_play, btn_quit)

    while repeat:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                repeat = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.rect.collidepoint(event.pos):
                    play = True
                    repeat = False
                if btn_quit.rect.collidepoint(event.pos):
                    play = False
                    repeat = False

        display.fill(Color.GREEN)
        display.blit(background, (0, 0))
        lista.draw(display)
        pygame.display.update()

    return play