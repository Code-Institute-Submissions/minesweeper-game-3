from typing import List, Callable, Optional, Tuple

from textual import events
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static
import numpy as np
from scipy.ndimage import label
from configurations import Icons


class Selector(Static, can_focus=True):
    """
    A class representing a selectable component that allows the user
    to choose from a list of options. It provides functionality to
    navigate through the options using left/right arrows
    or 'a'/'d' keys.

    Attributes:
        BINDINGS (List[Tuple[str, str]]): Key bindings for navigation.
        DEFAULT_CSS (str): CSS styling for the component.
    """

    BINDINGS = [
        ('left, a', 'previous_option'),
        ('right, d', 'next_option')
    ]

    DEFAULT_CSS = """
    Selector {
        background: $panel;

        &:focus {
            background: $accent;
        }
    }
    """

    def __init__(
            self,
            options: Optional[List[str]] = None,
            current_index: int = 0,
            value: Optional[str] = None,
            on_change: Optional[Callable] = None,
            width: int = 40,
            **kwargs
    ):
        """
        Initializes the Selector with given options and configuration.

        :param options: List of options to choose from.
        :type options: List[str], optional
        :param current_index: Index of the selected option.
        :type current_index: int
        :param value: The current selected value.
        :type value: str, optional
        :param on_change: Callback to invoke on option change.
        :type on_change: Callable, optional
        :param width: Width of the Selector component.
        :type width: int
        :param kwargs: Additional keyword arguments.
        :type kwargs: str
        :return: None
        """

        super().__init__(**kwargs)
        self.options = options if options is not None else []
        self.current_index = current_index
        self.value = value
        self.on_change = on_change
        self.width = self.styles.width = width

    def on_mount(self) -> None:
        """
        Called when the Selector is mounted. Initializes the value if
        options are provided.

        :return: None
        """

        if self.options:
            self.update_text()
            self.value = self.options[self.current_index]

    def action_next_option(self) -> None:
        """
        Moves to the next option in the list and updates the display.

        :return: None
        """

        self._update_index(increment=True)

    def action_previous_option(self) -> None:
        """
        Moves to the previous option in the list and updates the display.

        :return: None
        """

        self._update_index(increment=False)

    def _update_index(self, increment: bool) -> None:
        """
        Updates the current index based on the navigation direction.

        :param increment: True for moving to the next option,
                          False for the previous.
        :type increment: bool
        :return: None
        """

        direction = 1 if increment else -1
        self.current_index = (
            self.current_index + direction
        ) % len(self.options)
        self.update_text()
        self.update_value()

    def update_text(self) -> None:
        """
        Updates the displayed text to reflect the current option.

        :return: None
        """

        area_width = self.width - 6 if self.styles.border else self.width - 4
        centered_text = self.options[self.current_index].center(area_width)
        self.update(f' {Icons.LEFT.value}{centered_text}{Icons.RIGHT.value} ')

    def update_value(self) -> None:
        """
        Updates the value attribute and calls the on_change callback
        if defined.

        :return: None
        """

        self.value = self.options[self.current_index]
        if callable(self.on_change):
            self.on_change(self.value)


class MinefieldUI(Grid):
    """
    A user interface for a Minefield game that manages the grid of buttons,
    interactions, and game logic.

    Attributes:
        BINDINGS (List[Tuple[str, str]]): Key bindings for flag toggling.
    """

    BINDINGS = [
        ('space, f', 'toggle_flag')
    ]

    def __init__(
            self,
            grid_size: Optional[Tuple[int, int]] = (10, 10),
            number_of_mine: Optional[int] = 10,
            is_playing: bool = False,
            on_game_over: Optional[Callable] = None,
            on_flag: Optional[Callable] = None,
            **kwargs
    ):
        """
        Initializes the MinefieldUI with grid size, mine count, and callbacks.

        :param grid_size: Dimensions of the grid (cols, rows).
        :type grid_size: Tuple[int, int], optional
        :param number_of_mine: Number of mines in the grid.
        :type number_of_mine: int, optional
        :param is_playing: True if the game is active.
        :type is_playing: bool
        :param on_game_over: Callback to invoke when the game ends.
        :type on_game_over: Callable, optional
        :param on_flag: Callback to invoke when a flag is toggled.
        :type on_flag: Callable, optional
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: None
        """

        super().__init__(**kwargs)
        self.is_game_over = False
        self.is_playing = is_playing
        self.on_game_over = on_game_over
        self.on_flag = on_flag
        self.placed_flags = set()
        self.number_of_mine = number_of_mine
        self.grid_width, self.grid_height = grid_size
        self.game = MinefieldLogic(
            cols=self.grid_width,
            rows=self.grid_height,
            number_of_mines=number_of_mine
        )
        self.game_matrix = self.game.game_matrix
        self.flat_game_matrix = self.game_matrix.flatten()
        self.focused_button_index = 0
        self.setup_styles()
        self.build()

    def setup_styles(self) -> None:
        """
        Sets the grid and UI component styles.

        :return: None
        """

        self.styles.grid_size_columns = self.grid_width
        self.styles.grid_size_rows = self.grid_height
        self.styles.width = self.grid_width * 3 + 2
        self.styles.height = self.grid_height + 2

    def build(self) -> None:
        """
        Builds the grid by adding buttons with alternating styles.

        :return: None
        """

        for i in range(self.grid_width * self.grid_height):
            color_class = 'primary-bg' if i % 2 else 'secondary-bg'
            self.compose_add_child(
                Button(
                    label='',
                    classes=f'game_button {color_class}',
                    id=f'id_{i}'
                )
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handles button press events to start the game or uncover cells.

        :param event: The button pressed event.
        :type event: Button.Pressed
        :return: None
        """

        if not self.is_playing and not event.button.has_class('surface-bg'):
            self.is_playing = True

        value = self.get_value_by_index(self.focused_button_index)
        if value and self.is_playing:
            self.handle_button_press(value)
        else:
            self.uncover_connected_zeros()

    def handle_button_press(self, value: int) -> None:
        """
        Processes the button press based on its value.

        :param value: The value of the pressed button.
        :type value: int
        :return: None
        """

        if value >= 9:
            self.game_over(completed=False)
        else:
            self.set_button(self.focused_button_index)

    def on_mount(self):
        """
        Called when the component is mounted to update the focus.

        :return: None
        """

        self.update_focus()

    def update_focus(self) -> None:
        """
        Updates the focus to the currently selected button.

        :return: None
        """

        button = self.get_child_by_id(f'id_{self.focused_button_index}')
        if button:
            button.focus()

    def on_key(self, event: events.Key) -> None:
        """
        Handles key events to navigate through the grid.

        :param event: The key event.
        :type event: events.Key
        :return: None
        """

        button_index = self.focused_button_index

        if event.key in ('up', 'w'):
            if button_index >= self.grid_width:
                self.focused_button_index -= self.grid_width
        elif event.key in ('down', 's'):
            if button_index < (self.grid_width * (self.grid_height - 1)):
                self.focused_button_index += self.grid_width
        elif event.key in ('left', 'a'):
            if button_index % self.grid_width != 0:
                self.focused_button_index -= 1
        elif event.key in ('right', 'd'):
            if button_index % self.grid_width != self.grid_width - 1:
                self.focused_button_index += 1

        self.update_focus()

    def action_toggle_flag(self) -> None:
        """
        Toggles a flag on the currently focused cell.

        :return: None
        """

        if not self.is_playing and not self.is_game_over:
            self.is_playing = True

        button = self.children[self.focused_button_index]
        if not button.has_class('surface-bg'):
            position = self.index_to_position(self.focused_button_index)
            increment = 0

            if not button.label and self.number_of_mine > 0:
                button.label = f'{Icons.FLAG.value}'
                increment = -1
            elif button.label:
                button.label = ''
                increment = 1

            self.update_flag(increment, position)

            if not self.number_of_mine and self.game.validate_flags(
                    self.placed_flags):
                self.game_over(completed=True)

    def update_flag(self, increment: int, position: tuple) -> None:
        """
        Updates the flag count and triggers flag events.

        :param increment: The increment for the flag count.
        :type increment: int
        :param position: The grid position of the flag.
        :type position: tuple
        :return: None
        """

        self.number_of_mine += increment

        if increment > 0:
            self.placed_flags.remove(position)
        elif increment < 0:
            self.placed_flags.add(position)

        if callable(self.on_flag) and self.is_playing:
            self.on_flag(self.number_of_mine)

    def uncover_connected_zeros(self) -> None:
        """
        Uncovers all connected cells with zero value.

        :return: None
        """

        position = self.index_to_position(self.focused_button_index)
        positions = self.game.get_connected_component(position)

        for pos in positions:
            self.set_button(self.position_to_index(pos))

    def position_to_index(self, position: tuple) -> int:
        """
        Converts a grid position to an index.

        :param position: The grid position.
        :type position: tuple
        :return: The corresponding index.
        :rtype: int
        """

        return position[0] * self.grid_width + position[1]

    def index_to_position(self, index: int) -> tuple:
        """
        Converts an index to a grid position.

        :param index: The index in the flattened grid.
        :type index: int
        :return: The corresponding grid position.
        :rtype: tuple
        """

        return divmod(index, self.grid_width)

    def uncover_all(self) -> None:
        """
        Uncovers all the buttons in the grid.

        :return: None
        """

        self.is_playing = False
        for button_index in range(len(self.children)):
            self.set_button(button_index)

    def get_value_by_index(self, index: int) -> int:
        """
        Gets the value of the cell at the specified index.

        :param index: The index in the flattened grid.
        :type index: int
        :return: The value of the cell.
        :rtype: int
        """

        return int(self.flat_game_matrix[index])

    def set_button(self, button_index: int) -> None:
        """
        Sets the label and style for the button based on the cell value.

        :param button_index: The index of the button in the grid.
        :type button_index: int
        :return: None
        """

        if button_index < 0 or button_index >= len(self.children):
            return

        position = self.index_to_position(button_index)
        if position in self.placed_flags:
            self.update_flag(increment=1, position=position)

        button = self.children[button_index]
        value = self.get_value_by_index(button_index)
        if value >= 9:
            button.label = Icons.MINE.value
            button.classes = 'surface-bg block-red'
        elif value >= 3:
            button.label = str(value)
            button.classes = 'surface-bg block-orange'
        elif value == 2:
            button.label = str(value)
            button.classes = 'surface-bg block-green'
        elif value == 1:
            button.label = str(value)
            button.classes = 'surface-bg block-blue'
        else:
            button.label = ' '
            button.classes = 'surface-bg'

    def game_over(self, completed: bool = False) -> None:
        """
        Handles game over logic by uncovering all cells and triggering
        the on_game_over callback.

        :param completed: Whether the game was completed successfully.
        :type completed: bool, optional
        :return: None
        """

        self.uncover_all()
        self.is_game_over = True
        if callable(self.on_game_over):
            self.on_game_over(completed)


class MinefieldLogic:
    """
    Manages the logic for a Minesweeper game, including mine placement
    and validation of flags.

    Attributes:
        cols (int): Number of columns in the game grid.
        rows (int): Number of rows in the game grid.
        number_of_mines (int): Number of mines to place.
        game_matrix (np.ndarray): Matrix representing the game state.
        mask (np.ndarray): Mask used for mine placement.
        components (np.ndarray): Labeled components of the game matrix.
    """

    def __init__(
            self,
            cols: int = 10,
            rows: int = 10,
            number_of_mines: int = 10
    ):
        """
        Initializes the MinefieldLogic with given dimensions and mines.

        :param cols: Number of columns in the grid.
        :type cols: int
        :param rows: Number of rows in the grid.
        :type rows: int
        :param number_of_mines: Number of mines to be placed.
        :type number_of_mines: int
        :return: None
        """

        self.cols = cols
        self.rows = rows
        self.number_of_mines = number_of_mines
        self.game_matrix = np.zeros((self.rows, self.cols), dtype=np.uint8)
        self.mask = np.ones((3, 3), dtype=int)
        self.initialize_mines()
        self.components: np.ndarray = label(
            self.game_matrix == 0,
            structure=self.mask
        )[0]

    def initialize_mines(self) -> None:
        """
        Places mines randomly in the game matrix.

        Updates the game matrix with randomly placed mines based on
        the number_of_mines attribute.

        :return: None
        """

        matrix = self.game_matrix.copy()
        random_mines = np.random.choice(
            self.game_matrix.size,
            self.number_of_mines,
            replace=False
        )

        for mine in random_mines:
            mask = self.mask.copy()
            mask[1, 1] = 9
            pos_y, pos_x = divmod(mine, self.cols)
            pos_y, pos_x = pos_y - 1, pos_x - 1

            if pos_x < 0:
                mask = mask[:, 1:]
                pos_x = 0
            elif pos_x > self.cols - 3:
                mask = mask[:, :-1]

            if pos_y < 0:
                mask = mask[1:, :]
                pos_y = 0
            elif pos_y > self.rows - 3:
                mask = mask[:-1, :]

            new_matrix = self.game_matrix.copy()
            new_matrix[
                pos_y:pos_y + mask.shape[0],
                pos_x:pos_x + mask.shape[1]
            ] = mask
            matrix += new_matrix

        self.game_matrix = matrix

    def validate_flags(self, flags: set) -> bool:
        """
        Checks if flagged positions match the mine locations.

        :param flags: Set of flagged positions.
        :type flags: set
        :return: True if flags match mine positions, otherwise False.
        :rtype: bool
        """

        positions = map(tuple, np.argwhere(self.game_matrix >= 9).tolist())
        return not bool(set.difference(set(positions), flags))

    def get_connected_component(self, position: list | tuple) -> np.ndarray:
        """
        Retrieves the connected component of a given position.

        :param position: Coordinates of the position.
        :type position: list or tuple
        :return: Array of connected component positions.
        :rtype: np.ndarray
        """

        zeros = np.zeros_like(self.game_matrix, dtype=np.uint8)
        component = np.argwhere(self.components == self.components[position])

        for pos in component:
            pos_start = np.clip(pos - 1, 0, [self.rows - 1, self.cols - 1])
            pos_end = np.clip(pos + 1, 0, [self.rows - 1, self.cols - 1])

            zeros[pos_start[0]:pos_end[0] + 1, pos_start[1]:pos_end[1] + 1] = 1

        return np.argwhere(zeros)


class GameOverScreen(ModalScreen):
    """
    Displays the game over screen with result messages and buttons.

    Attributes:
        BINDINGS (List[Tuple[str, str]]): Key bindings for screen actions.
    """

    BINDINGS = [
        ('escape', 'close_modal'),
        ('left, right, a, d', 'next_button')
    ]

    def __init__(
            self,
            player_name: str,
            timer: str,
            completed: bool = False,
            on_close: Callable = None,
            **kwargs
    ):
        """
        Initializes the GameOverScreen with result message and buttons.

        :param player_name: Name of the player.
        :type player_name: str
        :param timer: Time taken to complete the game.
        :type timer: str
        :param completed: Whether the game was completed successfully.
        :type completed: bool
        :param on_close: Callback to invoke when closing the screen.
        :type on_close: Callable, optional
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: None
        """

        super().__init__(**kwargs)
        self.on_close = on_close
        self.result_message = (
            f'Congratulations, {player_name}! You successfully found all '
            f'the mines in {timer}s! Great job!'
            if completed
            else (
                f'Oops, {player_name}! You hit a mine and the game is over. '
                'Better luck next time!'
            )
        )
        self.content = Grid(
            Label(self.result_message),
            Button('Exit', id='exit', classes='bordered'),
            Button('Show', id='show', classes='bordered'),
        )

    def compose(self) -> ComposeResult:
        """
        Yields the content to be displayed on the screen.

        :return: The content of the screen.
        :rtype: ComposeResult
        """

        yield self.content

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handles button presses to either exit or show results.

        :param event: The button press event.
        :type event: Button.Pressed
        :return: None
        """

        if event.button.id == "exit":
            self.app.pop_screen()

        self.app.pop_screen()

    def action_close_modal(self) -> None:
        """
        Closes the modal and triggers the on_close callback if defined.

        :return: None
        """

        if callable(self.on_close):
            self.on_close()

        self.app.pop_screen()

    def action_next_button(self) -> None:
        """
        Cycles focus to the next button in the content.

        :return: None
        """

        buttons = self.content.children[1:]
        current_focus = next(button for button in buttons if button.has_focus)
        current_index = buttons.index(current_focus)
        next_index = (current_index + 1) % len(buttons)
        buttons[next_index].focus()


class ControlsFooter(Horizontal):
    """
    Displays a footer with control bindings and their descriptions.

    Attributes:
        DEFAULT_CSS (str): CSS styling for the footer component.
    """

    DEFAULT_CSS = """
    ControlsFooter {
        height: 1;
        padding: 0 1;
        background: $background;
    }
    """

    def __init__(
            self,
            bindings: dict | None = None,
            **kwargs
    ):
        """
        Initializes the ControlsFooter with bindings.

        :param bindings: Dictionary of key-bindings and descriptions.
        :type bindings: dict or None
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: None
        """

        super().__init__(**kwargs)
        self.bindings = bindings
        self.build()

    def build(self) -> None:
        """
        Constructs the footer by adding labels for each binding.

        :return: None
        """

        for key, description in self.bindings.items():
            self.compose_add_child(
                Label(f'[bold]{key}:[/bold] {description} [bold]|[/bold] '))
