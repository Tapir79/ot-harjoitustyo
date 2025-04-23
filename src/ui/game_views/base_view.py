import pygame
from app_enums import AppState


class BaseView:
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        while True:
            self.render()
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result is not None:
                    return result

    def render(self):
        raise NotImplementedError("Subclass must implement render()")

    def handle_event(self, event):
        raise NotImplementedError("Subclass must implement handle_event()")
