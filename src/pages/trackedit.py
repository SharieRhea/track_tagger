from flet import (
    Column,
    Container,
    CrossAxisAlignment,
    FilledButton,
    FloatingActionButton,
    Image,
    OutlinedButton,
    Row, 
    SafeArea,
    SnackBar,
    Stack,
    Text,
    TextField,
    VerticalDivider, 
)
from flet.app import flet

from controls.sidebar import Sidebar
from controls.tagchips import TagChipsControl
from util import metadata, query
from util.state import State

class TrackEditPage(Container):
    def __init__(self, state: State):
        super().__init__()
        self.state = state

        sidebar = Sidebar(state)

        self.title_field = TextField(
            label="Title",
            width=500
        )
        self.artist_field = TextField(
            label="Artist",
            width=500
        )
        self.album_field = TextField(
            label="Album",
            width=500
        )
        self.album_artist_field = TextField(
            label="Album Artist",
            width=500
        )

        self.tags = TagChipsControl(self.state, "track_tags", "Tags")

        self.album_image = Image(src="generic_album_cover.jpg", gapless_playback=True, border_radius=10, height=400, width=400)

        left_column = Column(controls=[
            Text(self.state.files[self.state.current_file_index].name, theme_style=flet.TextThemeStyle.HEADLINE_LARGE),
            self.title_field,
            self.artist_field,
            self.album_field,
            self.album_artist_field,
            self.tags.content
        ], expand=2)

        buttons = Column(controls=[
            OutlinedButton("Search last.fm", disabled=not self.state.use_lastfm, on_click=self.on_click_search_lastfm),
            FilledButton("Continue", icon=flet.Icons.ARROW_FORWARD_ROUNDED, on_click=self.on_click_continue)
        ], horizontal_alignment=flet.CrossAxisAlignment.END)

        album_image_stack = Stack(controls=[
            self.album_image,
            Container(content=FloatingActionButton(
                icon=flet.Icons.EDIT_ROUNDED, 
                mini=True, 
                on_click=self.on_click_edit_album_image), 
            alignment=flet.alignment.bottom_right,
            margin=16)
        ], height=300, width=300)

        right_column = Column(controls=[
            album_image_stack,
            buttons
        ], alignment=flet.MainAxisAlignment.SPACE_BETWEEN, horizontal_alignment=CrossAxisAlignment.END, expand=1)

        # put all the content together on the page
        self.content = SafeArea(content=Row(controls=[
            sidebar.content,
            VerticalDivider(thickness=3),
            left_column,
            right_column
        ], expand=True,
        height=self.state.height, width=self.state.width))

        # try to read metadata for the first file
        self.read_metadata()

    def on_click_continue(self, _):
        # TODO:
        pass

    def read_metadata(self):
        data = metadata.read_metadata(self.state.files[self.state.current_file_index].path)
        self.title_field.value = data[0]
        self.artist_field.value = data[1]
        self.album_field.value = data[2]
        self.album_artist_field.value = data[3]
        # FIX: this doesn't display anything
        # self.album_image.src = data[4]
        self.tags.add_tags(data[5])

    def on_click_search_lastfm(self, _):
        # search based on what's entered in title and artist fields
        title = self.title_field.value
        artist = self.artist_field.value

        # make sure required info is there
        if title is None or title == "":
            self.title_field.error_text="A title is required to search last.fm!"
            self.title_field.update()
            return
        self.title_field.error_text = None
        if artist is None or artist == "":
            self.artist_field.error_text="A title is required to search last.fm!"
            self.artist_field.update()
            return
        self.artist_field.error_text = None

        info = query.track_getinfo(self.state.lastfm_key, title, artist)
        if info is None or "track" not in info:
            self.state.page.overlay.append(SnackBar(
                content=Text(f"Unable to find a match for {title} by {artist}!", color=flet.Colors.ON_ERROR_CONTAINER), 
                open=True, 
                bgcolor=flet.Colors.ERROR_CONTAINER
            ))
            self.state.page.update()
            return

        # update everything according to what was found from lastfm
        self.title_field.value = info["track"]["name"]
        self.artist_field.value = info["track"]["artist"]["name"]

        if "album" in info["track"]:
            self.album_field.value = info["track"]["album"]["title"]
            self.album_artist_field.value = info["track"]["album"]["artist"]

            # see if there is a valid album image cover
            # -1 to get the largest image resolution available
            album_image_url = info["track"]["album"]["image"][-1]["#text"]
            if album_image_url != "":
                # album_image = query.get_album_image(album_image_url) 
                # if album_image is not None:
                self.album_image.src = album_image_url

        # TODO: populate tags from the query

        # update the page to show all changes
        if self.content is not None:
            self.content.update()

    def on_click_edit_album_image(self, _):
        # TODO:
        pass
