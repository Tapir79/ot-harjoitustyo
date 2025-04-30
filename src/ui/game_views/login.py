import pygame
from app_enums import AppState, CurrentField
from config import BLACK
from entities.user import User
from ui.game_views.base_view import BaseView


class LoginView(BaseView):
    """
    Login screen where the user can input their username and password 
    to authenticate.

    Inherits from BaseView to reuse input handling and rendering functionality.
    """

    def __init__(self, screen):
        """
        Initialize the login view.

        Args:
            screen: The pygame screen surface to draw on.
        """
        super().__init__(screen, esc_state=AppState.START_SCREEN)
        self.username = ""
        self.password = ""
        self.user = None

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
