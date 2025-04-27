import os
import pygame
from config import BLACK, BRONZE, GOLD, SILVER, WHITE, ASSETS_DIR
from app_enums import AppState, CurrentField
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

    def draw_title(self):
        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, "game_title.png")
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image, (self.screen.get_width(), self.image.get_height()))

        self.rect = self.image.get_rect()
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def draw_labels(self):
        """
        Draw the main title, high scores, and menu options
        with retro arcade-style layout.
        """
        screen_width = self.screen.get_width()
        center_x = screen_width // 2
        y = 60  # Start near top

        # Main Title
        self.draw_title()
        y += 100  # Big spacing after title

        if self.user:
            # Player Info
            self.draw_text(f"Player: {self.user.username}",
                           (center_x, y), self.small_font, center=True)
            y += 30
            self.draw_text(f"Your High Score: {self.user_statistics.high_score}", (
                center_x, y), self.small_font, center=True)
            y += 40

        # Top High Scores
        top_scores = ["1. NN placeholder",
                      "2. JJ placeholder", 
                      "3. KK placeholder"]
        top_colors = [GOLD, SILVER, BRONZE]

        y = self.draw_centered_title_and_left_align_rest(
            "--- Top High Scores ---",
            top_scores,
            center_x,
            y,
            line_colors=top_colors
        )

        y += 40
        # Menu Options
        self.draw_text(f"Press 1 to Start Game",
                       (center_x, y), self.font, center=True)
        if not self.user:
            y += 50
            self.draw_text(f"Press 2 to Login", (center_x, y),
                           self.small_font, center=True)
            y += 30
            self.draw_text(f"Press 3 to Create a New User",
                           (center_x, y), self.small_font, center=True)

        y += 30
        # Bottom Quit
        y += 30
        self.draw_text("Press ESC to Quit", (center_x, y),
                       self.font, center=True)

    def draw_centered_title_and_left_align_rest(self,
                                                title_text,
                                                lines,
                                                center_x,
                                                y_start,
                                                line_colors=None,
                                                line_fonts=None):
        """
        Draws a centered title, then draws each line left-aligned under it.

        Args:
            title_text (str): Title to center.
            lines (list[str]): Lines of text to draw.
            center_x (int): Center x-coordinate of screen.
            y_start (int): Start y position.
            line_colors (list[tuple[int,int,int]], optional): Colors for each line.
        """
        # Title
        title_surface = self.small_font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(center_x, y_start))
        self.screen.blit(title_surface, title_rect)

        y = y_start + 40
        left_x = title_rect.left

        # Lines
        for idx, line in enumerate(lines):
            color = WHITE  # Default white

            if line_colors and idx < len(line_colors):
                color = line_colors[idx]

            if line_fonts and idx < len(line_fonts):
                font = line_fonts[idx]
            else:
                font = self.small_font

            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (left_x, y)
            self.screen.blit(text_surface, text_rect)

            y += 40  # Move down after each line

        return y

    def draw_top_high_scores(self, center_x, y):
        """
        Draw the Top High Scores section.
        The title is centered; the scores are left-aligned starting from the same x position as the title's left side.
        """

        # First draw and measure the centered title
        title_surface = self.small_font.render(
            "--- Top High Scores ---", True, WHITE)
        title_rect = title_surface.get_rect(center=(center_x, y))
        self.screen.blit(title_surface, title_rect)

        y += 40  # Move down

        # Now align all the following texts based on the title_rect.left
        left_x = title_rect.left

        self.draw_text("1. NN placeholder", (left_x, y),
                       self.small_font, center=False)
        y += 30
        self.draw_text("2. JJ placeholder", (left_x, y),
                       self.small_font, center=False)
        y += 30
        self.draw_text("3. KK placeholder", (left_x, y),
                       self.small_font, center=False)
        y += 50

        return y

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
