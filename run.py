from typing import List, Callable

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Grid
from textual.screen import Screen
from textual.widgets import Button, Label, Static, Footer
from textual.color import Color
from configurations import Hue, DarkTheme, LightTheme, GameMode, Icons
import numpy as np
from scipy.ndimage import label


class Selector(Static, can_focus=True):
    BINDINGS = [
        ('left', 'previous_option'),
        ('right', 'next_option')
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

    def on_mount(self):
        self.update_text()
        self.value = self.options[self.current_index]

    def action_next_option(self):
        self.current_index = (self.current_index + 1) % len(self.options)
        self.update_text()
        self.update_value()

    def action_previous_option(self):
        self.current_index = (self.current_index - 1) % len(self.options)
        self.update_text()
        self.update_value()

    def update_text(self):
        text_area_width = self.width - 6 if self.styles.border else self.width - 4
        self.update(f' \u2B9C{self.options[self.current_index].center(text_area_width)}\u2B9E ')

    def update_value(self):
        self.value = self.options[self.current_index]
        if callable(self.on_change):
            self.on_change(self.value)


class GameBoard(Grid):
    BINDINGS = [
        ('space, f', 'toggle_flag')
    ]

    def __init__(
            self,
            grid_size=(10, 10),
            number_of_mine=10,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.number_of_mine = number_of_mine
        self.grid_width, self.grid_height = grid_size
        self.game = Game(cols=self.grid_width, rows=self.grid_height, number_of_mines=self.number_of_mine)
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
        if value := self.get_value_by_index(self.focused_button_index):
            if value >= 9:
                self.uncover_all()
            else:
                self.set_button(self.focused_button_index)
        else:
            self.uncover_connected_zeros()

    def on_mount(self):
        self.focused_button_index = 0
        self.update_focus()

    def update_focus(self):
        button = self.get_child_by_id(f'id_{self.focused_button_index}')
        if button:
            button.focus()

    def on_key(self, event):
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

    def action_toggle_flag(self):
        button = self.children[self.focused_button_index]
        button.label = '\u2691' if not button.label else ''

    def uncover_connected_zeros(self):
        position = self.index_to_position(self.focused_button_index)
        positions = self.game.get_connected_component_with_frame(position)

        for pos in positions:
            button_index = self.position_to_index(pos)
            self.set_button(button_index)

    def position_to_index(self, position):
        return position[0] * self.grid_width + position[1]

    def index_to_position(self, index):
        return divmod(index, self.grid_width)

    def uncover_all(self):
        for button_index in range(len(self.children)):
            self.set_button(button_index)

    def get_value_by_index(self, index) -> int:
        return int(self.flat_game_matrix[index])

    def get_value_by_position(self, position) -> int:
        return int(self.game_matrix[position])

    def get_value(self, position):
        return self.game_matrix[position]

    def set_button(self, button_index: int):
        button = self.children[button_index]
        value = self.get_value_by_index(button_index)
        if value >= 9:
            button.label = Icons.MINE.value
            button.classes = f'surface-bg board-red'
        elif value >= 3:
            button.label = str(value)
            button.classes = 'surface-bg board-red'
        elif value == 2:
            button.label = str(value)
            button.classes = 'surface-bg board-green'
        elif value == 1:
            button.label = str(value)
            button.classes = 'surface-bg board-blue'
        else:
            button.label = ' '
            button.classes = 'surface-bg'


class Game:
    def __init__(
            self,
            cols=10,
            rows=10,
            number_of_mines=10
    ):
        self.cols = cols
        self.rows = rows
        self.number_of_mines = number_of_mines
        self.game_matrix = np.zeros((self.rows, self.cols), dtype=np.uint8)
        self.mask = np.ones((3, 3), dtype=int)
        self.initialize_mines()
        self.labeled_components = label(self.game_matrix == 0, structure=self.mask)[0]

    def initialize_mines(self):
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

    def get_connected_component(self, position):
        return np.argwhere(self.labeled_components == self.labeled_components[position])

    def get_connected_component_with_frame(self, position):
        zeros = np.zeros_like(self.game_matrix, dtype=np.uint8)
        component = self.get_connected_component(position)

        for position in component:
            pos_start = np.clip(position - 1, 0, [self.rows - 1, self.cols - 1])
            pos_end = np.clip(position + 1, 0, [self.rows - 1, self.cols - 1])

            zeros[pos_start[0]:pos_end[0] + 1, pos_start[1]:pos_end[1] + 1] = 1

        print(zeros)
        return np.argwhere(zeros)


class MainScreen(Screen):
    BINDINGS = [
        ('up', 'previous_widget'),
        ('down', 'next_widget')
    ]

    def __init__(self):
        super().__init__()
        self.set_color_theme('orange')
        self.theme_selector = self.create_theme_selector()
        self.color_selector = self.create_color_selector()
        self.game_mode_selector = self.create_game_mode_selector()
        self.play_button = self.create_play_button()
        self.main_container = Container(
            self.theme_selector,
            self.color_selector,
            self.game_mode_selector,
            self.play_button,
            classes='main_container'
        )

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

    def set_color_theme(self, color):
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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play_button":
            game_mode = self.game_mode_selector.value
            self.app.push_screen(GameScreen(game_mode))


class GameScreen(Screen):
    BINDINGS = [
        ('q', 'quit_game')
    ]

    def __init__(self, game_mode, **kwargs):
        super().__init__(**kwargs)
        self.game_mode = GameMode[game_mode.upper()].value
        self.grid_size = self.game_mode['grid_size']
        self.mine = self.game_mode['mine']
        self.game_board = GameBoard(grid_size=self.grid_size, number_of_mine=self.mine)

    def compose(self) -> ComposeResult:
        yield Horizontal(Label(f'<------ Minesweeper Game ------>'), classes='header')
        yield Container(
            self.game_board,
            classes='main_container'
        )
        yield Footer()

    def action_quit_game(self):
        self.app.pop_screen()


class MinesweeperApp(App):
    CSS_PATH = "style.tcss"

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    MinesweeperApp().run()
