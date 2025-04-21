import pygame
from config import BLACK, WHITE
from app_state import AppState

class StartScreenView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 36)

    def run(self):
        while True:
            self.render()
            for event in pygame.event.get():
                state = self.handle_event(event)
                if state is not None:
                    return state

    def render(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.font.render("Alien Attack", True, WHITE), (250, 100))
        self.screen.blit(self.small_font.render("1: Start Game", True, WHITE), (250, 200))
        self.screen.blit(self.small_font.render("2: Login", True, WHITE), (250, 250))
        self.screen.blit(self.small_font.render("3: Create Account", True, WHITE), (250, 300))
        self.screen.blit(self.small_font.render("ESC: Quit", True, WHITE), (250, 350))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return AppState.QUIT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return AppState.GAME_RUNNING
            elif event.key == pygame.K_2:
                return AppState.LOGIN_VIEW
            elif event.key == pygame.K_3:
                return AppState.CREATE_USER_VIEW
            elif event.key == pygame.K_ESCAPE:
                return AppState.QUIT

# Entry point
def draw_start_screen(screen):
    return StartScreenView(screen).run()
