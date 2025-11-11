from typing import List
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, SelectionList

from pages.fileselectpage import FileSelectPage
from util.config import Config, load_config, save_config
from util.query import track_getinfo


class SettingsPage(Screen):

    BINDINGS = [Binding("escape", "exit_settings", "exit settings")]

    def compose(self) -> ComposeResult:
        self.lastfm_api_key: Input = Input(
            placeholder="last.fm API key",
            id="lastfm-api-key",
            password=True,
            classes="round-border",
        )
        self.lastfm_api_key.border_title = "last.fm API key"
        self.filename_format: Input = Input(
            # TODO: format tooltip as some kind of rich table ( | %t | title | )
            placeholder="filename format", id="filename-format", classes="round-border", tooltip="TODO"
        )
        self.filename_format.border_title = "filename format"
        self.tag_entry: Input = Input(
            placeholder="tag", id="tag-entry", classes="round-border"
        )
        self.tag_entry.border_title = "new tag"
        self.tags: List[str] = []
        self.tags_list: SelectionList = SelectionList(
            id="tags-list",
            classes="round-border"
        )
        self.tags_list.tooltip = "these tags will be automatically selected if provided by last.fm"
        # TODO: come up with a better name for this
        self.tags_list.border_title = "auto-select tags"

        self.load_config()
        self.update_tags_list()

        yield self.lastfm_api_key
        yield self.filename_format
        yield self.tag_entry
        yield self.tags_list
        yield Button("continue", variant="primary", flat=True)
        yield Footer()

    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        # make sure this tag is not already in the list
        if event.value in self.tags_list.selected:
            self.app.notify(
                "Hey, that tag is already in the list!",
                severity="warning",
            )
            return
        # add tag to the list and clear the input to prepare for another
        self.tags.append(event.value)
        self.update_tags_list()
        self.tag_entry.clear()

    @on(SelectionList.SelectionToggled)
    def on_selectionlist_selectiontoggled(self, event: SelectionList.SelectionToggled) -> None:
        tag = self.tags_list.get_option_at_index(event.selection_index)
        if not tag.disabled:
            self.tags.remove(tag.value)
            self.update_tags_list()

    def update_tags_list(self) -> None:
        self.tags_list.clear_options()
        self.tags_list.add_options(items=[(tag, tag, True) for tag in self.tags])

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
        self.app.install_screen(FileSelectPage(), "fileselect")
        self.app.push_screen("fileselect")

    def load_config(self) -> None:
        config = load_config(self.app)
        if config.lastfm_api_key != "":
            self.lastfm_api_key.value = config.lastfm_api_key
        if config.filename_format != "":
            self.filename_format.value = config.filename_format
        self.tags = config.tags

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

    def action_exit_settings(self) -> None:
        self.app.pop_screen()
