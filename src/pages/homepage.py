from typing import List
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Input, Markdown, SelectionList

from pages.editpage import EditPage
from util.config import Config, load_config, save_config
from util.query import track_getinfo

MARKDOWN = """\
# track_tagger

Welcome to track_tagger!     
"""


class HomePage(Screen):

    def compose(self) -> ComposeResult:
        self.lastfm_api_key: Input = Input(
            placeholder="last.fm API key",
            id="lastfm-api-key",
            password=True,
            classes="round-border",
        )
        self.filename_format: Input = Input(
            placeholder="filename format", id="filename-format", classes="round-border"
        )
        self.tag_entry: Input = Input(
            placeholder="tag", id="tag-entry", classes="round-border"
        )
        self.tags: List[str] = []
        self.tags_list: SelectionList = SelectionList(
            *[(tag, index, True) for (index, tag) in enumerate(self.tags)],
            id="tags-list",
            classes="round-border"
        )

        self.load_config()

        yield Markdown(MARKDOWN, classes="round-border")
        yield self.lastfm_api_key
        yield self.filename_format
        yield self.tag_entry
        yield self.tags_list
        yield Button("continue", variant="primary", flat=True)

    @on(Button.Pressed)
    def on_button_pressed(self, _: Button.Pressed) -> None:
        if not self.validate_lastfm_api_key() or not self.validate_filename_format():
            return

        # save the config, not worth it to check if anything has changed or not
        save_config(
            Config(
                lastfm_api_key=self.lastfm_api_key.value,
                filename_format=self.filename_format.value,
                tags=self.tags_list.selected,
            )
        )
        # TODO: hard coded file for debugging
        self.app.install_screen(EditPage("/home/sharie/Music/personal/Old Music/Bad Liar - Imagine Dragons.mp3"), "edit")
        self.app.push_screen("edit")

    def load_config(self) -> None:
        config = load_config()
        if config.lastfm_api_key != "":
            self.lastfm_api_key.value = config.lastfm_api_key
        if config.filename_format != "":
            self.filename_format.value = config.filename_format
        self.tags_list.add_options(items=[(tag, tag) for tag in config.tags])

    def validate_lastfm_api_key(self) -> bool:
        # if no key is provided, assume they will be entering values manually
        if self.lastfm_api_key.value == "":
            return True
        # query something just to see if the key is valid
        if track_getinfo(self.lastfm_api_key.value, "Dirt", "Alice in Chains") is None:
            self.app.notify(
                "Hey, your last.fm key was unable to query successfully!",
                severity="error",
            )
            return False
        return True

    def validate_filename_format(self) -> bool:
        # make sure the filename format does not have illegal characters
        illegal_characters = ["/", "\\", "*", '"', "<", ">", ":", "|", "?", "."]
        if any(
            character in self.filename_format.value for character in illegal_characters
        ):
            self.app.notify(
                "Hey, there is an invalid character in your filename format!",
                severity="error",
            )
            return False
        return True
