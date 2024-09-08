from typing import List, Callable

from textual import events
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static
from configurations import Icons
import numpy as np
from scipy.ndimage import label


class Selector(Static, can_focus=True):
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
            options: List[str] | None = None,
            current_index: int = 0,
            value: str | None = None,
            on_change: Callable = None,
            width: int = 30,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.options = options
        self.current_index = current_index
        self.value = value
        self.on_change = on_change
        self.width = self.styles.width = width

    def on_mount(self) -> None:
        self.update_text()
        self.value = self.options[self.current_index]

    def action_next_option(self) -> None:
        self.current_index = (self.current_index + 1) % len(self.options)
        self.update_text()
        self.update_value()

    def action_previous_option(self) -> None:
        self.current_index = (self.current_index - 1) % len(self.options)
        self.update_text()
        self.update_value()

    def update_text(self) -> None:
        text_area_width = self.width - 6 if self.styles.border else self.width - 4
        self.update(f' \u2B9C{self.options[self.current_index].center(text_area_width)}\u2B9E ')

    def update_value(self) -> None:
        self.value = self.options[self.current_index]
        if callable(self.on_change):
            self.on_change(self.value)


class MinefieldUI(Grid):
    BINDINGS = [
        ('space, f', 'toggle_flag')
    ]

    def __init__(
            self,
            grid_size: tuple | None = (10, 10),
            number_of_mine: int | None = 10,
            is_playing: bool = False,
            on_game_over: Callable = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.is_playing = is_playing
        self.on_game_over = on_game_over
        self.number_of_mine = number_of_mine
        self.grid_width, self.grid_height = grid_size
        self.game = MinefieldLogic(cols=self.grid_width, rows=self.grid_height, number_of_mines=self.number_of_mine)
        self.game_matrix = self.game.game_matrix
        self.flat_game_matrix = self.game_matrix.flatten()
        self.styles.grid_size_columns = self.grid_width
        self.styles.grid_size_rows = self.grid_height
        self.styles.width = self.grid_width * 3 + 2
        self.styles.height = self.grid_height + 2
        self.focused_button_index = 0
        self.build()

    def build(self) -> None:
        for i in range(self.grid_width * self.grid_height):
            color_class = 'primary-bg' if i % 2 else 'secondary-bg'
            self.compose_add_child(Button('', classes=f'game_button {color_class}', id=f'id_{i}'))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if not self.is_playing and not event.button.has_class('surface-bg'):
            self.is_playing = True

        if value := self.get_value_by_index(self.focused_button_index):
            if value >= 9:
                self.uncover_all()
                self.is_playing = False
                self.game_over(completed=False)
                # self.app.push_screen(GameOverScreen())
            else:
                self.set_button(self.focused_button_index)
        else:
            self.uncover_connected_zeros()

    def on_mount(self):
        self.update_focus()

    def update_focus(self) -> None:
        button = self.get_child_by_id(f'id_{self.focused_button_index}')
        if button:
            button.focus()

    def on_key(self, event: events.Key) -> None:
        if event.key in ('up', 'w'):
            if self.focused_button_index >= self.grid_width:
                self.focused_button_index -= self.grid_width
        elif event.key in ('down', 's'):
            if self.focused_button_index < (self.grid_width * (self.grid_height - 1)):
                self.focused_button_index += self.grid_width
        elif event.key in ('left', 'a'):
            if self.focused_button_index % self.grid_width != 0:
                self.focused_button_index -= 1
        elif event.key in ('right', 'd'):
            if self.focused_button_index % self.grid_width != self.grid_width - 1:
                self.focused_button_index += 1

        self.update_focus()

    def action_toggle_flag(self) -> None:
        button = self.children[self.focused_button_index]
        button.label = '\u2691' if not button.label else ''

    def uncover_connected_zeros(self) -> None:
        position = self.index_to_position(self.focused_button_index)
        positions = self.game.get_connected_component_with_frame(position)

        for pos in positions:
            self.set_button(self.position_to_index(pos))

    def position_to_index(self, position: list | tuple) -> int:
        return position[0] * self.grid_width + position[1]

    def index_to_position(self, index: int) -> tuple:
        return divmod(index, self.grid_width)

    def uncover_all(self) -> None:
        for button_index in range(len(self.children)):
            self.set_button(button_index)

    def get_value_by_index(self, index: int) -> int:
        return int(self.flat_game_matrix[index])

    def set_button(self, button_index: int) -> None:
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
            button.label, button.classes = ' ', 'surface-bg'

    def game_over(self, completed: bool = False) -> None:
        if callable(self.on_game_over):
            self.on_game_over(completed)


class MinefieldLogic:
    def __init__(
            self,
            cols: int = 10,
            rows: int = 10,
            number_of_mines: int = 10
    ):
        self.cols = cols
        self.rows = rows
        self.number_of_mines = number_of_mines
        self.game_matrix = np.zeros((self.rows, self.cols), dtype=np.uint8)
        self.mask = np.ones((3, 3), dtype=int)
        self.initialize_mines()
        self.labeled_components: np.ndarray = label(self.game_matrix == 0, structure=self.mask)[0]

    def initialize_mines(self) -> None:
        matrix = self.game_matrix.copy()
        random_mines = np.random.choice(self.game_matrix.size, self.number_of_mines, replace=False)

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
            new_matrix[pos_y:pos_y + mask.shape[0], pos_x:pos_x + mask.shape[1]] = mask
            matrix += new_matrix

        self.game_matrix = matrix

    def get_connected_component(self, position: list | tuple) -> np.ndarray:
        return np.argwhere(self.labeled_components == self.labeled_components[position])

    def get_connected_component_with_frame(self, position: list | tuple) -> np.ndarray:
        zeros = np.zeros_like(self.game_matrix, dtype=np.uint8)
        component = self.get_connected_component(position)

        for position in component:
            pos_start = np.clip(position - 1, 0, [self.rows - 1, self.cols - 1])
            pos_end = np.clip(position + 1, 0, [self.rows - 1, self.cols - 1])

            zeros[pos_start[0]:pos_end[0] + 1, pos_start[1]:pos_end[1] + 1] = 1

        return np.argwhere(zeros)


class GameOverScreen(ModalScreen):
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
        yield self.content

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            self.app.pop_screen()

        self.app.pop_screen()

    def action_close_modal(self) -> None:
        if callable(self.on_close):
            self.on_close()

        self.app.pop_screen()

    def action_next_button(self) -> None:
        buttons = self.content.children[1:]
        current_focus = next(button for button in buttons if button.has_focus)
        current_index = buttons.index(current_focus)
        next_index = (current_index + 1) % len(buttons)
        buttons[next_index].focus()


class ControlsFooter(Horizontal):
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
        super().__init__(**kwargs)
        self.bindings = bindings
        self.build()

    def build(self) -> None:
        for key, description in self.bindings.items():
            self.compose_add_child(Label(f'[bold]{key}:[/bold] {description} [bold]|[/bold] '))
