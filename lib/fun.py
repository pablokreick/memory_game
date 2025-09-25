import pygame
import lib.constants as constant
import lib.classes as c
from os.path import join
import random


def menu(display, clock):
    dt = clock.tick(30) / 1000
    repeat = True
    play = False
    background = pygame.image.load(join("images", "main.png")).convert_alpha()
    btn_play = c.Button("btn_play.png", constant.WIDTH // 2, constant.HEIGHT // 2)
    btn_quit = c.Button("btn_quit.png", constant.WIDTH // 2, constant.HEIGHT // 2 + 120)
    lista = pygame.sprite.Group()
    lista.add(btn_play)
    lista.add(btn_quit)
    display.fill("green")
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

        lista.update()
        display.blit(background, (0, 0))
        lista.draw(display)
        pygame.display.update()

    return play


def final_menu(display, clock, winner):
    dt = clock.tick(30) / 1000
    repeat = True
    play = False
    background = pygame.image.load(
        join("images", "winner.png" if winner else "looser.png")
    ).convert_alpha()
    btn_play = c.Button(
        "btn_again_winner.png" if winner else "btn_again.png",
        constant.WIDTH // 2,
        constant.HEIGHT // 2,
    )
    btn_quit = c.Button("btn_quit.png", constant.WIDTH // 2, constant.HEIGHT // 2 + 120)
    lista = pygame.sprite.Group()
    lista.add(btn_play)
    lista.add(btn_quit)
    display.fill("green")
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

        lista.update()
        display.blit(background, (0, 0))
        lista.draw(display)
        pygame.display.update()

    return play
