from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import DirectoryTree, Input


class AlbumArtSelectModal(ModalScreen[Path | str]):

    BINDINGS = [Binding("escape", "exit", "exit album art select")]

    def compose(self) -> ComposeResult:
        self.add_class("center")
        self.filetree = DirectoryTree(".", id="album-art-select", classes="round-border")
        self.filetree.border_title = "select the album art"

        self.image_link_entry = Input(placeholder="https://...", id="image-link-entry", classes="round-border")
        self.image_link_entry.border_title = "image link"

        with Vertical(id="album-art-select-modal"):
            yield self.filetree
            yield self.image_link_entry

    @on(DirectoryTree.FileSelected)
    def on_directorytree_fileselected(self, event: DirectoryTree.FileSelected) -> None:
        self.dismiss(event.path)

    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        # TODO: validate link here before dismissing the scree, notify on fail
        self.dismiss(event.value)

    def action_exit(self) -> None:
        self.app.pop_screen()
