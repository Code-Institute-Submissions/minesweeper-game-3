from typing import List, Callable

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Grid
from textual.screen import Screen
from textual.widgets import Button, Label, Static, Footer
from textual.color import Color
from configurations import Hue, DarkTheme, LightTheme, GameMode


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
    def __init__(self, grid_size=(10, 10), **kwargs):
        super().__init__(**kwargs)
        self.grid_size = grid_size
        self.grid_width, self.grid_height = grid_size
        self.styles.grid_size_columns = self.grid_size[0]
        self.styles.grid_size_rows = self.grid_size[1]
        self.styles.width = self.grid_width * 3 + 2
        self.styles.height = self.grid_height + 2
        self.focused_button_index = 0
        self.build()

    def build(self) -> None:
        for i in range(self.grid_size[0] * self.grid_size[1]):
            color_class = 'primary-bg' if i % 2 else 'secondary-bg'
            self.compose_add_child(Button(' ', classes=f'game_button {color_class}', id=f'id_{i}'))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.button.classes = 'surface-bg'
        event.button.label = '1'

    def on_mount(self):
        self.focused_button_index = 0
        self.update_focus()

    def update_focus(self):
        print(self.focused_button_index)
        button = self.get_child_by_id(f'id_{self.focused_button_index}')
        if button:
            button.focus()

    def on_key(self, event):
        if event.key == "up":
            if self.focused_button_index >= self.grid_size[0]:
                self.focused_button_index -= self.grid_size[0]
        elif event.key == "down":
            if self.focused_button_index < (self.grid_size[0] * (self.grid_size[1] - 1)):
                self.focused_button_index += self.grid_size[0]
        elif event.key == "left":
            if self.focused_button_index % self.grid_size[0] != 0:
                self.focused_button_index -= 1
        elif event.key == "right":
            if self.focused_button_index % self.grid_size[0] != self.grid_size[0] - 1:
                self.focused_button_index += 1

        self.update_focus()


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
        print(self.app.design['dark'].__dict__)
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
        self.main_container = Container(
            Button("Back to Main Screen", id="go_to_main")
        )

    def compose(self) -> ComposeResult:
        yield Horizontal(Label(f'<------ Minesweeper Game ------>'), classes='header')
        yield Container(
            GameBoard(grid_size=self.grid_size),
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
