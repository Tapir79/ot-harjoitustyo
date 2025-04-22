import pygame
from app_enums import AppState, CurrentField
from config import BLACK, WHITE
from services.user_service import UserService


class CreateUserView:
    """
    A UI view to create a new user with a password.
    """

    def __init__(self, screen):
        self.screen = screen
        self.input_boxes = {CurrentField.USERNAME: "",
                            CurrentField.PASSWORD: ""}
        self.current_field = CurrentField.USERNAME
        self.message = ""
        self.font = pygame.font.Font(None, 36)
        self.username_rect = pygame.Rect(250, 150, 300, 36)
        self.password_rect = pygame.Rect(250, 200, 300, 36)
        self.borders = {"thick": 3, "thin": 1}
        self.user_service = UserService()

    def run(self):
        while True:
            self.render()
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result is not None:
                    return result

    def render(self):
        self.screen.fill(BLACK)
        self.draw_labels()
        self.draw_input_field(
            self.username_rect, self.input_boxes[CurrentField.USERNAME], self.current_field == CurrentField.USERNAME)
        self.draw_input_field(
            self.password_rect, self.input_boxes[CurrentField.PASSWORD], self.current_field == CurrentField.PASSWORD, is_password=True)

        if self.message:
            self.screen.blit(self.font.render(
                self.message, True, WHITE), (100, 300))

        pygame.display.flip()

    def draw_labels(self):
        self.screen.blit(self.font.render(
            "Create a new user", True, WHITE), (100, 100))
        self.screen.blit(self.font.render(
            "Username:", True, WHITE), (100, 150))
        self.screen.blit(self.font.render(
            "Password:", True, WHITE), (100, 200))
        self.screen.blit(self.font.render(
            "Press ENTER to submit", True, WHITE), (100, 250))

    def draw_input_field(self, input_field_rect, text, is_active, is_password=False):
        border = self.borders["thick"] if is_active else self.borders["thin"]
        pygame.draw.rect(self.screen, WHITE, input_field_rect, border)
        input_field_text = self.get_input_field_text(text, is_password)
        surface = self.font.render(input_field_text, True, WHITE)
        position = self.get_input_field_text_coordinates(input_field_rect)
        self.screen.blit(surface, position)

    def get_input_field_text(self, text, is_password):
        if is_password:
            return "*" * len(text)
        return text

    def get_input_field_text_coordinates(self, input_field_rect):
        padding = 5
        return (input_field_rect.x + padding, input_field_rect.y + padding)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return AppState.QUIT

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return AppState.START_SCREEN
            return self.handle_keydown(event)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_TAB:
            self.current_field = CurrentField.PASSWORD if self.current_field == CurrentField.USERNAME else CurrentField.USERNAME
        elif event.key == pygame.K_BACKSPACE:
            self.input_boxes[self.current_field] = self.input_boxes[self.current_field][:-1]
        elif event.key == pygame.K_RETURN:
            return self.try_create_user()
        else:
            self.input_boxes[self.current_field] += event.unicode

    def handle_mouse_click(self, event):
        if self.username_rect.collidepoint(event.pos):
            self.current_field = CurrentField.USERNAME
        elif self.password_rect.collidepoint(event.pos):
            self.current_field = CurrentField.PASSWORD

    def try_create_user(self):
        username = self.input_boxes[CurrentField.USERNAME].strip()
        password = self.input_boxes[CurrentField.PASSWORD].strip()

        success, message = self.user_service.register_user(username, password)
        self.message = message
        if success:
            self.render()
            pygame.display.flip()
            pygame.time.wait(1500)
            return AppState.START_SCREEN

        return None

# Entry point from main


def create_user_view(screen):
    return CreateUserView(screen).run()
