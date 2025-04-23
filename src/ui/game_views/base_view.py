import pygame
from app_enums import AppState, CurrentField
from config import BLACK, WHITE
from db import Database
from repositories.user_repository import UserRepository
from services.user_service import UserService


class BaseView:
    def __init__(self, screen, esc_state=None):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.current_field = CurrentField.USERNAME
        self.message = ""
        self.borders = {"thick": 3, "thin": 1}
        self.user_service = UserService(UserRepository(Database()))
        self.username_rect = pygame.Rect(250, 150, 300, 36)
        self.password_rect = pygame.Rect(250, 200, 300, 36)
        self.esc_state = esc_state

    def run(self):
        while True:
            self.render()
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result is not None:
                    return result

    def render(self):
        raise NotImplementedError("Subclass must implement render()")

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return AppState.QUIT
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.esc_state is not None:
                return self.esc_state
            return self.handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_mouse_click(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_TAB:
            self.current_field = (
                CurrentField.PASSWORD if self.current_field == CurrentField.USERNAME else CurrentField.USERNAME
            )
        elif event.key == pygame.K_BACKSPACE:
            self._update_input_field(backspace=True)
        elif event.key == pygame.K_RETURN:
            return self.on_submit()
        else:
            self._update_input_field(char=event.unicode)

    def _update_input_field(self, backspace=False, char=None):
        if hasattr(self, "input_boxes"):
            if backspace:
                self.input_boxes[self.current_field] = self.input_boxes[self.current_field][:-1]
            elif char:
                self.input_boxes[self.current_field] += char
        else:
            if backspace:
                if self.current_field == CurrentField.USERNAME:
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            elif char:
                if self.current_field == CurrentField.USERNAME:
                    self.username += char
                else:
                    self.password += char

    def handle_mouse_click(self, event):
        if self.username_rect.collidepoint(event.pos):
            self.current_field = CurrentField.USERNAME
        elif self.password_rect.collidepoint(event.pos):
            self.current_field = CurrentField.PASSWORD

    def draw_input_field(self, rect, text, is_active, is_password=False):
        border = self.borders["thick"] if is_active else self.borders["thin"]
        pygame.draw.rect(self.screen, WHITE, rect, border)
        display_text = "*" * len(text) if is_password else text
        surface = self.font.render(display_text, True, WHITE)
        self.screen.blit(surface, (rect.x + 5, rect.y + 5))

    def draw_text(self, text, pos, font=None):
        f = font or self.font
        surface = f.render(text, True, WHITE)
        self.screen.blit(surface, pos)

    def on_submit(self):
        raise NotImplementedError("Subclass must implement on_submit()")
