import logging
from pathlib import Path
from typing import List
from textual.app import ComposeResult
from rich_pixels import Pixels
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Input, Static
from textual.logging import TextualHandler

from util.config import load_config
from util.metadata import read_metadata, write_metadata
from util.query import track_getinfo

logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
)

class EditPage(Screen):

    BINDINGS = [
        Binding("ctrl+o", "write_out", "write out"), 
        Binding("ctrl+p", "previous", "previous"), 
        Binding("ctrl+n", "next", "next"), 
        Binding("ctrl+s", "search", "search")
    ]

    def __init__(self, files: List[Path]):
        super().__init__()
        self.files = files
        self.file_index = 0
        self.config = load_config(self.app)

    def compose(self) -> ComposeResult:
        self.title_input: Input = Input(
            placeholder="title", id="title", classes="round-border"
        )
        self.artist_input: Input = Input(
            placeholder="artist",
            id="artist",
            classes="round-border",
        )
        self.album_title_input: Input = Input(
            placeholder="album title",
            id="album-title",
            classes="round-border",
        )
        self.album_artist_input: Input = Input(
            placeholder="album artist",
            id="album-artist",
            classes="round-border",
        )
        self.album_art: Static = Static()
        self.push_data()

        with Horizontal():
            with Vertical():
                yield self.title_input
                yield self.artist_input
                yield self.album_title_input
                yield self.album_artist_input
            yield self.album_art
        yield Footer()

    def pull_data(self) -> tuple:
        data = (
            self.title_input.value,
            self.artist_input.value,
            self.album_title_input.value,
            self.album_artist_input.value,
            # TODO: implement album art
            None,
        )
        return data

    def push_data(self) -> None:
        data = read_metadata(self.files[self.file_index])

        self.title_input.value = data[0]
        self.artist_input.value = data[1]
        self.album_title_input.value = data[2]
        self.album_artist_input.value = data[3]

        # TODO: this whole file needs to have album art added
        image = Pixels.from_image(data[4].resize((60, 60)))
        self.album_art.update(image)

    def action_save(self) -> None:
        write_metadata(self.files[self.file_index], self.pull_data())
        # TODO: rename file, maybe should go in metadata utils?
        pass

    def action_next(self) -> None:
        self.file_index += 1
        self.push_data()
        self.refresh_bindings()

    def action_previous(self) -> None:
        self.file_index -= 1
        self.push_data()
        self.refresh_bindings()

    def action_search(self) -> None:
        self.refresh_bindings()
        data = self.pull_data()
        # TODO: error handle title or artist blank
        results = track_getinfo(self.config.lastfm_api_key, data[0], data[1])
        # if results:
        # self.push_data(results)
        # TODO: pull the title and artist then search lastfm
        # populate on success
        pass

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:  
        """Check if an action may run."""
        if action == "search" and self.config.lastfm_api_key == "":
            self.app.notify(
                "You need to provide a last.fm API key to look up song info!",
                severity="warning",
            )
            return None
        if action == "previous" and self.file_index == 0:
            return None
        if action == "next" and self.file_index == len(self.files) - 1:
            return None
        return True
