import pygame
from app_enums import AppState
from config import BLACK, WHITE


def draw_login_view(screen):
    font = pygame.font.Font(None, 36)
    while True:
        screen.fill(BLACK)
        screen.blit(font.render(
            "Login View (press ESC to go back)", True, WHITE), (100, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return AppState.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return AppState.START_SCREEN
