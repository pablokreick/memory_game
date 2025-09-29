import pygame
import sys
import random
from lib.Core import Player, Ball, HUDLifes, SoundManager, AssetManager

import lib.Var as Var
import lib.Color as Color
import lib.fun as f


def main():
    pygame.init()
    display = pygame.display.set_mode((Var.WIDTH, Var.HEIGHT))
    pygame.display.set_caption(Var.TITLE)
    clock = pygame.time.Clock()

    # ==== Gestores ====
    sound_manager = SoundManager()
    assets = AssetManager()

    # Variables del juego
    level = 1
    balls_quantity = 2

    # Grupos de sprites
    player_sprite = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    ball_sprites = pygame.sprite.Group()

    # Recursos
    numbers = assets.get_numbers()
    level_image = assets.get_level_image()
    top_menu = assets.get_top_menu()
    life = assets.get_life()
    background = assets.get_background()
    hud_lifes = HUDLifes(life, max_lifes=3)
    top_menu_rect = top_menu.get_rect(center=(Var.WIDTH // 2, top_menu.get_height() // 2))
    level_rect = level_image.get_rect(topright=(Var.WIDTH - 100, 70))
    background_rect = background.get_rect(topleft=(0, 0))

    # Fuente por si no tenés sprite de "Puntos"
    font = pygame.font.SysFont(None, 36)

    # ==== Función auxiliar para mostrar las bolas del patrón ====
    def show_balls(balls):
        for i, ball in enumerate(balls):
            surf = assets.get_ball(ball.color)
            rect = surf.get_rect(topleft=(200 + i * 50, 7))
            display.blit(surf, rect)

    # ==== Función para evitar superposición de bolas ====
    def recolocar_bolas(bolas):
        for i in range(len(bolas)):
            for j in range(i + 1, len(bolas)):
                # mientras se superpongan, recoloco la bola j
                while bolas[i].rect.colliderect(bolas[j].rect):
                    bolas[j].rect.center = (
                        random.randint(50, Var.WIDTH - 50),
                        random.randint(100, Var.HEIGHT // 3),
                    )

    # Menú inicial
    play = f.menu(display)

    # ==== Bucle principal del juego ====
    while play:
        all_sprites.empty()
        ball_sprites.empty()
        player_sprite.empty()

        level_number_image = numbers[level]
        level_number_rect = level_number_image.get_rect(
            topleft=(Var.WIDTH - level_number_image.get_width() - 20, 70)
        )

        balls = []
        pattern = []
        player = Player((all_sprites, player_sprite))
        player.rect.center = (Var.WIDTH // 2, Var.HEIGHT - player.image.get_height())
        player.colors = []
        player.lifes = 3
        player.reset_score()   # 👈 reinicia el score al comenzar nivel
        hud_lifes.reset()

        # Crear patrón (lista de colores)
        for _ in range(balls_quantity):
            color = random.choice(["blue", "lightblue", "green", "red", "violet", "yellow"])
            pattern.append(color)

        # Crear bolas del patrón con posiciones iniciales aleatorias
        for color in pattern:
            ball = Ball(assets.get_ball(color), color, (all_sprites, ball_sprites))
            ball.rect.center = (
                random.randint(50, Var.WIDTH - 50),
                random.randint(100, Var.HEIGHT // 3),
            )
            balls.append(ball)

        # 👇 Corregir superposiciones
        recolocar_bolas(balls)

        # 👇 Mostrar el patrón ANTES del menú de cuenta regresiva
        display.blit(background, background_rect)
        display.blit(top_menu, top_menu_rect)
        show_balls(balls)
        pygame.display.update()

        # Ahora sí mostrar el menú de cuenta regresiva
        play = f.pattern_menu(display, balls)
        print(pattern)

        in_game = True
        while in_game and play:
            dt = clock.tick(Var.FPS) / 1000
            display.fill(Color.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    in_game = False

            # Colisiones
            collided_ball = pygame.sprite.spritecollide(
                player, ball_sprites, False, pygame.sprite.collide_mask
            )
            if collided_ball:
                for ball in collided_ball:
                    index = len(player.colors)
                    if ball.color == pattern[index]:
                        player.colors.append(ball)
                        sound_manager.play_good()
                        all_sprites.remove(ball)
                        ball_sprites.remove(ball)
                        player.add_score(10)   # 👈 suma puntos
                        if len(player.colors) >= len(pattern):
                            sound_manager.play_win()
                            play = f.final_menu(display, True)
                            level += 1
                            balls_quantity += 1
                            Var.BALL_SPEED += 5
                            in_game = False
                    else:
                        # rebota mal → se recoloca
                        ball.rect.center = (
                            random.randint(0, Var.WIDTH),
                            random.randint(0, Var.HEIGHT),
                        )
                        sound_manager.play_wrong()
                        player.lifes -= 1
                        player.add_score(-1)   # 👈 resta puntos
                        hud_lifes.lose()
                        if player.lifes == 0:
                            sound_manager.play_fail()
                            play = f.final_menu(display, False)
                            in_game = False
                            balls_quantity = 2
                            level = 1

            # === Dibujado ===
            all_sprites.update(dt)
            display.blit(background, background_rect)
            all_sprites.draw(display)
            display.blit(top_menu, top_menu_rect)
            show_balls(player.colors)
            hud_lifes.draw(display)
            display.blit(level_image, level_rect)
            display.blit(level_number_image, level_number_rect)

            # --- Mostrar SCORE ---
            score_text = font.render(f"Score: {player.get_score()}", True, (255, 255, 255))
            display.blit(score_text, (300, 70))

            pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()