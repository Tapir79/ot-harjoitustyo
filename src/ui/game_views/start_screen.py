import pygame
from config import BLACK, WHITE
from app_enums import AppState, CurrentField
from ui.game_views.base_view import BaseView


class StartScreenView(BaseView):
    def __init__(self, screen):
        super().__init__(screen, esc_state=AppState.QUIT)
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 36)
        self.current_field = CurrentField.START
        self.init_mouse_click_areas()

    def init_mouse_click_areas(self):
        self.start_rect = pygame.Rect(250, 200, 350, 36)
        self.login_rect = pygame.Rect(250, 250, 350, 36)
        self.create_account_rect = pygame.Rect(250, 300, 350, 36)

    def render(self):
        self.screen.fill(BLACK)
        self.draw_labels()
        pygame.display.flip()

    def draw_labels(self):
        self.draw_text("Alien Attack", (250, 100), self.font)
        self.draw_text("1. Start Game", (250, 200), self.small_font)
        self.draw_text("2. Login", (250, 250), self.small_font)
        self.draw_text("3. Create Account", (250, 300), self.small_font)
        self.draw_text("ESC: Quit", (250, 350), self.small_font)

    def handle_keydown(self, event):
        if event.key == pygame.K_1:
            return AppState.GAME_RUNNING
        elif event.key == pygame.K_2:
            return AppState.LOGIN_VIEW
        elif event.key == pygame.K_3:
            return AppState.CREATE_USER_VIEW

    def handle_mouse_click(self, event):
        if self.start_rect.collidepoint(event.pos):
            return AppState.GAME_RUNNING
        elif self.login_rect.collidepoint(event.pos):
            return AppState.LOGIN_VIEW
        elif self.create_account_rect.collidepoint(event.pos):
            return AppState.CREATE_USER_VIEW
