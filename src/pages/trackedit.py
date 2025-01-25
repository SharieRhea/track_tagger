from flet import (
    Column,
    Container,
    FilledButton,
    OutlinedButton,
    Row, 
    SafeArea,
    Text,
    TextField,
    VerticalDivider, 
)
from flet.app import flet

from controls.sidebar import Sidebar
from controls.tagchips import TagChipsControl
from util.state import State

class TrackEditPage(Container):
    def __init__(self, state: State):
        super().__init__()
        self.state = state

        sidebar = Sidebar(state)

        title_field = TextField(
            label="Title",
            width=500
        )
        artist_field = TextField(
            label="Artist",
            width=500
        )
        album_field = TextField(
            label="Album",
            width=500
        )
        album_artist_field = TextField(
            label="Album Artist",
            width=500
        )

        tags = TagChipsControl(self.state, "track_tags", "Tags")

        info_column = Column(controls=[
            Text(self.state.files[self.state.current_file_index].name, theme_style=flet.TextThemeStyle.HEADLINE_LARGE),
            title_field,
            artist_field,
            album_field,
            album_artist_field,
            tags.content
        ])

        buttons = Column(controls=[
            OutlinedButton("Search last.fm", disabled=not self.state.use_lastfm, on_click=self.on_click_search_lastfm),
            FilledButton("Continue", icon=flet.Icons.ARROW_FORWARD_ROUNDED, on_click=self.on_click_continue)
        ], alignment=flet.MainAxisAlignment.END)

        # put all the content together on the page
        self.content = SafeArea(content=Row(controls=[
            sidebar.content,
            VerticalDivider(thickness=3),
            info_column,
            buttons
        ], expand=True,
        height=self.state.height))

    def on_click_continue(self, _):
        # TODO:
        pass

    def on_click_search_lastfm(self, _):
        # TODO:
        pass
