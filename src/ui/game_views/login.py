import pygame
from app_enums import AppState, CurrentField
from config import BLACK, WHITE
from entities.user import User
from db import Database
from repositories.user_repository import UserRepository
from repositories.user_statistics_repository import UserStatisticsRepository
from services.session_service import SessionService
from services.user_service import UserService
from services.user_statistics_service import UserStatisticsService
from utils.game_helpers import update_single_field


class LoginView():
    """
    Login screen where the user can input their username and password 
    to authenticate.

    Inherits from BaseView to reuse input handling and rendering functionality.
    """

    def __init__(self, screen, user=None):
        """
        Initialize the login view.

        Args:
            screen: The pygame screen surface to draw on.
        """
        self.username = ""
        self.password = ""
        self.user = None

        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.current_field = CurrentField.USERNAME
        self.message = ""
        self.borders = {"thick": 3, "thin": 1}
        self.user_service = UserService(UserRepository(Database()))
        self.user_statistics_service = UserStatisticsService(
            UserStatisticsRepository(Database()))
        self.username_rect = pygame.Rect(250, 150, 300, 36)
        self.password_rect = pygame.Rect(250, 200, 300, 36)
        self.esc_state = AppState.START_SCREEN
        self.session_service = SessionService()
        self.user, self.user_statistics = self.session_service.init_user(user)

    def run(self):
        """
        Main loop for the view.
        Renders the view and handles events until an AppState is returned.

        Returns:
            AppState: The next application state based on user actions.
        """
        while True:
            self.render()
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result is not None:
                    return result, self.user

    def render(self):
        """
        Draw the login view elements to the screen.
        """
        self.screen.fill(BLACK)
        y = self.draw_login_labels()
        self.draw_input_field(self.username_rect, self.username,
                              self.current_field == CurrentField.USERNAME)
        self.draw_input_field(self.password_rect, self.password,
                              self.current_field == CurrentField.PASSWORD, is_password=True)
        if self.message:
            self.draw_text(self.message, (100, y))
        pygame.display.flip()

    def handle_event(self, event):
        """
        Handle a pygame event (key press, quit event).

        Args:
            event: The pygame event to handle.

        Returns:
            AppState or None: The next application state or None if no change.
        """
        if event.type == pygame.QUIT:
            return AppState.QUIT
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.esc_state is not None:
                return self.esc_state
            return self.handle_keydown(event)

    def handle_keydown(self, event):
        """
        Handle keyboard input for navigating fields and submitting data.

        Args:
            event: The pygame KEYDOWN event.

        Returns:
            AppState or None: The next application state or None.
        """
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
        """
        Update the active input field with user typing or backspace.

        Args:
            backspace: Whether to delete a character.
            char: The character to add.
        """
        if hasattr(self, "input_boxes"):
            if backspace:
                self.input_boxes[self.current_field] = self.input_boxes[self.current_field][:-1]
            elif char:
                self.input_boxes[self.current_field] += char
        else:
            if self.current_field == CurrentField.USERNAME:
                self.username = update_single_field(self.username,
                                                    backspace=backspace,
                                                    char=char)
            else:
                self.password = update_single_field(self.password,
                                                    backspace=backspace,
                                                    char=char)

    def draw_input_field(self, rect, text, is_active, is_password=False):
        """
        Draw an input box on the screen.

        Args:
            rect: The pygame.Rect defining the box position and size.
            text: The text to display inside the box.
            is_active: Whether the box is currently selected.
            is_password: Whether to hide the text (for passwords).
        """
        border = self.borders["thick"] if is_active else self.borders["thin"]
        pygame.draw.rect(self.screen, WHITE, rect, border)
        display_text = "*" * len(text) if is_password else text
        surface = self.font.render(display_text, True, WHITE)
        self.screen.blit(surface, (rect.x + 5, rect.y + 5))

    def draw_text(self, text, position, font=None, center=False, color=WHITE):
        """
        Draw text on the screen.

        Args:
            text: The string to render.
            pos: A tuple (x, y) for the text position.
            font: A pygame.Font object to use (optional).

        Returns:
            pygame.Rect: The rectangle of the drawn text.
        """
        if font is None:
            font = self.small_font
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect()
        if center:
            rect.center = position
        else:
            rect.topleft = position
        self.screen.blit(text_surface, rect)

        return rect

    def draw_labels(self, lines):
        """
        Draw static text labels (Login, Username, Password prompts) on the screen.
        """
        x = 100
        y = 100

        for line in lines:
            self.draw_text(line, (x, y), self.font)
            y += 50

        return y

    def draw_login_labels(self):
        """
        Draw static text labels (Login, Username, Password prompts) on the screen.
        """
        lines = ["Login",
                 "Username:",
                 "Password:",
                 "Press Tab to change field",
                 "Press ENTER to submit",
                 "Press ESC to return"]
        y = self.draw_labels(lines)
        return y

    def on_submit(self):
        """
        Handle user submission of login form.

        Returns:
            AppState or None: 
                - AppState.START_SCREEN if login successful,
                - None if login failed.
        """
        username = self.username.strip()
        password = self.password.strip()
        user_id, msg = self.user_service.login(username, password)
        if user_id:
            self.message = f"Welcome, {username}!"
            self.user = User(user_id, username)
            self.render()
            pygame.time.wait(1500)
            return AppState.START_SCREEN
        else:
            self.message = msg
        return None
