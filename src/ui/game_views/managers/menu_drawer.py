import pygame
from app_enums import GameAttributes
from config import THICK_BORDER, THIN_BORDER, WHITE


class MenuDrawer:
    """
    Handles rendering of text and input fields on the screen.

    This class provides utility methods to draw input boxes, single text labels,
    and multiple lines of text.
    """

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.borders = {GameAttributes.THICK_BORDER: THICK_BORDER, 
                        GameAttributes.THIN_BORDER: THIN_BORDER}

    def draw_input_field(self, rect, text, is_active, is_password=False):
        """
        Draw an input box on the screen.

        Args:
            rect: The pygame.Rect defining the box position and size.
            text: The text to display inside the box.
            is_active: If the box is currently selected.
            is_password: password is hidden and replaced with * characters
        """
        border = self.generate_border(self, is_active)
        pygame.draw.rect(self.screen, WHITE, rect, border)
        
        display_text = self.generate_display_text(self, text, is_password)
        surface = self.font.render(display_text, True, WHITE)

        y_offset = 5
        self.screen.blit(surface, (rect.x + y_offset, rect.y + y_offset))

    def generate_border(self, is_active):
        """
        Generate a border style. 

        Args: 
            is_active: Choose active border style. 
        
        Returns:
            border style integer 
        """
        thick = GameAttributes.THICK_BORDER
        thin = GameAttributes.THIN_BORDER
        return self.borders[thick] if is_active else self.borders[thin]

    def generate_display_text(self, text, is_password):
        """
        Generate display text.

        Args:
            text: the text to draw. 
            is_password: if the text is password it should be replaced with *.
        
        Returns:
            text or the text as *.
        """
        asterixes = "*" * len(text)
        return asterixes if is_password else text

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

    def draw_labels(self, lines, start_x=100, start_y=100, line_spacing=50):
        """
        Draw static text labels (Login, Username, Password prompts) on the screen.

        Args: 
            lines: text lines to draw as a list. 
            start_x: x to start
            start_y: y to start
            line_spacing: how much space should be between the lines

        Returns:
            y: updated y for the next drawer method.
        """
        y = start_y
        for line in lines:
            self.draw_text(line, (start_x, y), self.font)
            y += line_spacing
        return y
