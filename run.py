import time

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Label, Input, Digits
from textual.color import Color
from configurations import Hue, DarkTheme, LightTheme, GameMode, Icons
from game_components import (
    ControlsFooter,
    Selector,
    MinefieldUI,
    GameOverScreen
)


class MainScreen(Screen):
    """
    Main screen for setting up game preferences and starting the game.

    Attributes:
        BINDINGS (List[Tuple[str, str]]): Key bindings for widget navigation.
    """

    BINDINGS = [
        ('up, w', 'previous_widget'),
        ('down, s', 'next_widget')
    ]

    def __init__(self):
        """
        Initializes the MainScreen with input fields, selectors, and button.

        :return: None
        """

        super().__init__()
        self.set_color_theme('orange')
        self.input_field = self.create_input_field()
        self.theme_selector = self.create_theme_selector()
        self.color_selector = self.create_color_selector()
        self.game_mode_selector = self.create_game_mode_selector()
        self.play_button = self.create_play_button()
        self.main_container = Container(
            self.input_field,
            self.theme_selector,
            self.color_selector,
            self.game_mode_selector,
            self.play_button,
            classes='main_container'
        )

    def create_input_field(self) -> Input:
        """
        Creates and configures the input field for player name.

        :return: Configured Input field.
        :rtype: Input
        """

        input_field = Input(
            placeholder='Please enter your name',
            type='text',
            max_length=10,
            classes='bordered'
        )
        input_field.border_title = 'Player'
        input_field.styles.text_style = 'bold'
        input_field.styles.width = 40
        input_field.styles.text_align = 'center'
        return input_field

    def create_theme_selector(self) -> Selector:
        """
        Creates a selector for theme (Dark or Light).

        :return: Configured theme Selector.
        :rtype: Selector
        """

        selector = Selector(
            options=['Dark', 'Light'],
            classes='bordered',
            on_change=lambda x: setattr(self.app, 'dark', x == 'Dark')
        )
        selector.current_index = 0
        selector.border_title = 'Theme'
        return selector

    def create_color_selector(self) -> Selector:
        """
        Creates a selector for color themes.

        :return: Configured color Selector.
        :rtype: Selector
        """

        selector = Selector(
            options=[
                'Orange',
                'Yellow',
                'Green',
                'Blue',
                'Purple',
                'Pink',
                'Red'
            ],
            classes='bordered',
            on_change=lambda x: self.set_color_theme(x)
        )
        selector.current_index = 0
        selector.border_title = 'Color'
        return selector

    def set_color_theme(self, color: str) -> None:
        """
        Sets the color theme for the app based on the selected color.

        :param color: Selected color for the theme.
        :type color: str
        :return: None
        """

        hue = Hue[color.upper()].value / 360
        modes = {
            'dark': {
                'PRIMARY_BACKGROUND': DarkTheme.PRIMARY_BACKGROUND.value,
                'SECONDARY_BACKGROUND': DarkTheme.SECONDARY_BACKGROUND.value,
                'PRIMARY_ACCENT': DarkTheme.PRIMARY_ACCENT.value,
                'SECONDARY_ACCENT': DarkTheme.SECONDARY_ACCENT.value
            },
            'light': {
                'PRIMARY_BACKGROUND': LightTheme.PRIMARY_BACKGROUND.value,
                'SECONDARY_BACKGROUND': LightTheme.SECONDARY_BACKGROUND.value,
                'PRIMARY_ACCENT': LightTheme.PRIMARY_ACCENT.value,
                'SECONDARY_ACCENT': LightTheme.SECONDARY_ACCENT.value
            }
        }

        for mode, theme in modes.items():
            self.app.design[mode].primary = Color.from_hsl(
                hue,
                *theme['PRIMARY_BACKGROUND']
            )
            self.app.design[mode].secondary = Color.from_hsl(
                hue,
                *theme['SECONDARY_BACKGROUND']
            )
            self.app.design[mode].background = Color.from_hsl(
                hue,
                *theme['SECONDARY_ACCENT']
            )
            self.app.design[mode].accent = Color.from_hsl(
                hue,
                *theme['PRIMARY_ACCENT']
            )

        self.app.dark = not self.app.dark
        self.app.dark = not self.app.dark

    def create_game_mode_selector(self) -> Selector:
        """
        Creates a selector for game difficulty levels.

        :return: Configured game mode Selector.
        :rtype: Selector
        """

        selector = Selector(
            options=['Easy', 'Medium', 'Hard'],
            classes='bordered'
        )
        selector.current_index = 0
        selector.border_title = 'Difficulty'
        return selector

    def create_play_button(self) -> Button:
        """
        Creates the play button for starting the game.

        :return: Configured Play button.
        :rtype: Button
        """

        button = Button("Play", id="play_button", classes='bordered')
        button.styles.width = 40
        return button

    def compose(self) -> ComposeResult:
        """
        Yields the layout components for the MainScreen.

        :return: Layout components for the screen.
        :rtype: ComposeResult
        """

        yield Horizontal(
            Label(f'{Icons.BOMB.value} Minesweeper Game {Icons.BOMB.value}'),
            classes='header'
        )
        yield self.main_container
        yield ControlsFooter(
            bindings={
                f'{Icons.UP.value} {Icons.DOWN.value} / w, s ': 'Up & Down',
                f'{Icons.LEFT.value} {Icons.RIGHT.value} / a, d ': 'Switch',
                'enter': 'Start Game'
            }
        )

    def get_focused_widget(self) -> int | None:
        """
        Returns the index of the currently focused widget.

        :return: Index of the focused widget or None.
        :rtype: int or None
        """

        for index, widget in enumerate(self.main_container.children):
            if widget.has_focus:
                return index

    def action_next_widget(self) -> None:
        """
        Focuses the next widget in the container.

        :return: None
        """

        focused = self.get_focused_widget()
        next_widget_index = (focused + 1) % len(self.main_container.children)
        self.main_container.children[next_widget_index].focus()

    def action_previous_widget(self) -> None:
        """
        Focuses the previous widget in the container.

        :return: None
        """

        focused = self.get_focused_widget()
        next_widget_index = (focused - 1) % len(self.main_container.children)
        self.main_container.children[next_widget_index].focus()

    def validate_player_name(self) -> str | None:
        """
        Validates and returns the player name if valid.

        :return: Validated player name or None.
        :rtype: str or None
        """

        player_name = self.input_field.value.strip()

        if len(player_name) < 3:
            self.input_field.value = ''
            self.input_field.placeholder = (
                'Use at least 3 letters'
                if player_name
                else 'Please enter your name'
            )
            self.main_container.children[0].focus()
            return

        self.input_field.value = ''
        return player_name.capitalize()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handles button presses to start the game with the player name.

        :param event: The button press event.
        :type event: Button.Pressed
        :return: None
        """

        player_name = self.validate_player_name()
        if player_name and event.button.id == "play_button":
            game_mode = self.game_mode_selector.value
            self.app.push_screen(
                GameScreen(
                    game_mode=game_mode,
                    player_name=player_name
                )
            )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """
        Moves focus to the next widget when input is submitted.

        :param event: The input submission event.
        :type event: Input.Submitted
        :return: None
        """

        self.action_next_widget()


class GameScreen(Screen):
    """
    Screen for the game where the Minesweeper game is played.

    Attributes:
        BINDINGS (List[Tuple[str, str]]): Key bindings for quitting the game.
    """

    BINDINGS = [
        ('escape, q', 'quit_game')
    ]

    def __init__(
            self,
            game_mode: str,
            player_name: str,
            **kwargs
    ):
        """
        Initializes the GameScreen with game mode and player name.

        :param game_mode: The selected game mode.
        :type game_mode: str
        :param player_name: The name of the player.
        :type player_name: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: None
        """

        super().__init__(**kwargs)
        self.player_name = player_name
        self.game_mode = GameMode[game_mode.upper()].value
        self.grid_size = self.game_mode['grid_size']
        self.mine = self.game_mode['mine']
        self.start_time = None
        self.flag_counter = Digits(
            value='00',
            classes='digits'
        )
        self.timer = Digits(
            value='00:00',
            classes='digits'
        )
        self.game_board = MinefieldUI(
            grid_size=self.grid_size,
            number_of_mine=self.mine,
            on_game_over=lambda x: self.toggle_game_over_modal(x),
            on_flag=lambda x: self.update_flag_counter(x)
        )
        self.update_flag_counter(self.mine)

    def compose(self) -> ComposeResult:
        """
        Yields the layout components for the GameScreen.

        :return: Layout components for the screen.
        :rtype: ComposeResult
        """

        yield Horizontal(
            self.flag_counter,
            Container(Label(f'Player: {self.player_name}'), classes='title'),
            self.timer,
            classes='header'
        )
        yield Container(
            self.game_board,
            classes='main_container'
        )
        yield ControlsFooter(
            bindings={
                'esc/q': 'Quit',
                f'{Icons.UP.value} '
                f'{Icons.LEFT.value} '
                f'{Icons.DOWN.value} '
                f'{Icons.RIGHT.value} / w, a, s, d ': 'Move',
                'enter': 'Hit',
                'space/f': 'Place flag'
            }
        )

    def on_key(self, event: events.Key) -> None:
        """
        Handles key events to start the timer when appropriate.

        :param event: The key event.
        :type event: events.Key
        :return: None
        """

        if event.key in ('enter', 'space') and not self.game_board.is_playing:
            self.start_timer()

    def start_timer(self) -> None:
        """
        Starts the game timer and updates it every second.

        :return: None
        """

        self.start_time = time.time()
        self.update_timer()
        self.set_interval(1, self.update_timer)

    def update_timer(self) -> None:
        """
        Updates the timer display with elapsed time.

        :return: None
        """

        if self.game_board.is_playing:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            self.timer.update(f'{minutes:02}:{seconds:02}')

    def update_flag_counter(self, value: int) -> None:
        """
        Updates the flag counter display.

        :param value: The number of remaining flags.
        :type value: int
        :return: None
        """

        self.flag_counter.update(f'{value:02}')

    def action_quit_game(self) -> None:
        """
        Handles quitting the game and returning to the previous screen.

        :return: None
        """

        self.app.pop_screen()

    def toggle_game_over_modal(self, completed):
        """
        Displays the game over modal with the result message.

        :param completed: Whether the game was completed successfully.
        :type completed: bool
        :return: None
        """

        modal = GameOverScreen(
            player_name=self.player_name,
            timer=self.timer.value,
            completed=completed
        )
        self.app.push_screen(modal)


class MinesweeperApp(App):
    """
    Main application class for the Minesweeper game.

    Attributes:
        CSS_PATH (str): Path to the CSS file for styling.
    """

    CSS_PATH = "style.tcss"

    def on_mount(self) -> None:
        """
        Called when the application is mounted. Pushes the MainScreen
        onto the screen stack.

        :return: None
        """

        self.push_screen(MainScreen())


if __name__ == "__main__":
    MinesweeperApp().run()
