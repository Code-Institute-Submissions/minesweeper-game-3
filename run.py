from typing import List, Callable

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Label, Static, Footer


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
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
            disabled: bool = False,
            options: List[str] | None = None,
            current_index: int = 0,
            value: str | None = None,
            on_change: Callable = None,
            width: int = 30
    ):
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.options = options
        self.current_index = current_index
        self.value = value
        self.on_change = on_change
        self.width = self.styles.width = width
        # self.update_text()


    def on_mount(self):
        self.update_text()

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




class MainScreen(Screen):
    game_mode_selector = Selector(options=['Easy', 'Medium', 'Hard'], classes='bordered')
    play_button = Button("Play", id="play_button", classes='bordered')
    play_button.styles.width = 30

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label('<------ Minesweeper Game ------>'),
            classes='header'
        )
        yield Container(
            self.game_mode_selector,
            self.play_button,
            classes='main_container'
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play_button":
            self.app.push_screen(GameScreen())



class GameScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label()
        yield Container(Button("Back to Main Screen", id="go_to_main"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_to_main":
            self.app.pop_screen()


class MinesweeperApp(App):
    CSS_PATH = "style.tcss"

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    MinesweeperApp().run()
