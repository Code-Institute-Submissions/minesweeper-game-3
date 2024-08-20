from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.screen import Screen
from textual.widgets import Button, Label, Footer, Select


class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label('<------ Minesweeper Game ------>'),
            classes='header'
        )
        yield Container(
            Select((line, line) for line in ['Easy', 'Medium', 'Hard']),
            Button("Go to Second Screen", id="go_to_second")
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_to_second":
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
