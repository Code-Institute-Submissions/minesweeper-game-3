from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Header, Footer


class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(Button("Go to Second Screen", id="go_to_second"))
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_to_second":
            self.app.push_screen(GameScreen())


class GameScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(Button("Back to Main Screen", id="go_to_main"))
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_to_main":
            self.app.pop_screen()


class MinesweeperApp(App):
    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    MinesweeperApp().run()
