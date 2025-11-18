import logging
from pathlib import Path
from typing import List

from rich_pixels import Pixels
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Horizontal, Vertical
from textual.logging import TextualHandler
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Input,
    Label,
    ListItem,
    ListView,
    SelectionList,
    Static,
)
from textual.widgets.selection_list import Selection

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
        Binding("ctrl+s", "search", "search"),
    ]

    def __init__(self, files: List[Path]):
        super().__init__()
        self.file_paths = files
        self.file_index = 0
        self.config = load_config(self.app)

    def compose(self) -> ComposeResult:
        self.filenames_list: ListView = ListView(
            *[ListItem(Label(file.name)) for file in self.file_paths], id="filenames-list"
        )

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
            with Vertical(id="right-column"):
                with Center():
                    yield self.album_art
        yield Footer()

    def pull_data(self) -> tuple:
        data = (
            self.title_input.value,
            self.artist_input.value,
            self.album_title_input.value,
            self.album_artist_input.value,
            self.album_art_raw,
            self.tags_list.selected,
        )
        return data

    def push_data(self) -> None:
        self.filename.update(self.file_paths[self.file_index].name)
        data = read_metadata(self.file_paths[self.file_index])

        self.title_input.value = data[0]
        self.artist_input.value = data[1]
        self.album_title_input.value = data[2]
        self.album_artist_input.value = data[3]

        self.album_art_raw = data[4]
        image = Pixels.from_image(data[4].resize((40, 40)))
        self.album_art.update(image)
        self.album_art.styles.width = 40
        self.album_art.styles.height = 20

        tags: List[str] = data[5]
        self.tags_list.clear_options()
        for tag in tags:
            self.tags_list.add_option(Selection(tag, tag, True))

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
        # self.filenames_list.highlighted_child = self.filenames_list. [self.file_index]
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
        _ = track_getinfo(self.config.lastfm_api_key, data[0], data[1])
        # if results:
        # self.push_data(results)
        # TODO: pull the title and artist then search lastfm
        # populate on success

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
