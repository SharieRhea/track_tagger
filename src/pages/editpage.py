import logging
from io import BytesIO
from pathlib import Path
from typing import List

from PIL import Image
from PIL.ImageFile import ImageFile
from rich_pixels import Pixels
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Horizontal, Vertical
from textual.logging import TextualHandler
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Input,
    Label,
    ListItem,
    ListView,
    SelectionList,
    Static,
)
from textual.widgets.selection_list import Selection

from modals.albumartselectmodal import AlbumArtSelectModal
from util.config import load_config
from util.metadata import read_metadata, write_metadata
from util.query import get_album_image, track_getinfo

logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
)

# TODO: add some type of indication that there are unsaved changes!


class EditPage(Screen):

    BINDINGS = [
        Binding("ctrl+o", "write_out", "write out"),
        Binding("ctrl+p", "previous", "previous"),
        Binding("ctrl+n", "next", "next"),
        Binding("ctrl+s", "search", "search"),
    ]

    def __init__(self, files: List[Path]):
        super().__init__()
        self.file_paths = files
        self.file_index = 0
        self.config = load_config(self.app)

    def compose(self) -> ComposeResult:
        self.filenames_list: ListView = ListView(
            *[ListItem(Label(file.name), classes="filename-list-item") for file in self.file_paths],
            id="filenames-list",
            classes="round-border"
        )
        self.filenames_list.border_title = "files"

        self.filename: Label = Label(id="filename", classes="round-border")
        self.title_input: Input = Input(placeholder="title", id="title", classes="round-border")
        self.title_input.border_title = "track title"
        self.artist_input: Input = Input(
            placeholder="artist",
            id="artist",
            classes="round-border",
        )
        self.artist_input.border_title = "artist"
        self.album_title_input: Input = Input(
            placeholder="album title",
            id="album-title",
            classes="round-border",
        )
        self.album_title_input.border_title = "album title"
        self.album_artist_input: Input = Input(
            placeholder="album artist",
            id="album-artist",
            classes="round-border",
        )
        self.album_artist_input.border_title = "album artist"
        self.album_art: Static = Static(id="album-art")
        self.tag_entry: Input = Input(placeholder="tag", id="tag-entry", classes="round-border")
        self.tag_entry.border_title = "new tag"
        self.tags_list: SelectionList = SelectionList(id="tags-list", classes="round-border")
        self.tags_list.border_title = "tags"
        self.push_data()

        # force sizing for the album art for the layout to look nice
        self.album_art.styles.width = 40
        self.album_art.styles.height = 20

        self.update_button: Button = Button("update", id="update-button", variant="primary", flat=True)

        with Horizontal(id="editpage-columns"):
            yield self.filenames_list
            with Vertical(id="left-column"):
                yield self.filename
                yield self.title_input
                yield self.artist_input
                yield self.album_title_input
                yield self.album_artist_input
                yield self.tag_entry
                yield self.tags_list
            with Vertical(id="right-column", classes="center"):
                with Center():
                    yield self.album_art
                with Center():
                    yield self.update_button
        yield Footer()

    def pull_data(self) -> dict:
        data = {}
        data["track_title"] = self.title_input.value
        data["artist"] = self.artist_input.value
        data["album_title"] = self.album_title_input.value
        data["album_artist"] = self.album_artist_input.value
        data["album_art"] = self.album_art_raw
        data["tags"] = self.tags_list.selected
        return data

    def push_data(self, data: dict | None = None) -> None:
        self.filename.update(self.file_paths[self.file_index].name)
        if not data:
            data = read_metadata(self.file_paths[self.file_index])

        self.title_input.value = data["track_title"]
        self.artist_input.value = data["artist"]
        self.album_title_input.value = data["album_title"]
        self.album_artist_input.value = data["album_artist"]

        self.update_album_art(data["album_art"])

        tags: List[str] = data["tags"]
        logging.debug(tags)
        self.tags_list.clear_options()
        for tag in tags:
            self.tags_list.add_option(Selection(tag, tag, True))

    def update_album_art(self, data: ImageFile | Path | str | None) -> None:
        if not data:
            return

        if isinstance(data, Path):
            # this is a local file, open it and set the album art
            self.album_art_raw = Image.open(data)
        elif isinstance(data, str):
            # this is an image link
            image_bytes = get_album_image(data)
            if image_bytes:
                self.album_art_raw = Image.open(BytesIO(image_bytes))
        else:
            # this is already the opened image, just set it
            self.album_art_raw = data

        # TODO: what happens when an image isn't actually a square? does it crop?
        image = Pixels.from_image(self.album_art_raw.resize((40, 40)))
        self.album_art.update(image)

    @on(Button.Pressed)
    def on_button_pressed(self, _: Button.Pressed) -> None:
        self.app.push_screen(AlbumArtSelectModal(), self.update_album_art)

    @on(ListView.Selected)
    def on_listview_selected(self, event: ListView.Selected) -> None:
        self.file_index = event.index
        self.push_data()
        self.refresh_bindings()

    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        # make sure this tag is not already in the list
        if event.value in [option.prompt for option in self.tags_list.options]:
            self.app.notify(
                "Hey, that tag is already in the list!",
                severity="warning",
            )
            return
        # TODO: possibly sanitize? (lower?)
        self.tags_list.add_option((event.value, event.value, True))
        self.tag_entry.clear()

    def action_write_out(self) -> None:
        if write_metadata(self.file_paths[self.file_index], self.pull_data()):
            self.app.notify(
                "File saved successfully!",
                severity="information",
            )
        else:
            self.app.notify(
                "Unable to save file!",
                severity="error",
            )
        # TODO: rename file, maybe should go in metadata utils?

    def action_next(self) -> None:
        self.file_index += 1
        self.push_data()
        self.refresh_bindings()
        self.filenames_list.index = self.file_index

    def action_previous(self) -> None:
        self.file_index -= 1
        self.push_data()
        self.refresh_bindings()
        self.filenames_list.index = self.file_index

    def action_search(self) -> None:
        self.refresh_bindings()
        data = self.pull_data()
        # TODO: error handle title or artist blank
        result = track_getinfo(self.config.lastfm_api_key, data["track_title"], data["artist"])
        if result:
            self.push_data(result)
            self.app.notify(f"last.fm query for {data["track_title"]} by {data["artist"]} successful!", severity="information")

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
        if action == "next" and self.file_index == len(self.file_paths) - 1:
            return None
        return True
