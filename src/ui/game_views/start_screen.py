
import os
import pygame
from config import BLACK, BRONZE, GOLD, SILVER, WHITE, ASSETS_DIR
from app_enums import AppState, CurrentField
from db import Database
from ui.game_views.managers.event_loop import EventLoop
from ui.game_views.managers.menu_drawer import MenuDrawer
from ui.game_views.managers.session_manager import SessionManager
from utils.ui_helpers import format_high_scores


class StartScreenView():
    """
    The start screen view shown when the game launches.

    Allows users to choose between starting the game, logging in, or creating an account.
    If the player is logged in only start game is visible. 

    Inherits from BaseView to use common input handling and rendering functionality.
    """

    def __init__(self, screen, user=None, esc_state=AppState.QUIT):
        """
        Initialize the start screen view.

        Args:
            screen: The pygame screen surface to draw on.
            user: The currently logged-in user (optional).
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 36)
        self.selected_index = 0
        self.borders = {"thick": 3, "thin": 1}
        self._drawer = MenuDrawer(screen)

        self.current_field = CurrentField.START
        self.username_rect = pygame.Rect(250, 150, 300, 36)
        self.password_rect = pygame.Rect(250, 200, 300, 36)

        self.menu_items = []
        self.esc_state = esc_state

        session = SessionManager(Database())
        self.user, self.user_statistics = session.current_user(user)
        self._user_service = session.user_service
        self._user_statistics_service = session.user_statistics_service

        self.top_scores = session.top_scores()

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
        Render the start screen elements and update the display.
        """
        self.screen.fill(BLACK)
        self.draw_labels()
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
        Handle keypress events to select a menu option.

        Args:
            event: The pygame KEYDOWN event.

        Returns:
            AppState: The next application state based on user choice.
        """
        if event.key == pygame.K_UP:
            self.move_up()
        elif event.key == pygame.K_DOWN:
            self.move_down()
        elif event.key == pygame.K_RETURN:
            return self.choose_option()
        if event.key == pygame.K_TAB:
            self.handle_key_tab()

        if event.key == pygame.K_1:
            return AppState.RUN_GAME
        elif event.key == pygame.K_2:
            return AppState.LOGIN_VIEW
        elif event.key == pygame.K_3:
            return AppState.CREATE_USER_VIEW

        return None

    def draw_title(self):
        """
        Loads and draws the main title image at the top of the screen.

        The image is loaded from the assets directory, scaled to match the screen width 
        while preserving its height, and then blitted onto the screen at the top-left corner.
        """
        self.image = pygame.image.load(
            os.path.join(ASSETS_DIR, "game_title.png")
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image, (self.screen.get_width(), self.image.get_height()))

        self.rect = self.image.get_rect()
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def draw_main_title(self, center_x, y):
        """
        Draw the main title image. 

        Args:
            center_x: center x-coordinate
            y: The y-coordinate to start drawing the first option

        Returns:
            y = The next y coordinate
        """
        self.draw_title()
        y += 100

        if self.user:
            self._drawer.draw_text(f"Player: {self.user.username}",
                                   (center_x, y), self.small_font, center=True)
            y += 30
            self._drawer.draw_text(f"Your High Score: {self.user_statistics.high_score}", (
                center_x, y), self.small_font, center=True)
            y += 30

        return y

    def draw_top_high_scores(self, center_x, y):
        """
        Draw top high scores.

        Args:
            center_x: center x-coordinate
            y: The y-coordinate to start drawing the first option

        Returns:
            y = The next y coordinate
        """

        if not self.top_scores:
            self.top_scores = [None, None, None]

        rows = []

        y += 20
        title = "Rank  High Score  Username"
        title_rect = self._drawer.draw_text(
            str(title), (center_x, y), center=True)
        y += 30

        for i, score in enumerate(self.top_scores):
            rank, high_score, username = format_high_scores(i, score)
            rows.append(f"{rank}  {high_score}   {username}")

        player_colors = [GOLD, SILVER, BRONZE]
        for i, row in enumerate(rows):
            self._drawer.draw_text(str(row), (title_rect.left, y),  center=False,
                                   color=player_colors[i])
            y += 30

        y += 30
        return y

    def draw_menu_options(self, center_x, y):
        """
        Draw menu options.

        Args:
            center_x: center x-coordinate
            y: The y-coordinate to start drawing the first option

        Returns:
            y = The next y coordinate
        """
        menu_items = [(f"Start Game", AppState.RUN_GAME)]
        if self.user.user_id == 1:
            menu_items += [
                (f"Login", AppState.LOGIN_VIEW),
                (f"Create a New User", AppState.CREATE_USER_VIEW)
            ]
        if self.user.user_id != 1:
            menu_items += [(f"Logout", AppState.LOGOUT)]

        for index, (text, app_state) in enumerate(menu_items):
            selected = (index == self.selected_index)
            rect = self.draw_text_return_rect(
                text,
                (center_x, y),
                self.font,
                center=True,
                highlight=selected
            )
            self.menu_items.append((rect, app_state))
            y += 50

        return y

    def draw_labels(self):
        """
        Draw the main title, high scores, and menu options
        with retro arcade-style layout.
        """
        self.menu_items.clear()

        screen_width = self.screen.get_width()
        center_x = screen_width // 2
        y = 60

        y = self.draw_main_title(center_x, y)

        y = self.draw_top_high_scores(center_x, y)

        y = self.draw_menu_options(center_x, y)

        y += 20
        self._drawer.draw_text("Press ESC to Quit", (center_x, y),
                               self.font, center=True)

    def draw_text_return_rect(self, text, pos, font, center=False, highlight=False):
        """
        Draws text and returns its Rect for future use.

        Args:
            text: The text to draw.
            pos: (x, y) position.
            font: Font to use.
            center: Whether to center the text.
            highlight: Whether to highlight the text (yellow color).

        Returns:
            pygame.Rect: The rectangle area of the drawn text.
        """
        color = (255, 255, 0) if highlight else WHITE
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if center:
            text_rect.center = pos
        else:
            text_rect.topleft = pos

        self.screen.blit(text_surface, text_rect)

        if highlight:
            underline_start = (text_rect.left, text_rect.bottom + 2)
            underline_end = (text_rect.right, text_rect.bottom + 2)
            pygame.draw.line(self.screen, color,
                             underline_start, underline_end, 2)

        return text_rect

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
            title_text: Title to center.
            lines: Lines of text to draw.
            center_x: Center x-coordinate of screen.
            y_start: Start y position.
            line_colors: Colors for each line.
            line_fonts: Fonts for each line.
        """

        y, left_x = self.draw_centered_title(title_text, center_x, y_start)
        y = self.draw_lines_aligned_with_title(
            lines, line_colors, line_fonts, left_x, y)

        return y

    def draw_centered_title(self, title_text, center_x, y_start):
        """
        Draws a centered title. 

        Args:
            title_text: The text of the title.
            center_x: Center x-coordinate of screen.
            y_start: Start y position.

        Returns: 
            y = next y coordinate
            left_x = title text left x coordinate
        """
        title_surface = self.small_font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(center_x, y_start))
        self.screen.blit(title_surface, title_rect)

        y = y_start + 40
        left_x = title_rect.left

        return y, left_x

    def draw_lines_aligned_with_title(self, lines, line_colors, line_fonts, x, y):
        """
        Draws a list of text lines.
        Lines can have different colors and fonts. 

        Args:
            title_text: Title to center.
            lines: Lines of text to draw.
            line_colors: Colors for each line.
            line_fonts: Fonts for each line.
            x: x-coordinate position for each line
            y: y-coordinate position for the first line

        Returns:
        y = next y coordinate 
        """
        for idx, line in enumerate(lines):
            color = WHITE
            if line_colors and idx < len(line_colors):
                color = line_colors[idx]
            if line_fonts and idx < len(line_fonts):
                font = line_fonts[idx]
            else:
                font = self.small_font

            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x, y)
            self.screen.blit(text_surface, text_rect)

            y += 40

        return y

    def move_up(self):
        """
        Selected index moves backwards in the menu_items.
        Visually this means moving up in the menu.
        If in the beginning of the list the index is set to last index. 
        """
        if self.menu_items:
            self.selected_index = (
                self.selected_index - 1) % len(self.menu_items)

    def move_down(self):
        """
        Selected index moves forwards in the menu_items.
        Visually this means moving down in the menu.
        If at the end of the list the index is set to 0. 
        """
        if self.menu_items:
            self.selected_index = (
                self.selected_index + 1) % len(self.menu_items)

    def choose_option(self):
        """
        Fetch menu_item application state from menu items by selected index
        """
        if self.menu_items:
            rect, app_state = self.menu_items[self.selected_index]
            return app_state

    def handle_key_tab(self):
        """
        Selected index moves forwards in the menu_items.
        Visually this means moving down in the menu.
        If at the end of the list the index is set to 0. 
        """
        if self.menu_items:
            self.selected_index = (
                self.selected_index + 1) % len(self.menu_items)
