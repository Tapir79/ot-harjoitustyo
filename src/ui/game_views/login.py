import pygame
from app_enums import AppState, CurrentField
from config import BLACK, WHITE
from db import Database
from repositories.user_repository import UserRepository
from services.user_service import UserService
from ui.game_views.base_view import BaseView


class LoginView(BaseView):
    def __init__(self, screen):
        super().__init__(screen, esc_state=AppState.START_SCREEN)
        self.username = ""
        self.password = ""

    def render(self):
        self.screen.fill(BLACK)
        self.draw_labels()
        self.draw_input_field(self.username_rect, self.username,
                              self.current_field == CurrentField.USERNAME)
        self.draw_input_field(self.password_rect, self.password,
                              self.current_field == CurrentField.PASSWORD, is_password=True)
        if self.message:
            self.draw_text(self.message, (100, 300))
        pygame.display.flip()

    def draw_labels(self):
        self.draw_text("Login", (100, 100))
        self.draw_text("Username:", (100, 150))
        self.draw_text("Password:", (100, 200))
        self.draw_text("Press ENTER to submit", (100, 250))

    def on_submit(self):
        username = self.username.strip()
        password = self.password.strip()
        user_id, msg = self.user_service.login(username, password)
        if user_id:
            self.message = f"Welcome, {username}!"
            self.render()
            pygame.time.wait(1500)
            return AppState.START_SCREEN
        else:
            self.message = msg
        return None
