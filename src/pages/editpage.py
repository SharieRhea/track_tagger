from pathlib import Path
from PIL import Image
from textual.app import ComposeResult
from rich_pixels import Pixels
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Input, Static

from util.config import load_config
from util.metadata import read_metadata, write_metadata
from util.query import track_getinfo


class EditPage(Screen):

    BINDINGS = [Binding("ctrl-s", "save", "save"), Binding("ctrl-n", "next", "next")]

    def __init__(self, filepath: Path):
        super().__init__()
        self.filepath = filepath
        self.data = read_metadata(str(filepath))
        self.config = load_config()
        if self.config.lastfm_api_key != "":
            self.BINDINGS.append(Binding("ctrl-l", "look up", "look_up"))

    def compose(self) -> ComposeResult:
        self.title_input: Input = Input(
            placeholder="title", id="title", classes="round-border", value=self.data[0]
        )
        self.artist_input: Input = Input(
            placeholder="artist",
            id="artist",
            classes="round-border",
            value=self.data[1],
        )
        self.album_title_input: Input = Input(
            placeholder="album title",
            id="album-title",
            classes="round-border",
            value=self.data[2],
        )
        self.album_artist_input: Input = Input(
            placeholder="album artist",
            id="album-artist",
            classes="round-border",
            value=self.data[3],
        )
        image = Pixels.from_image(self.data[4].resize((60, 60)))

        self.album_art: Static = Static(image)

        # text_inputs = Vertical(self.title_input, self.artist_input, self.album_title_input, self.album_artist_input)
        with Horizontal():
            with Vertical():
                yield self.title_input
                yield self.artist_input
                yield self.album_title_input
                yield self.album_artist_input
            yield self.album_art

    def pull_data(self) -> tuple:
        data = (
            self.title_input.value,
            self.artist_input.value,
            self.album_title_input.value,
            self.album_artist_input.value,
            None,
        )
        return data

    def push_data(self, data: tuple) -> None:
        self.title_input.value = data[0]
        self.artist_input.value = data[1]
        self.album_title_input.value = data[2]
        self.album_artist_input.value = data[3]
        # TODO: this whole file needs to have album art added
        self.album_art.update(Pixels.from_image(data[4]))

    def action_save(self) -> None:
        write_metadata(self.filepath, self.pull_data())
        # TODO: rename file, maybe should go in metadata utils?
        pass

    def action_next(self) -> None:
        pass

    def action_search(self) -> None:
        data = self.pull_data()
        # TODO: error handle title or artist blank
        results = track_getinfo(self.config.lastfm_api_key, data[0], data[1])
        # if results:
        # self.push_data(results)
        # TODO: pull the title and artist then search lastfm
        # populate on success
        pass
