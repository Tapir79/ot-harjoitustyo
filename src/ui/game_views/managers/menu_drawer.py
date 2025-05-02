import pygame
from config import WHITE


class MenuDrawer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.borders = {"thick": 3, "thin": 1}

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

    def draw_labels(self, lines, start_x=100, start_y=100, line_spacing=50):
        """
        Draw static text labels (Login, Username, Password prompts) on the screen.
        """
        y = start_y
        for line in lines:
            self.draw_text(line, (start_x, y), self.font)
            y += line_spacing
        return y
