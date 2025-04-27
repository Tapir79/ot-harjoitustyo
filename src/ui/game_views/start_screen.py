import pygame
from config import BLACK
from app_enums import AppState, CurrentField
from entities.user_statistics import UserStatistics
from ui.game_views.base_view import BaseView


class StartScreenView(BaseView):
    """
    The start screen view shown when the game launches.

    Allows users to choose between starting the game, logging in, or creating an account.
    If the player is logged in only start game is visible. 

    Inherits from BaseView to use common input handling and rendering functionality.
    """

    def __init__(self, screen, user=None):
        """
        Initialize the start screen view.

        Args:
            screen: The pygame screen surface to draw on.
            user: The currently logged-in user (optional).
        """
        super().__init__(screen, esc_state=AppState.QUIT)
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 36)
        self.current_field = CurrentField.START
        self.user = user
        if self.user:
            self.user_statistics, _ = self.user_statistics_service.get_user_statistics(
                self.user.user_id)
        self.init_mouse_click_areas()

    def init_mouse_click_areas(self):
        """
        Define clickable areas (start, login, create account) on the start screen.
        """
        self.start_rect = pygame.Rect(250, 200, 350, 36)
        self.login_rect = pygame.Rect(250, 250, 350, 36)
        self.create_account_rect = pygame.Rect(250, 300, 350, 36)

    def render(self):
        """
        Render the start screen elements and update the display.
        """
        self.screen.fill(BLACK)
        self.draw_labels()
        pygame.display.flip()

    def draw_labels(self):
        """
        Draw the main title and menu options based on whether a user is logged in.
        """
        self.draw_text("Alien Attack", (250, 100), self.font)

        if self.user:
            self.draw_text(f"Playing as: {self.user.username}",
                           (250, 150), self.small_font)
            self.draw_text(
                f"{self.user.username} high score: {self.user_statistics.high_score}", (250, 200), self.small_font)
            self.top_high_scores()
            self.draw_text("1. Start Game", (250, 450), self.small_font)
            self.draw_text("ESC: Quit", (250, 500), self.small_font)
        else:
            self.top_high_scores()
            self.draw_text("1. Start Game", (250, 450), self.small_font)
            self.draw_text("2. Login", (250, 500), self.small_font)
            self.draw_text("3. Create Account", (250, 550), self.small_font)
            self.draw_text("ESC: Quit", (250, 600), self.small_font)

    def top_high_scores(self):
        """
        TODO get top 3 all time high scores
        """
        self.draw_text("High scores", (250, 250), self.small_font)
        self.draw_text("1. NN placeholder", (250, 300), self.small_font)
        self.draw_text("2. JJ placeholder", (250, 350), self.small_font)
        self.draw_text("3. KK placeholder", (250, 400), self.small_font)

    def handle_keydown(self, event):
        """
        Handle keypress events to select a menu option.

        Args:
            event: The pygame KEYDOWN event.

        Returns:
            AppState: The next application state based on user choice.
        """
        if event.key == pygame.K_1:
            return AppState.RUN_GAME
        elif event.key == pygame.K_2:
            return AppState.LOGIN_VIEW
        elif event.key == pygame.K_3:
            return AppState.CREATE_USER_VIEW

    def handle_mouse_click(self, event):
        """
        Handle mouse clicks on the start screen menu options.

        Args:
            event: The pygame MOUSEBUTTONDOWN event.

        Returns:
            AppState: The next application state based on which area was clicked.
        """
        if self.start_rect.collidepoint(event.pos):
            return AppState.RUN_GAME
        elif self.login_rect.collidepoint(event.pos):
            return AppState.LOGIN_VIEW
        elif self.create_account_rect.collidepoint(event.pos):
            return AppState.CREATE_USER_VIEW
