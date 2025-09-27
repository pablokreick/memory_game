import pygame
import lib.Var as Var
import lib.Color as Color
import lib.Core as c
from os.path import join


def menu(display):
    repeat = True
    play = False
    background = pygame.image.load(
        join("sprite", "main.png")
    ).convert_alpha()  # 👈 cambiado a sprite/

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

        # Dibujo
        display.fill(Color.GREEN)
        display.blit(background, (0, 0))
        lista.draw(display)
        pygame.display.update()

    return play


def final_menu(display, winner):
    repeat = True
    play = False
    background = pygame.image.load(
        join(
            "sprite", "winner.png" if winner else "looser.png"
        )  # 👈 cambiado a sprite/
    ).convert_alpha()

    # Botones
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

        # Dibujo
        display.fill(Color.GREEN)
        display.blit(background, (0, 0))
        lista.draw(display)
        pygame.display.update()

    return play


# En cada partida se reinicia el patrón, las vidas, el array del player, se incrementa el nivel en 1.
# Se puede poner una puntuación para el jugador.
