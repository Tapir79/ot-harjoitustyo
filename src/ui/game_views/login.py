import pygame
from app_enums import AppState, CurrentField
from config import BLACK, WHITE
from db import Database
from repositories.user_repository import UserRepository
from services.user_service import UserService
from ui.game_views.base_view import BaseView


class LoginView(BaseView):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = pygame.font.Font(None, 36)
        self.username = ""
        self.password = ""
        self.current_field = CurrentField.USERNAME
        self.message = ""
        self.username_rect = pygame.Rect(250, 150, 300, 36)
        self.password_rect = pygame.Rect(250, 200, 300, 36)
        self.borders = {"thick": 3, "thin": 1}
        self.user_service = UserService(UserRepository(Database()))

    def render(self):
        self.screen.fill(BLACK)
        self.draw_labels()
        pygame.draw.rect(self.screen, WHITE, self.username_rect,
                         2 if self.current_field == CurrentField.USERNAME else 1)
        pygame.draw.rect(self.screen, WHITE, self.password_rect,
                         2 if self.current_field == CurrentField.PASSWORD else 1)

        username_surface = self.font.render(self.username, True, WHITE)
        self.screen.blit(username_surface,
                         (self.username_rect.x + 5, self.username_rect.y + 5))

        hidden_password = "*" * len(self.password)
        password_surface = self.font.render(hidden_password, True, WHITE)
        self.screen.blit(password_surface,
                         (self.password_rect.x + 5, self.password_rect.y + 5))

        if self.message:
            self.screen.blit(self.font.render(
                self.message, True, WHITE), (100, 300))

        pygame.display.flip()

    def draw_labels(self):
        self.screen.blit(self.font.render("Login", True, WHITE), (100, 100))
        self.screen.blit(self.font.render(
            "Username:", True, WHITE), (100, 150))
        self.screen.blit(self.font.render(
            "Password:", True, WHITE), (100, 200))
        self.screen.blit(self.font.render(
            "Press ENTER to submit", True, WHITE), (100, 250))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return AppState.QUIT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return AppState.START_SCREEN
            return self.handle_keydown(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_TAB:
            self.current_field = CurrentField.PASSWORD if self.current_field == CurrentField.USERNAME else CurrentField.USERNAME
        elif event.key == pygame.K_BACKSPACE:
            if self.current_field == CurrentField.USERNAME:
                self.username = self.username[:-1]
            else:
                self.password = self.password[:-1]
        elif event.key == pygame.K_RETURN:
            return self.try_login()
        else:
            if self.current_field == CurrentField.USERNAME:
                self.username += event.unicode
            else:
                self.password += event.unicode

    def handle_mouse_click(self, event):
        if self.username_rect.collidepoint(event.pos):
            self.current_field = CurrentField.USERNAME
        elif self.password_rect.collidepoint(event.pos):
            self.current_field = CurrentField.PASSWORD

    def try_login(self):
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

# Entry point


def login_view(screen):
    return LoginView(screen).run()
