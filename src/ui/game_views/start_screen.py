import pygame
from config import BLACK, WHITE
from app_state import AppState


def draw_start_screen(screen):
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 36)

    while True:
        screen.fill(BLACK)
        screen.blit(font.render("Alien Attack", True, WHITE), (250, 100))
        screen.blit(small_font.render(
            "1: Start Game", True, WHITE), (250, 200))
        screen.blit(small_font.render("2: Login", True, WHITE), (250, 250))
        screen.blit(small_font.render(
            "3: Create Account", True, WHITE), (250, 300))
        screen.blit(small_font.render("ESC: Quit", True, WHITE), (250, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return AppState.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return AppState.GAME_RUNNING
                elif event.key == pygame.K_2:
                    return AppState.LOGIN_VIEW
                elif event.key == pygame.K_3:
                    return AppState.CREATE_USER_VIEW
                elif event.key == pygame.K_ESCAPE:
                    return AppState.QUIT
