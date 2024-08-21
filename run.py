from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.screen import Screen
from textual.widgets import Button, Label, Static




class GameSelect(Static, can_focus=True):
    BINDINGS = [
        ('left', 'previous_mode'),
        ('right', 'next_mode')
    ]
    GAME_MODES = ['Easy', 'Medium', 'Hard']
    DEFAULT_CSS = """
    GameSelect {
        width: 21;
        height: 3;
        background: $panel;
        content-align: center middle;
        margin: 1 0;
    }
    
    GameSelect:focus {
        background: #535e6c;
    }
    """
    current_game_mode = 0


    def on_mount(self) -> None:
        self.update_label()

    def action_next_mode(self) -> None:
        self.current_game_mode = (self.current_game_mode + 1) % len(self.GAME_MODES)
        self.update_label()

    def action_previous_mode(self) -> None:
        self.current_game_mode = (self.current_game_mode - 1) % len(self.GAME_MODES)
        self.update_label()

    def update_label(self) -> None:
        self.update(f'\u2B9C {self.GAME_MODES[self.current_game_mode]} \u2B9E')


class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label('<------ Minesweeper Game ------>'),
            classes='header'
        )
        yield Container(
            GameSelect(),
            Button("Go to Second Screen", id="go_to_second"),
            classes='main_container'

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
