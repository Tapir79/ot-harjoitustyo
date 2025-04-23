import pygame
from app_enums import AppState, CurrentField
from config import BLACK, WHITE
from db import Database
from services.user_service import UserService
from repositories.user_repository import UserRepository
from ui.game_views.base_view import BaseView


class CreateUserView(BaseView):
    def __init__(self, screen):
        super().__init__(screen, esc_state=AppState.START_SCREEN)
        self.input_boxes = {
            CurrentField.USERNAME: "",
            CurrentField.PASSWORD: ""
        }

    def render(self):
        self.screen.fill(BLACK)
        self.draw_labels()
        self.draw_input_field(
            self.username_rect, self.input_boxes[CurrentField.USERNAME], self.current_field == CurrentField.USERNAME)
        self.draw_input_field(
            self.password_rect, self.input_boxes[CurrentField.PASSWORD], self.current_field == CurrentField.PASSWORD, is_password=True)
        if self.message:
            self.draw_text(self.message, (100, 300))
        pygame.display.flip()

    def draw_labels(self):
        self.draw_text("Create a new user", (100, 100))
        self.draw_text("Username:", (100, 150))
        self.draw_text("Password:", (100, 200))
        self.draw_text("Press ENTER to submit", (100, 250))

    def on_submit(self):
        username = self.input_boxes[CurrentField.USERNAME].strip()
        password = self.input_boxes[CurrentField.PASSWORD].strip()
        success, message, _ = self.user_service.register_user(
            username, password)
        self.message = message
        if success:
            self.render()
            pygame.display.flip()
            pygame.time.wait(1500)
            return AppState.START_SCREEN
        return None
