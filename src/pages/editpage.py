from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label


class EditPage(Screen):

    def compose(self) -> ComposeResult:
        yield Label("TODO")
