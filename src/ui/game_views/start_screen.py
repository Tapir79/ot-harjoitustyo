import pygame
from config import BLACK, WHITE
from app_enums import AppState, CurrentField
from ui.game_views.base_view import BaseView


class StartScreenView(BaseView):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 36)
        self.init_mouse_click_areas()
        self.current_field = CurrentField.START

    def init_mouse_click_areas(self):
        self.start_rect = pygame.Rect(250, 200, 350, 36)
        self.login_rect = pygame.Rect(250, 250, 350, 36)
        self.create_account_rect = pygame.Rect(250, 300, 350, 36)

    def render(self):
        self.screen.fill(BLACK)
        self.draw_labels()
        pygame.display.flip()

    def draw_labels(self):
        self.screen.blit(self.font.render(
            "Alien Attack", True, WHITE), (250, 100))
        self.screen.blit(self.small_font.render(
            "1. Start Game", True, WHITE), (250, 200))
        self.screen.blit(self.small_font.render(
            "2. Login", True, WHITE), (250, 250))
        self.screen.blit(self.small_font.render(
            "3. Create Account", True, WHITE), (250, 300))
        self.screen.blit(self.small_font.render(
            "ESC: Quit", True, WHITE), (250, 350))

    def handle_event(self, event):
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_mouse_click(event)

    def handle_mouse_click(self, event):
        if self.start_rect.collidepoint(event.pos):
            self.current_field = CurrentField.START
            return AppState.GAME_RUNNING
        elif self.login_rect.collidepoint(event.pos):
            self.current_field = CurrentField.LOGIN
            return AppState.LOGIN_VIEW
        elif self.create_account_rect.collidepoint(event.pos):
            self.current_field = CurrentField.CREATE
            return AppState.CREATE_USER_VIEW

# Entry point


def start_screen(screen):
    return StartScreenView(screen).run()
