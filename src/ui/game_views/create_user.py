import pygame
from app_enums import AppState, CurrentField
from config import BLACK
from db import Database
from entities.user import User
from ui.game_views.managers.event_loop import EventLoop
from ui.game_views.managers.menu_drawer import MenuDrawer
from ui.game_views.managers.session_manager import SessionManager


class CreateUserView():
    """
    View for creating a new user account.

    Inherits from BaseView and provides input fields and submit logic
    for user registration.
    """

    def __init__(self, screen, user=None):
        """
        Initialize the CreateUserView.

        Args:
            screen: The pygame display surface.
        """
        self.screen = screen
        self.message = ""
        self._drawer = MenuDrawer(screen)

        self.current_field = CurrentField.USERNAME
        self._username_rect = pygame.Rect(250, 150, 300, 36)
        self._password_rect = pygame.Rect(250, 200, 300, 36)
        self._loop = EventLoop(self, esc_state=AppState.START_SCREEN)

        self.input_boxes = {
            CurrentField.USERNAME: "",
            CurrentField.PASSWORD: ""
        }

        session = SessionManager(Database())
        self.user, _ = session.current_user(user)
        self._user_service = session.user_service
        self._user_statistics_service = session.user_statistics_service

    def run(self):
        """
        Main loop for the view.
        Renders the view and handles events until an AppState is returned.

        Returns:
            AppState: The next application state based on user actions.
        """
        return self._loop.run()

    def render(self):
        """
        Render the CreateUserView.

        Fills the screen, draws labels and input fields,
        and displays any messages.
        """
        self.screen.fill(BLACK)
        y = self.draw_create_user_labels()
        self._drawer.draw_input_field(
            self._username_rect,
            self.input_boxes[CurrentField.USERNAME],
            self.current_field == CurrentField.USERNAME
        )
        self._drawer.draw_input_field(
            self._password_rect,
            self.input_boxes[CurrentField.PASSWORD],
            self.current_field == CurrentField.PASSWORD,
            is_password=True
        )
        if self.message:
            self._drawer.draw_text(self.message, (100, y))
        pygame.display.flip()

    def draw_create_user_labels(self):
        """
        Draw static text labels (Login, Username, Password prompts) on the screen.
        """
        lines = ["Create a new user", "Username:", "Password:",
                 "Press Tab to change field",
                 "Press ENTER to submit",
                 "Press ESC to return"]
        y = self._drawer.draw_labels(lines)
        return y

    def on_submit(self):
        """
        Handle the user registration when ENTER is pressed.

        Returns:
            AppState or None: Returns AppState.START_SCREEN on success, or None on failure.
        """
        username = self.input_boxes[CurrentField.USERNAME].strip()
        password = self.input_boxes[CurrentField.PASSWORD].strip()
        success, message, user = self._user_service.register_user(
            username, password)
        if success:
            self._user_statistics_service.create_user_statistics(
                user.user_id, 0, 0)
            user_id, msg = self._user_service.login(username, password)

        self.message = message
        if success:
            self.render()
            self.user = User(user_id, username)
            pygame.display.flip()
            pygame.time.wait(1500)
            return AppState.START_SCREEN
        return None
