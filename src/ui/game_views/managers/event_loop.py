import pygame
from app_enums import AppState, CurrentField
from utils.game_helpers import update_single_field


class EventLoop:
    """
    Handles the main event loop for a view with text input.

    This class manages rendering, keyboard input handling (e.g., tabbing fields,
    submitting, or updating text), and application state transitions.

    Attributes:
        view: The view instance (LoginView or CreateUserView).
        esc_state: The AppState to return if ESC is pressed.
    """

    def __init__(self, view, esc_state):
        """
        view: a login or create user view object
        esc_state: the AppState to return on ESC
        """
        self.view = view
        self.esc_state = esc_state

    def run(self):
        """
        Main loop for the view.
        Renders the view and handles events until an AppState is returned.

        Returns:
            AppState: The next application state based on user actions.
        """
        while True:
            self.view.render()
            for event in pygame.event.get():
                state = self._handle_event(event)
                if state is not None:
                    return state, self.view.user

    def _handle_event(self, event):
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
            return self._handle_keydown(event)
        return None

    def _handle_keydown(self, event):
        """
        Handle keyboard input for navigating fields and submitting data.

        Args:
            event: The pygame KEYDOWN event.

        Returns:
            AppState or None: The next application state or None.
        """
        if event.key == pygame.K_TAB:
            v = self.view
            v.current_field = (
                CurrentField.PASSWORD
                if v.current_field == CurrentField.USERNAME
                else CurrentField.USERNAME
            )
            return None

        if event.key == pygame.K_BACKSPACE:
            self._update_input_field(backspace=True)
            return None

        if event.key == pygame.K_RETURN:
            return self.view.on_submit()

        self._update_input_field(char=event.unicode)
        return None

    def _update_input_field(self, backspace=False, char=None):
        """
        Move the per view text entry logic here.
        """
        v = self.view

        if hasattr(v, "input_boxes"):
            # CreateUserView style
            current = v.input_boxes[v.current_field]
            if backspace:
                v.input_boxes[v.current_field] = current[:-1]
            elif char:
                v.input_boxes[v.current_field] = current + char

        else:
            # LoginView style (attributes .username and .password)
            field_name = "username" if v.current_field == CurrentField.USERNAME else "password"
            old = getattr(v, field_name)
            new = update_single_field(old, backspace=backspace, char=char)
            setattr(v, field_name, new)
