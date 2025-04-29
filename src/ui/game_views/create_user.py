import pygame
from app_enums import AppState, CurrentField
from config import BLACK
from entities.user import User
from ui.game_views.base_view import BaseView


class CreateUserView(BaseView):
    """
    View for creating a new user account.

    Inherits from BaseView and provides input fields and submit logic
    for user registration.
    """

    def __init__(self, screen):
        """
        Initialize the CreateUserView.

        Args:
            screen: The pygame display surface.
        """
        super().__init__(screen, esc_state=AppState.START_SCREEN)
        self.input_boxes = {
            CurrentField.USERNAME: "",
            CurrentField.PASSWORD: ""
        }

    def render(self):
        """
        Render the CreateUserView.

        Fills the screen, draws labels and input fields,
        and displays any messages.
        """
        self.screen.fill(BLACK)
        y = self.draw_create_user_labels()
        self.draw_input_field(
            self.username_rect,
            self.input_boxes[CurrentField.USERNAME],
            self.current_field == CurrentField.USERNAME
        )
        self.draw_input_field(
            self.password_rect,
            self.input_boxes[CurrentField.PASSWORD],
            self.current_field == CurrentField.PASSWORD,
            is_password=True
        )
        if self.message:
            self.draw_text(self.message, (100, y))
        pygame.display.flip()

    def draw_create_user_labels(self):
        """
        Draw static text labels (Login, Username, Password prompts) on the screen.
        """
        lines = ["Create a new user", "Username:", "Password:",
                 "Press Tab to change field",
                 "Press ENTER to submit",
                 "Press ESC to return"]
        y = self.draw_labels(lines)
        return y

    def on_submit(self):
        """
        Handle the user registration when ENTER is pressed.

        Returns:
            AppState or None: Returns AppState.START_SCREEN on success, or None on failure.
        """
        username = self.input_boxes[CurrentField.USERNAME].strip()
        password = self.input_boxes[CurrentField.PASSWORD].strip()
        success, message, user = self.user_service.register_user(
            username, password)
        if success:
            self.user_statistics_service.create_user_statistics(
                user.user_id, 0, 0)
            user_id, msg = self.user_service.login(username, password)

        self.message = message
        if success:
            self.render()
            pygame.display.flip()
            pygame.time.wait(1500)
            return AppState.START_SCREEN, User(user_id, username)
        return None
