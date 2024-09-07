from typing import List, Callable
import time

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Grid
from textual.screen import Screen, ModalScreen
from textual.widgets import Button, Label, Input, Static, Footer, Digits
from textual.color import Color
from configurations import Hue, DarkTheme, LightTheme, GameMode, Icons
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
            button.label, button.classes = Icons.MINE.value, f'surface-bg board-red'
        elif value >= 3:
            button.label, button.classes = str(value), 'surface-bg board-red'
        elif value == 2:
            button.label, button.classes = str(value), 'surface-bg board-green'
        elif value == 1:
            button.label, button.classes = str(value), 'surface-bg board-blue'
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


class MainScreen(Screen):
    BINDINGS = [
        ('up, w', 'previous_widget'),
        ('down, s', 'next_widget')
    ]

    def __init__(self):
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
        input_field = Input(
            placeholder='Please enter your name',
            type='text',
            max_length=10,
            classes='bordered'
        )
        input_field.border_title = 'Player'
        input_field.styles.text_style = 'bold'
        input_field.styles.width = 30
        input_field.styles.text_align = 'center'
        return input_field

    def create_theme_selector(self) -> Selector:
        selector = Selector(
            options=['Dark', 'Light'],
            classes='bordered',
            on_change=lambda x: setattr(self.app, 'dark', x == 'Dark')
        )
        selector.current_index = 0
        selector.border_title = 'Theme'
        return selector

    def create_color_selector(self) -> Selector:
        selector = Selector(
            options=['Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Red'],
            classes='bordered',
            on_change=lambda x: self.set_color_theme(x)
        )
        selector.current_index = 0
        selector.border_title = 'Color'
        return selector

    def set_color_theme(self, color: str) -> None:
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
            self.app.design[mode].primary = Color.from_hsl(hue, *theme['PRIMARY_BACKGROUND'])
            self.app.design[mode].secondary = Color.from_hsl(hue, *theme['SECONDARY_BACKGROUND'])
            self.app.design[mode].background = Color.from_hsl(hue, *theme['SECONDARY_ACCENT'])
            self.app.design[mode].accent = Color.from_hsl(hue, *theme['PRIMARY_ACCENT'])

        self.app.dark = not self.app.dark
        self.app.dark = not self.app.dark

    def create_game_mode_selector(self) -> Selector:
        selector = Selector(
            options=['Easy', 'Medium', 'Hard'],
            classes='bordered'
        )
        selector.current_index = 0
        selector.border_title = 'Difficulty'
        return selector

    def create_play_button(self) -> Button:
        button = Button("Play", id="play_button", classes='bordered')
        button.styles.width = 30
        return button

    def compose(self) -> ComposeResult:
        yield Horizontal(Label(f'<------ Minesweeper Game ------>'), classes='header')
        yield self.main_container
        yield Footer()

    def get_focused_widget(self) -> int:
        for index, widget in enumerate(self.main_container.children):
            if widget.has_focus:
                return index

    def action_next_widget(self) -> None:
        next_widget_index = (self.get_focused_widget() + 1) % len(self.main_container.children)
        self.main_container.children[next_widget_index].focus()

    def action_previous_widget(self) -> None:
        next_widget_index = (self.get_focused_widget() - 1) % len(self.main_container.children)
        self.main_container.children[next_widget_index].focus()

    def validate_player_name(self) -> str | None:
        if len(player_name := self.input_field.value) < 3:
            self.input_field.value = ''
            self.input_field.placeholder = 'Use at least 3 letter' if player_name else 'Please enter your name'
            self.main_container.children[0].focus()
            return

        self.input_field.value = ''
        return player_name.capitalize()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if (player_name := self.validate_player_name()) and event.button.id == "play_button":
            game_mode = self.game_mode_selector.value
            self.app.push_screen(GameScreen(game_mode=game_mode, player_name=player_name))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.action_next_widget()


class GameScreen(Screen):
    BINDINGS = [
        ('escape, q', 'quit_game')
    ]

    def __init__(
            self,
            game_mode: str,
            player_name: str,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.player_name = player_name
        self.game_mode = GameMode[game_mode.upper()].value
        self.grid_size = self.game_mode['grid_size']
        self.mine = self.game_mode['mine']
        self.game_board = MinefieldUI(grid_size=self.grid_size, number_of_mine=self.mine, on_game_over=lambda x: self.toggle_game_over_modal(x))
        self.start_time = None
        self.counter = Digits('99', classes='digits')
        self.timer = Digits('00:00', classes='digits')

    def compose(self) -> ComposeResult:
        yield Horizontal(
            self.counter,
            Container(Label(f'Player: {self.player_name}'), classes='title'),
            self.timer,
            classes='header'
        )
        yield Container(
            self.game_board,
            classes='main_container'
        )
        yield Footer()

    def on_key(self, event: events.Key) -> None:
        if event.key == 'enter' and not self.game_board.is_playing:
            print('start timer...')
            self.start_timer()

    def start_timer(self) -> None:
        self.start_time = time.time()
        self.update_timer()
        self.set_interval(1, self.update_timer)

    def update_timer(self) -> None:
        if self.game_board.is_playing:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            colon = ':' if seconds % 2 else ' '
            self.timer.update(f'{minutes:02}{colon}{seconds:02}')

    def action_quit_game(self) -> None:
        self.app.pop_screen()

    def toggle_game_over_modal(self, completed):
        modal = GameOverScreen(player_name=self.player_name, timer=self.timer.value, completed=completed)
        self.app.push_screen(modal)


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
            Button("Quit", id="quit", classes='bordered'),
            Button("Cancel", id="cancel", classes='bordered'),
        )

    def compose(self) -> ComposeResult:
        yield self.content

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
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


class MinesweeperApp(App):
    CSS_PATH = "style.tcss"

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    MinesweeperApp().run()
